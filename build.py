#!/usr/bin/env python3
"""
build.py — pre-renders the dynamic pages so crawlers see real content.

Why this exists: property-detail.html, school.html and blog-post.html render
everything client-side. AI crawlers (GPTBot, ClaudeBot, PerplexityBot) and
link-preview bots (WhatsApp, iMessage) never execute JavaScript, so every
listing looked like an empty template with a generic title and og-image.

What it does, on every Vercel deploy (and locally via `python3 build.py`):
  1. Fetches listings / schools / posts from Supabase using the PUBLIC
     read-only key (already in the repo; RLS allows anonymous SELECT only).
  2. Uses the three existing pages as templates and bakes one real page per
     row into /property/<id>/, /school/<slug>/, /blog/<slug>/ — with per-page
     <title>, meta description, canonical, Open Graph tags, JSON-LD, and the
     visible content in plain HTML.
  3. The existing client-side JS still runs on load and re-renders from live
     data, so humans always see fresh content; the baked HTML is for bots.
  4. Regenerates sitemap.xml with every URL.

If Supabase is unreachable or an anchor string is missing, the build FAILS —
Vercel then keeps the previous deployment live, so the site never half-ships.
"""
import html
import json
import os
import re
import shutil
import sys
from datetime import date
from urllib.request import Request, urlopen

SITE = "https://soldbytiago.com"
SB_URL = "https://xjliwfmugylwxlrwyvmh.supabase.co"
# Publishable anon key: read-only via RLS, and already public in this repo.
SB_KEY = "sb_publishable_YHOe_eAJzuWpzbFD_tO-4A_vuvnSHum"
ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().isoformat()

# Posts that have a hand-built custom page instead of the generated template.
CUSTOM_BLOG_PAGES = {"el-chante-tamarindo-villas"}


# ── helpers ──────────────────────────────────────────────────────

def fetch(path):
    req = Request(
        f"{SB_URL}/rest/v1/{path}",
        headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}"},
    )
    with urlopen(req, timeout=30) as r:
        return json.load(r)


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def sub_once(doc, pattern, replacement, label, count=1, flags=0):
    """Regex-replace that fails the build if the anchor is missing/ambiguous."""
    out, n = re.subn(pattern, replacement, doc, flags=flags)
    if n != count:
        raise SystemExit(f"BUILD FAILED: anchor '{label}' matched {n}x (expected {count})")
    return out


def inline_md(t):
    """Inline markdown → HTML. Input must already be HTML-escaped."""
    t = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+|mailto:[^\s)]+)\)",
        r'<a href="\2" class="body-link" target="_blank" rel="noopener">\1</a>',
        t,
    )
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t


def parse_body(text):
    """Same markdown subset the site's JS parser supports."""
    if not text:
        return ""
    out = []
    for block in (b.strip() for b in text.split("\n\n")):
        if not block:
            continue
        block = esc(block)
        if block == "---":
            out.append('<hr class="body-hr" />')
            continue
        if block.startswith("### "):
            out.append("<h3>" + inline_md(block[4:]) + "</h3>")
            continue
        if block.startswith("## "):
            out.append("<h2>" + inline_md(block[3:]) + "</h2>")
            continue
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if len(lines) > 1 and all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join("<li>" + inline_md(l[2:]) + "</li>" for l in lines) + "</ul>")
            continue
        if len(lines) > 1 and all(re.match(r"^\d+\.\s", l) for l in lines):
            out.append("<ol>" + "".join("<li>" + inline_md(re.sub(r"^\d+\.\s", "", l)) + "</li>" for l in lines) + "</ol>")
            continue
        out.append("<p>" + inline_md(block) + "</p>")
    return "".join(out)


def one_line(s, limit=155):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= limit else s[: limit - 1].rstrip() + "…"


def fmt_num(v):
    if v in (None, "", 0):
        return None
    f = float(v)
    return str(int(f)) if f.is_integer() else str(f)


def area_both(v):
    """Area stored in m², rendered in both systems (buyers here use both)."""
    if not v:
        return None
    m2 = int(float(v))
    sf = format(round(m2 * 10.7639), ",")
    return format(m2, ",") + ' m&sup2;<span class="detail-stat-alt">' + sf + " ft&sup2;</span>"


def write_page(rel_dir, content):
    d = os.path.join(ROOT, rel_dir)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)


def head_common(doc, title, desc, canon, og_title, og_desc, og_image):
    """Per-page head surgery shared by all three templates."""
    if '<base href="/">' not in doc:
        doc = sub_once(doc, r"<head>", '<head>\n  <base href="/">', "<head> (base tag)")
    doc = sub_once(doc, r"<title>[^<]*</title>", f"<title>{esc(title)}</title>", "<title>")
    doc = sub_once(
        doc,
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{esc(desc)}">',
        "meta description",
    )
    og_block = (
        f'<meta property="og:title" content="{esc(og_title)}">\n'
        f'  <meta property="og:description" content="{esc(og_desc)}">\n'
        f'  <meta property="og:url" content="{canon}">'
    )
    if re.search(r'<link rel="canonical" href="[^"]*">', doc):
        doc = sub_once(
            doc, r'<link rel="canonical" href="[^"]*">',
            f'<link rel="canonical" href="{canon}">', "canonical",
        )
    else:
        doc = sub_once(
            doc, r'(<meta name="description" content="[^"]*">)',
            f'\\1\n  <link rel="canonical" href="{canon}">', "canonical insert",
        )
    if re.search(r'<meta property="og:title" content="[^"]*">', doc):
        doc = sub_once(doc, r'<meta property="og:title" content="[^"]*">', og_block, "og:title")
    else:
        doc = sub_once(
            doc, r'(<link rel="canonical" href="[^"]*">)', f"\\1\n  {og_block}", "og block insert",
        )
    for pat, label in (
        (r'<meta property="og:image" content="[^"]*">', "og:image"),
        (r'<meta name="twitter:image" content="[^"]*">', "twitter:image"),
    ):
        if re.search(pat, doc):
            attr = 'property="og:image"' if "og:image" in label else 'name="twitter:image"'
            doc = sub_once(doc, pat, f'<meta {attr} content="{esc(og_image)}">', label)
        else:
            doc = sub_once(
                doc, r'(<meta property="og:url"[^>]*>)',
                f'\\1\n  <meta {"property" if "og" in label else "name"}="{label}" content="{esc(og_image)}">',
                label + " insert",
            )
    return doc


def agent_ld(knows_about):
    """Compact RealEstateAgent node. Same @id and core fields as the homepage
    #agent entity so crawlers and AI assistants merge them into one entity;
    knowsAbout carries the page-specific topic."""
    return {
        "@context": "https://schema.org",
        "@type": "RealEstateAgent",
        "@id": SITE + "/#agent",
        "name": "Tiago Leao",
        "url": SITE,
        "telephone": "+506-8302-8660",
        "email": "tiago@soldbytiago.com",
        "worksFor": {"@type": "Organization", "name": "KRAIN Luxury Real Estate"},
        "areaServed": "Guanacaste, Costa Rica",
        "knowsAbout": knows_about,
    }


def fill_cta_name(doc, default, name, label):
    """Bake the page's name into the closing-CTA spans (2 in each template)."""
    needle = f'<span class="cta-name">{default}</span>'
    n = doc.count(needle)
    if n != 2:
        raise SystemExit(f"BUILD FAILED: expected 2 CTA name spans in {label}, found {n}")
    return doc.replace(needle, f'<span class="cta-name">{esc(name)}</span>')


def ld_script(obj, baked=True):
    attr = ' data-baked="1"' if baked else ""
    return f'<script type="application/ld+json"{attr}>\n{json.dumps(obj, indent=2, ensure_ascii=False)}\n</script>'


# ── properties ───────────────────────────────────────────────────

# SVGs and band wording mirror renderAreaSection() in property-detail.html —
# keep the two in sync so the runtime re-render is pixel-identical.
_AROUND_ICONS = {
    "walk": '<svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><circle cx="13" cy="4" r="2"/><path d="M7 21l3-7 4-2-1-5"/><path d="M13 7l4 2 2 4"/><path d="M10 14l-3-3"/></svg>',
    "beach": '<svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18c2 0 2-1.5 4-1.5S8 18 10 18s2-1.5 4-1.5S16 18 18 18s2-1.5 4-1.5"/><path d="M2 22c2 0 2-1.5 4-1.5S8 22 10 22s2-1.5 4-1.5S16 22 18 22s2-1.5 4-1.5"/><circle cx="12" cy="7" r="4"/></svg>',
    "plane": '<svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M17.8 19.2L16 11l3.5-3.5a2.5 2.5 0 000-3.5 2.5 2.5 0 00-3.5 0L12.5 7.5 4.3 5.7a1 1 0 00-1 1.6L8 11l-2 2H3l-1 2 4 1 1 4 2-1v-3l2-2 3.7 4.7a1 1 0 001.6-1z"/></svg>',
}


def _around_tile(icon, label, value, unit, note):
    return ('<div class="around-tile"><div class="around-icon">' + _AROUND_ICONS[icon]
            + '</div><div><div class="around-label">' + label
            + '</div><div class="around-value">' + str(value)
            + (' <span>' + unit + '</span>' if unit else '')
            + '</div>' + ('<div class="around-note">' + note + '</div>' if note else '')
            + '</div></div>')


def _around_tiles(p):
    tiles = []
    ws = p.get("walk_score")
    if ws is not None and ws != "":
        ws = int(ws)
        band = ("Walker's paradise" if ws >= 90 else "Very walkable" if ws >= 70
                else "Somewhat walkable" if ws >= 50 else "Car dependent" if ws >= 25 else "Car required")
        tiles.append(_around_tile("walk", "Walk Score", ws, "/ 100", band))
    bm = p.get("beach_minutes")
    if bm is not None and bm != "":
        drive = p.get("beach_mode") == "drive"
        tiles.append(_around_tile("beach", "To the beach", bm, "min", "By car" if drive else "On foot"))
    am = p.get("airport_minutes")
    if am is not None and am != "":
        tiles.append(_around_tile("plane", "To Liberia (LIR)", am, "min", "By car"))
    return "".join(tiles)


def _sim_card(o):
    slug = o.get("slug") or o["id"]
    name = esc(o.get("name") or "")
    img = ('<img src="' + esc(o["photos"][0]) + '" alt="' + name + '" />') if o.get("photos") else ""
    typ = (o.get("type") or "property").capitalize()
    size = f'{int(o["size"]):,}' if o.get("size") else "&mdash;"
    return ('<a href="/property/' + slug + '/" class="sim-card"><div class="sim-img">' + img
            + '<span class="sim-type">' + esc(typ) + '</span></div><div class="sim-info">'
            + '<div class="sim-price">' + esc(o.get("price") or "&mdash;") + '</div>'
            + '<div class="sim-meta"><strong>' + str(o.get("beds") or "&mdash;") + '</strong> bd'
            + '<span class="meta-div">|</span><strong>' + str(o.get("baths") or "&mdash;") + '</strong> ba'
            + '<span class="meta-div">|</span><strong>' + size + '</strong> m&sup2;</div>'
            + '<div class="sim-name">' + name + '</div></div></a>')


def build_properties(tpl, rows):
    if not rows:
        raise SystemExit("BUILD FAILED: zero properties returned")
    urls = []
    for p in rows:
        pid = p["id"]
        name = p.get("name") or "Property in Guanacaste"
        loc = p.get("location") or "Guanacaste, Costa Rica"
        price = p.get("price") or ""
        sold = p.get("status") == "sold"
        photos = [u for u in (p.get("photos") or []) if u]
        slug = (p.get("slug") or "").strip()
        seg = slug or pid
        canon = f"{SITE}/property/{seg}/"
        desc = one_line(p.get("short_desc") or p.get("description") or f"{name} in {loc}.")
        title = f"{name} | Tiago Leao | Guanacaste Real Estate"
        og_title = f"{name} — Sold" if sold else (f"{name} — {price}" if price else name)
        og_image = photos[0] if photos else f"{SITE}/og-image.jpg"

        doc = head_common(tpl, title, desc, canon, og_title, f"{loc}. {desc}", og_image)

        # Replace the generic Product JSON-LD with the real listing schema.
        price_num = re.sub(r"[^0-9]", "", str(price))
        about_type = {"condo": "Apartment", "home": "House", "villa": "House"}.get(
            (p.get("type") or "home").lower(), "Residence"
        )
        ld = {
            "@context": "https://schema.org",
            "@type": "RealEstateListing",
            "url": canon,
            "name": name,
            "description": desc,
            "image": photos[:6] or [f"{SITE}/og-image.jpg"],
            "datePosted": (p.get("created_at") or TODAY)[:10],
            "about": {
                "@type": about_type,
                "numberOfBedrooms": fmt_num(p.get("beds")),
                "numberOfBathroomsTotal": fmt_num(p.get("baths")),
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": loc,
                    "addressRegion": "Guanacaste",
                    "addressCountry": "CR",
                },
            },
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "availability": "https://schema.org/SoldOut" if sold else "https://schema.org/InStock",
                "seller": {"@type": "RealEstateAgent", "name": "Tiago Leao", "url": SITE},
            },
        }
        if price_num:
            ld["offers"]["price"] = int(price_num)
        if p.get("lat") is not None and p.get("lng") is not None:
            ld["about"]["geo"] = {"@type": "GeoCoordinates", "latitude": p["lat"], "longitude": p["lng"]}
        if p.get("size"):
            ld["about"]["floorSize"] = {"@type": "QuantitativeValue", "value": fmt_num(p["size"]), "unitCode": "MTK"}
        ld["about"] = {k: v for k, v in ld["about"].items() if v is not None}
        doc = sub_once(
            doc, r'<script type="application/ld\+json">.*?</script>',
            ld_script(ld).replace("\\", "\\\\"), "property JSON-LD", flags=re.S,
        )

        if sold:
            doc = sub_once(doc, r"<body>", '<body class="listing-sold">', "<body> sold class")

        # Visible content into the containers the JS later re-renders.
        doc = sub_once(
            doc, r'<div class="detail-eyebrow reveal" id="detail-type">Property</div>',
            f'<div class="detail-eyebrow reveal" id="detail-type">{esc((p.get("type") or "home").capitalize())}</div>',
            "eyebrow",
        )
        doc = sub_once(
            doc, r'<h1 class="detail-title reveal reveal-delay-1" id="detail-title">Loading property&hellip;</h1>',
            f'<h1 class="detail-title reveal reveal-delay-1" id="detail-title">{esc(name)}</h1>',
            "h1 title",
        )
        doc = sub_once(
            doc, r'<div class="detail-location reveal reveal-delay-2" id="detail-location"></div>',
            f'<div class="detail-location reveal reveal-delay-2" id="detail-location">{esc(loc)}</div>',
            "location",
        )
        price_html = (
            f'<span class="price-sold">{esc(price)}</span><span class="sold-flag">Sold</span>'
            if sold else esc(price)
        )
        doc = sub_once(
            doc, r'<div class="detail-price reveal reveal-delay-3" id="detail-price"></div>',
            f'<div class="detail-price reveal reveal-delay-3" id="detail-price">{price_html}</div>',
            "price",
        )
        for stat, val in (
            ("stat-beds", fmt_num(p.get("beds"))),
            ("stat-baths", fmt_num(p.get("baths"))),
            ("stat-sqft", area_both(p.get("size"))),
            ("stat-lot", area_both(p.get("lot"))),
        ):
            doc = sub_once(
                doc, rf'<span class="detail-stat-value" id="{stat}">&mdash;</span>',
                f'<span class="detail-stat-value" id="{stat}">{val or "&mdash;"}</span>',
                stat,
            )
        paragraphs = "".join(
            "<p>" + esc(t) + "</p>" for t in (p.get("description") or "").split("\n\n") if t.strip()
        )
        doc = sub_once(
            doc, r'<div class="detail-description" id="detail-description"></div>',
            f'<div class="detail-description" id="detail-description">{paragraphs}</div>',
            "description",
        )
        feat_svg = ('<div class="feature-check"><svg viewBox="0 0 10 10" fill="none" stroke="#0d4a4a" '
                    'stroke-width="1.5"><path d="M1.5 5l2.5 2.5 4.5-4.5"/></svg></div>')
        feats = "".join(
            f'<div class="feature-item">{feat_svg}{esc(f)}</div>' for f in (p.get("features") or [])
        )
        if feats:
            doc = sub_once(
                doc, r'<div class="features-grid" id="features-grid"></div>',
                f'<div class="features-grid" id="features-grid">{feats}</div>',
                "features",
            )
        else:
            doc = sub_once(
                doc, r'<div class="detail-section-title">Features &amp; Amenities</div>\s*<div class="features-grid" id="features-grid"></div>',
                '<div class="features-grid" id="features-grid" style="display:none"></div>',
                "features (empty, heading dropped)", flags=re.S,
            )

        # Written location summary under the Location heading (survives a
        # failed map load, and gives crawlers real text instead of a shell).
        doc = sub_once(
            doc, r'<p class="map-location-line" id="map-location-line"></p>',
            f'<p class="map-location-line" id="map-location-line">{esc(loc)}</p>',
            "map location line",
        )

        # Getting Around: bake the tiles whenever the data exists, mirroring
        # the runtime renderAreaSection() markup exactly (JS re-renders the
        # same values, so there is no flash of different content).
        around = _around_tiles(p)
        if around:
            doc = sub_once(doc, r'<div id="area-section" style="display:none;">',
                           '<div id="area-section">', "area-section unhide")
            doc = sub_once(doc, r'<div id="around-block" class="area-block" style="display:none;">',
                           '<div id="around-block" class="area-block" style="display:block;">', "around-block unhide")
            doc = sub_once(doc, r'<div class="around-grid" id="around-grid"></div>',
                           f'<div class="around-grid" id="around-grid">{around}</div>', "around tiles")

        # Similar properties: bake three real cards (internal links crawlers
        # can follow) and unhide the section only when cards exist.
        others = [o for o in rows if o["id"] != p["id"] and o.get("status") == "active"][:3]
        if others:
            cards = "".join(_sim_card(o) for o in others)
            doc = sub_once(doc, r'<section class="similar-section" id="similar-section" style="display:none;">',
                           '<section class="similar-section" id="similar-section">', "similar unhide")
            doc = sub_once(doc, r'<div class="similar-grid" id="similar-grid">\s*<!-- Injected by JS -->\s*</div>',
                           f'<div class="similar-grid" id="similar-grid">{cards}</div>',
                           "similar cards", flags=re.S)
        NA = "Available on request"
        def _atext(v):
            m2 = int(float(v))
            return format(m2, ",") + " m&sup2; / " + format(round(m2 * 10.7639), ",") + " ft&sup2;"
        srows = [
            ("Location", esc(loc) if p.get("location") else NA),
            ("Asking price", "Sold" if sold else (esc(price) or NA)),
            ("Property type", esc((p.get("type") or "home").capitalize())),
            ("Bedrooms", fmt_num(p.get("beds")) or NA),
            ("Bathrooms", fmt_num(p.get("baths")) or NA),
            ("Built area", _atext(p["size"]) if p.get("size") else NA),
            ("Lot area", _atext(p["lot"]) if p.get("lot") else NA),
            ("Status", "Sold" if sold else "For sale"),
        ]
        sum_html = "".join(f'<div class="ps-row"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in srows)
        doc = sub_once(doc, r'<dl class="prop-summary" id="prop-summary-list"></dl>',
                       f'<dl class="prop-summary" id="prop-summary-list">{sum_html}</dl>', "summary list")
        upd = (p.get("updated_at") or "")[:10]
        if upd:
            doc = sub_once(doc, r'<p class="prop-summary-updated" id="prop-summary-updated"></p>',
                           f'<p class="prop-summary-updated" id="prop-summary-updated">Listing details last updated {upd}.</p>',
                           "summary updated")
        doc = doc.replace('<div class="map-placeholder">Map loading…</div>',
                          f'<div class="map-placeholder">Located in {esc(loc)}, Guanacaste, Costa Rica.</div>')
        if photos:
            doc = sub_once(
                doc, r'<span class="gallery-placeholder-label">Photo 1</span>',
                f'<img src="{esc(photos[0])}" alt="{esc(name)}" '
                'style="width:100%;height:100%;object-fit:cover;display:block;" />',
                "gallery main photo",
            )

        write_page(f"property/{seg}", doc)
        if slug:
            # The old uuid URL redirects permanently to the descriptive slug,
            # so nothing ever breaks and only one URL gets indexed.
            write_page(f"property/{pid}",
                '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
                + f'<title>{esc(name)}</title><link rel="canonical" href="{canon}">'
                + f'<meta http-equiv="refresh" content="0;url={canon}">'
                + f'<script>location.replace("{canon}")</script></head>'
                + f'<body><a href="{canon}">{esc(name)}</a></body></html>')
        urls.append((f"/property/{seg}/", (p.get("updated_at") or TODAY)[:10], "0.7", "weekly"))
    return urls


# ── schools ──────────────────────────────────────────────────────

def build_schools(tpl, rows):
    if not rows:
        raise SystemExit("BUILD FAILED: zero schools returned")
    urls = []
    for s in rows:
        slug = s["slug"]
        name = s.get("name") or "School"
        canon = f"{SITE}/school/{slug}/"
        desc = one_line(s.get("meta_desc") or s.get("excerpt") or f"{name} — schools in Guanacaste, Costa Rica.")
        title = f"{name} | Schools in Guanacaste | Tiago Leao"
        og_image = s.get("cover_url") or f"{SITE}/og-image.jpg"

        doc = head_common(tpl, title, desc, canon, name, desc, og_image)

        facts = ""
        for label, value in (
            ("Town", esc(s.get("town"))),
            ("Grades", esc(s.get("grades"))),
            ("Curriculum", esc(s.get("curriculum"))),
            ("Languages", esc(s.get("languages"))),
            ("Accreditation", esc(s.get("accreditation"))),
            ("Tuition", esc(s.get("tuition"))),
            ("Founded", esc(s.get("founded"))),
            ("Address", esc(s.get("address"))),
            ("Website", (f'<a href="{esc(s.get("website"))}" target="_blank" rel="noopener">'
                         f'{esc(re.sub(r"^https?://", "", (s.get("website") or "")).rstrip("/"))}</a>'
                         if s.get("website") else "")),
        ):
            if value:
                facts += (f'<div class="sch-fact"><div class="sch-fact-label">{label}</div>'
                          f'<div class="sch-fact-value">{value}</div></div>')
        body_html = parse_body(s.get("body")) or (
            '<p class="sch-empty">Details for this school come straight from the school itself; '
            "their website has the most current information.</p>"
        )
        hero_style = f' style="background-image:url(\'{esc(s["cover_url"])}\')"' if s.get("cover_url") else ""
        baked = f"""<div class="sch-crumb"><a href="index.html">Home</a> &rsaquo; <a href="schools.html">Schools</a> &rsaquo; {esc(name)}</div>
        <div class="sch-hero"{hero_style}></div>
        {f'<div class="sch-town">{esc(s["town"])}</div>' if s.get("town") else ''}
        <h1 class="sch-title">{esc(name)}</h1>
        {f'<p class="sch-excerpt">{esc(s["excerpt"])}</p>' if s.get("excerpt") else ''}
        <div class="sch-cols">
          <div class="sch-body">{body_html}</div>
          <aside class="sch-facts"><h3>The Details</h3>{facts}</aside>
        </div>"""
        doc = sub_once(doc, r'<div class="sch-loading">Loading&hellip;</div>', baked, "school content")

        ld = {
            "@context": "https://schema.org",
            "@type": "School",
            "name": name,
            "url": canon,
            "description": desc,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": s.get("address") or None,
                "addressLocality": s.get("town") or None,
                "addressRegion": "Guanacaste",
                "addressCountry": "CR",
            },
        }
        ld["address"] = {k: v for k, v in ld["address"].items() if v}
        if s.get("website"):
            ld["sameAs"] = [s["website"]]
        if s.get("lat") is not None and s.get("lng") is not None:
            ld["geo"] = {"@type": "GeoCoordinates", "latitude": s["lat"], "longitude": s["lng"]}
        crumbs = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Schools", "item": f"{SITE}/schools.html"},
                {"@type": "ListItem", "position": 3, "name": name, "item": canon},
            ],
        }
        agent = agent_ld(f"Homes near {name}, Guanacaste, Costa Rica")
        doc = sub_once(
            doc, r"</head>",
            ld_script(ld) + "\n" + ld_script(crumbs) + "\n" + ld_script(agent) + "\n</head>",
            "school ld insert"
        )
        doc = fill_cta_name(doc, "this school", name, f"school/{slug}")

        write_page(f"school/{slug}", doc)
        urls.append((f"/school/{slug}/", (s.get("updated_at") or TODAY)[:10], "0.6", "monthly"))
    return urls


def _dev_card(s):
    photo = (' style="background-image:url(' + "'" + esc(s["cover_url"]) + "'" + ')"') if s.get("cover_url") else ""
    tags = "".join('<span class="school-tag">' + esc(t) + "</span>"
                   for t in ((("Est. " + s["established"]) if s.get("established") else ""), s.get("best_for")) if t)
    town = ('<div class="school-card-town">' + esc(s["town"]) + "</div>") if s.get("town") else ""
    return ('<a href="/development/' + s["slug"] + '/" class="school-card">'
            + '<div class="school-card-photo"' + photo + "></div>"
            + '<div class="school-card-body">' + town
            + '<div class="school-card-name">' + esc(s.get("name") or "") + "</div>"
            + '<div class="school-card-excerpt">' + esc(s.get("excerpt") or "") + "</div>"
            + ('<div class="school-card-tags">' + tags + "</div>" if tags else "") + "</div></a>")


def build_developments(tpl, rows):
    urls = []
    for s in rows:
        slug = s["slug"]
        name = s.get("name") or "Community"
        canon = f"{SITE}/development/{slug}/"
        desc = one_line(s.get("meta_desc") or s.get("excerpt") or f"{name} - gated community in Guanacaste, Costa Rica.")
        title = f"{name} | Guanacaste Communities | Tiago Leao"
        og_image = s.get("cover_url") or f"{SITE}/og-image.jpg"
        doc = head_common(tpl, title, desc, canon, name, desc, og_image)

        facts = ""
        for label, value in (
            ("Town", esc(s.get("town"))),
            ("Established", esc(s.get("established"))),
            ("Typical asking range", esc(s.get("price_range"))),
            ("HOA fees", esc(s.get("hoa_fees"))),
            ("Amenities", esc(s.get("amenities"))),
            ("Beach access", esc(s.get("beach_access"))),
            ("Rental rules", esc(s.get("rental_rules"))),
            ("Construction", esc(s.get("construction_rules"))),
            ("Title structure", esc(s.get("title_structure"))),
            ("Best for", esc(s.get("best_for"))),
        ):
            if value:
                facts += ('<div class="sch-fact"><div class="sch-fact-label">' + label
                          + '</div><div class="sch-fact-value">' + value + "</div></div>")
        body_html = parse_body(s.get("body")) or ""
        hero_style = (' style="background-image:url(' + "'" + esc(s["cover_url"]) + "'" + ')"') if s.get("cover_url") else ""
        town_div = ('<div class="sch-town">' + esc(s["town"]) + "</div>") if s.get("town") else ""
        exc_p = ('<p class="sch-excerpt">' + esc(s["excerpt"]) + "</p>") if s.get("excerpt") else ""
        baked = ('<div class="sch-crumb"><a href="index.html">Home</a> &rsaquo; '
                 '<a href="developments.html">Communities</a> &rsaquo; ' + esc(name) + "</div>"
                 + '<div class="sch-hero"' + hero_style + "></div>"
                 + town_div
                 + '<h1 class="sch-title">' + esc(name) + "</h1>"
                 + exc_p
                 + '<div class="sch-cols"><div class="sch-body">' + body_html + "</div>"
                 + '<aside class="sch-facts"><h3>The Details</h3>' + facts + "</aside></div>")
        doc = sub_once(doc, r'<div class="sch-loading">Loading&hellip;</div>',
                       lambda m, b=baked: b, "dev content")

        ld = {
            "@context": "https://schema.org",
            "@type": "Residence",
            "name": name, "url": canon, "description": desc,
            "address": {"@type": "PostalAddress", "addressLocality": s.get("town") or None,
                        "addressRegion": "Guanacaste", "addressCountry": "CR"},
        }
        ld["address"] = {k: v for k, v in ld["address"].items() if v}
        if s.get("lat") is not None and s.get("lng") is not None:
            ld["geo"] = {"@type": "GeoCoordinates", "latitude": s["lat"], "longitude": s["lng"]}
        crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                      {"@type": "ListItem", "position": 2, "name": "Communities", "item": SITE + "/developments.html"},
                      {"@type": "ListItem", "position": 3, "name": name, "item": canon}]}
        agent = agent_ld(f"{name}, Guanacaste, Costa Rica")
        doc = sub_once(doc, r"</head>",
                       ld_script(ld) + "\n" + ld_script(crumbs) + "\n" + ld_script(agent) + "\n</head>",
                       "dev ld insert")
        doc = fill_cta_name(doc, "this community", name, f"development/{slug}")
        write_page(f"development/{slug}", doc)
        urls.append((f"/development/{slug}/", (s.get("updated_at") or TODAY)[:10], "0.7", "monthly"))
    return urls


# ── blog posts ───────────────────────────────────────────────────

def build_posts(tpl, rows):
    if not rows:
        raise SystemExit("BUILD FAILED: zero blog posts returned")
    urls = []
    for p in rows:
        slug = p["slug"]
        if slug in CUSTOM_BLOG_PAGES:
            continue
        title_txt = p.get("title") or "Article"
        canon = f"{SITE}/blog/{slug}/"
        desc = one_line(p.get("meta_desc") or p.get("excerpt") or title_txt)
        og_image = p.get("cover_url") or f"{SITE}/og-image.jpg"

        doc = head_common(tpl, f"{title_txt} | Tiago Leao | Guanacaste Real Estate", desc, canon, title_txt, desc, og_image)

        upd = (p.get("updated_at") or p.get("created_at") or TODAY)[:10]
        try:
            y, m, d = (int(x) for x in upd.split("-"))
            nice_date = f"{date(y, m, d):%B} {d}, {y}"
        except ValueError:
            nice_date = upd
        disclaimer = ""
        body_low = (p.get("body") or "").lower()
        if (p.get("category") or "") in ("guide", "investment", "market") and "not constitute legal" not in body_low and "not legal, tax" not in body_low:
            disclaimer = ('<p style="margin-top:32px;font-size:13px;line-height:1.6;color:#6b7a7a;">'
                          'This article is general information, not legal, tax, immigration, or financial advice. '
                          'Rules and figures change; confirm your situation with qualified Costa Rican professionals '
                          'before making decisions.</p>')
        sources = '<div style="margin-top:28px;padding-top:20px;border-top:1px solid rgba(0,0,0,0.08);"><p style="font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#0d4a4a;margin-bottom:8px;">Sources &amp; verification</p><p style="font-size:12.5px;line-height:1.8;color:#6b7a7a;">Official references for the rules and figures discussed: <a href="https://www.registronacional.go.cr" target="_blank" rel="noopener" style="color:#0d4a4a;">Registro Nacional</a> &middot; <a href="https://www.hacienda.go.cr" target="_blank" rel="noopener" style="color:#0d4a4a;">Ministerio de Hacienda</a> &middot; <a href="https://www.migracion.go.cr" target="_blank" rel="noopener" style="color:#0d4a4a;">Migraci&oacute;n</a> &middot; <a href="https://www.sugef.fi.cr" target="_blank" rel="noopener" style="color:#0d4a4a;">SUGEF</a> &middot; <a href="https://www.ict.go.cr" target="_blank" rel="noopener" style="color:#0d4a4a;">ICT</a> &middot; <a href="https://www.ccss.sa.cr" target="_blank" rel="noopener" style="color:#0d4a4a;">CCSS/CAJA</a>. Verify current requirements directly &mdash; rules change. Last reviewed: July 2026.</p></div>' if (p.get("category") or "") in ("guide", "investment", "market") else ""
        byline = (f'By <a href="about.html" style="color:inherit;text-decoration:underline;">Tiago Leao</a> &middot; '
                  f"KRAIN Luxury Real Estate &middot; Updated {nice_date}"
                  + (f" &middot; {esc(p['readtime'])}" if p.get("readtime") else ""))
        baked = f"""<a href="blog.html" class="article-back">&larr; All Articles</a>
    <div class="article-tag">{esc((p.get("category") or "guide").capitalize())}</div>
    <h1 class="article-title">{esc(title_txt)}</h1>
    <div class="article-byline">{byline}</div>
    <div class="article-body">
      {parse_body(p.get("body"))}
      <div class="article-cta"><p>Interested in learning more?</p><a href="index.html#form-section">Get in Touch &rarr;</a></div>
      {disclaimer}
      {sources}
    </div>"""
        doc = sub_once(doc, r'<div class="loading">Loading article\.\.\.</div>', baked, "article content")

        ld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title_txt,
            "description": desc,
            "url": canon,
            "datePublished": (p.get("created_at") or TODAY)[:10],
            "dateModified": upd,
            "image": og_image,
            "author": {"@type": "Person", "@id": f"{SITE}/#person", "name": "Tiago Leao", "url": f"{SITE}/about.html"},
            "publisher": {"@type": "RealEstateAgent", "name": "Tiago Leao | Guanacaste Real Estate", "url": SITE},
            "mainEntityOfPage": canon,
        }
        doc = sub_once(doc, r"</head>", ld_script(ld) + "\n</head>", "article ld insert")

        write_page(f"blog/{slug}", doc)
        urls.append((f"/blog/{slug}/", upd, "0.7", "monthly"))
    return urls


# ── root pages ───────────────────────────────────────────────────
# The index/properties/blog/schools grids are also client-rendered, so a
# crawler used to see "Loading…" placeholders and stale hardcoded counts.
# Real cards are injected between BAKE marker comments (which persist, so
# the injection is idempotent); the client JS still re-renders on load.

def inject(fname, start, end, content, label):
    path = os.path.join(ROOT, fname)
    with open(path, encoding="utf-8") as f:
        src = f.read()
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(src):
        raise SystemExit(f"BUILD FAILED: markers '{label}' missing in {fname}")
    src = pat.sub(lambda m: start + "\n" + content + "\n" + end, src, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    return src


def _prop_card(p):
    sold = p.get("status") == "sold"
    photos = [u for u in (p.get("photos") or []) if u]
    name = esc(p.get("name") or "")
    img = ('<img class="prop-slide active" src="' + esc(photos[0]) + '" alt="' + name + '" />') if photos else ""
    badge = ('<div class="prop-badge prop-badge-sold">Sold</div>' if sold
             else ('<div class="prop-badge">Featured</div>' if p.get("featured") else ""))
    meta = []
    if p.get("beds"):
        meta.append("<span><strong>" + fmt_num(p["beds"]) + "</strong> bds</span>")
    if p.get("baths"):
        meta.append("<span><strong>" + fmt_num(p["baths"]) + "</strong> ba</span>")
    if p.get("size"):
        meta.append("<span><strong>" + format(int(float(p["size"])), ",") + "</strong> m&sup2; / "
                    + format(round(float(p["size"]) * 10.7639), ",") + " ft&sup2;</span>")
    tname = esc((p.get("type") or "home").capitalize())
    meta.append("<span>" + tname + ("" if sold else " for sale") + "</span>")
    meta_html = '<span class="meta-divider">|</span>'.join(meta)
    price_num = re.sub(r"[^0-9]", "", str(p.get("price") or "")) or "0"
    loc = esc(p.get("location") or "")
    cls = "property-card visible-card" + (" is-sold" if sold else "")
    return ('<a href="/property/' + (p.get("slug") or p["id"]) + '/" class="' + cls + '"'
            + ' data-type="' + esc(p.get("type") or "home") + '" data-price="' + price_num + '"'
            + ' data-status="' + esc(p.get("status") or "active") + '" data-beds="' + (fmt_num(p.get("beds")) or "0") + '"'
            + ' data-lat="' + str(p.get("lat") or "") + '" data-lng="' + str(p.get("lng") or "") + '"'
            + ' data-created="' + esc((p.get("created_at") or ""))
            + '"><div class="prop-img">' + img + badge + '</div>'
            + '<div class="prop-info"><div class="prop-price">' + esc(p.get("price") or "") + '</div>'
            + '<div class="prop-meta">' + meta_html + '</div>'
            + '<div class="prop-name">' + name + (", " + loc if loc else "") + '</div></div></a>')


def _featured_card(p):
    photos = [u for u in (p.get("photos") or []) if u]
    bg = (' style="background-image:url(' + "'" + esc(photos[0]) + "'" + ');background-size:cover;background-position:center;"') if photos else ""
    tname = esc((p.get("type") or "home").capitalize())
    meta = []
    if p.get("beds"):
        meta.append("<span><strong>" + fmt_num(p["beds"]) + "</strong> Beds</span>")
    if p.get("baths"):
        meta.append("<span><strong>" + fmt_num(p["baths"]) + "</strong> Baths</span>")
    if p.get("size"):
        meta.append("<span><strong>" + format(int(float(p["size"])), ",") + "</strong> m&sup2; / "
                    + format(round(float(p["size"]) * 10.7639), ",") + " ft&sup2;</span>")
    return ('<a href="/property/' + (p.get("slug") or p["id"]) + '/" class="property-card">'
            + '<div class="property-img-placeholder"' + bg + '>'
            + '<div class="property-badge">Featured</div>'
            + '<div class="property-type-tag">' + tname + '</div></div>'
            + '<div class="property-info"><div class="property-name">' + esc(p.get("name") or "") + '</div>'
            + '<div class="property-location">' + esc(p.get("location") or "") + '</div>'
            + '<div class="property-price">' + esc(p.get("price") or "") + '</div>'
            + '<div class="property-meta">' + "".join(meta) + '</div></div></a>')


def _blog_card(p):
    href = ("blog-el-chante-tamarindo.html" if p["slug"] in CUSTOM_BLOG_PAGES
            else "/blog/" + p["slug"] + "/")
    cover = (' style="background-image:url(' + "'" + esc(p["cover_url"]) + "'" + ');background-size:cover;background-position:center;"') if p.get("cover_url") else ""
    cat = esc((p.get("category") or "market").capitalize())
    return ('<a href="' + href + '" class="blog-card">'
            + '<div class="blog-card-img"' + cover + '></div>'
            + '<div class="blog-card-body"><div class="blog-card-tag">' + cat + '</div>'
            + '<div class="blog-card-title">' + esc(p.get("title") or "") + '</div>'
            + '<div class="blog-card-excerpt">' + esc(p.get("excerpt") or "") + '</div>'
            + '<div class="blog-card-meta">' + esc(p.get("readtime") or "") + '</div>'
            + '<span class="blog-card-link">Read More &rarr;</span></div></a>')


def _school_card(s):
    photo = (' style="background-image:url(' + "'" + esc(s["cover_url"]) + "'" + ')"') if s.get("cover_url") else ""
    tags = "".join('<span class="school-tag">' + esc(t) + "</span>"
                   for t in (s.get("grades"), s.get("curriculum"), s.get("languages")) if t)
    town = ('<div class="school-card-town">' + esc(s["town"]) + '</div>') if s.get("town") else ""
    return ('<a href="/school/' + s["slug"] + '/" class="school-card">'
            + '<div class="school-card-photo"' + photo + '></div>'
            + '<div class="school-card-body">' + town
            + '<div class="school-card-name">' + esc(s.get("name") or "") + '</div>'
            + '<div class="school-card-excerpt">' + esc(s.get("excerpt") or "") + '</div>'
            + ('<div class="school-card-tags">' + tags + '</div>' if tags else "") + '</div></a>')


def bake_roots(props, schools, posts, devs=None):
    inject("properties.html", "<!--BAKE:LISTINGS-->", "<!--/BAKE:LISTINGS-->",
           "".join(_prop_card(p) for p in props), "listings")
    # The shell used to hardcode "6 results" and "0 results"; keep both counts real.
    path = os.path.join(ROOT, "properties.html")
    with open(path, encoding="utf-8") as f:
        src = f.read()
    n = str(len(props))
    src, c1 = re.subn(r'<span id="visible-count">[^<]*</span>', '<span id="visible-count">' + n + "</span>", src)
    src, c2 = re.subn(r'<span id="list-count">[^<]*</span>', '<span id="list-count">' + n + "</span>", src)
    if c1 != 1 or c2 != 1:
        raise SystemExit("BUILD FAILED: result-count spans not found in properties.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)

    featured = [p for p in props if p.get("featured") and p.get("status") == "active"]
    inject("index.html", "<!--BAKE:FEATURED-->", "<!--/BAKE:FEATURED-->",
           "".join(_featured_card(p) for p in featured), "featured")
    inject("blog.html", "<!--BAKE:POSTS-->", "<!--/BAKE:POSTS-->",
           "".join(_blog_card(p) for p in posts), "posts")
    inject("schools.html", "<!--BAKE:SCHOOLS-->", "<!--/BAKE:SCHOOLS-->",
           "".join(_school_card(s) for s in schools), "schools")
    if devs:
        inject("developments.html", "<!--BAKE:DEVS-->", "<!--/BAKE:DEVS-->",
               "".join(_dev_card(d) for d in devs), "developments")

    # Hub ItemList structured data — lets crawlers and AI assistants read the
    # full catalog of school/community pages without executing any JS.
    def hub_itemlist(title, rows, path_prefix):
        return ld_script({
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": title,
            "numberOfItems": len(rows),
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "name": r.get("name") or "", "url": f"{SITE}/{path_prefix}/{r['slug']}/"}
                for i, r in enumerate(rows)
            ],
        })
    inject("schools.html", "<!--BAKE:SCHOOLS-LD-->", "<!--/BAKE:SCHOOLS-LD-->",
           hub_itemlist("International Schools in Guanacaste, Costa Rica", schools, "school"),
           "schools itemlist ld")
    if devs:
        inject("developments.html", "<!--BAKE:DEVS-LD-->", "<!--/BAKE:DEVS-LD-->",
               hub_itemlist("Gated Communities & Developments in Guanacaste, Costa Rica", devs, "development"),
               "developments itemlist ld")


# ── sitemap ──────────────────────────────────────────────────────

STATIC_PAGES = [
    ("/", "1.0", "weekly"),
    ("/properties.html", "0.9", "weekly"),
    ("/communities.html", "0.9", "weekly"),
    ("/buyers-guide.html", "0.9", "monthly"),
    ("/sellers-guide.html", "0.9", "monthly"),
    ("/how-i-sell.html", "0.8", "monthly"),
    ("/about.html", "0.8", "monthly"),
    ("/schools.html", "0.8", "monthly"),
    ("/developments.html", "0.9", "weekly"),
    ("/blog.html", "0.8", "weekly"),
    ("/blog-el-chante-tamarindo.html", "0.8", "monthly"),
    ("/playas-del-coco.html", "0.8", "monthly"),
    ("/potrero.html", "0.8", "monthly"),
    ("/las-catalinas.html", "0.8", "monthly"),
    ("/flamingo.html", "0.8", "monthly"),
    ("/conchal.html", "0.8", "monthly"),
    ("/playa-grande.html", "0.8", "monthly"),
    ("/tamarindo.html", "0.8", "monthly"),
    ("/langosta.html", "0.8", "monthly"),
    ("/avellanas.html", "0.8", "monthly"),
    ("/marbella.html", "0.8", "monthly"),
    ("/nosara.html", "0.8", "monthly"),
]


def write_sitemap(dynamic_urls):
    entries = []
    # Static pages get no lastmod — faking "modified today" on every build
    # teaches crawlers to ignore the field. Dynamic rows use real updated_at.
    for path, prio, freq in STATIC_PAGES:
        entries.append((path, None, prio, freq))
    entries.extend(dynamic_urls)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, mod, prio, freq in entries:
        xml.append("  <url>")
        xml.append(f"    <loc>{SITE}{path}</loc>")
        if mod:
            xml.append(f"    <lastmod>{mod}</lastmod>")
        xml.append(f"    <priority>{prio}</priority>")
        xml.append(f"    <changefreq>{freq}</changefreq>")
        xml.append("  </url>")
    xml.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(xml) + "\n")
    return len(entries)


# ── main ─────────────────────────────────────────────────────────

def validate(props, schools, posts):
    """Data-consistency audit: warns loudly, never blocks the deploy."""
    warn = []
    names = {}
    for p in props:
        n = p.get("name") or ""
        names[n] = names.get(n, 0) + 1
        m = re.search(r"(\d+)[- ]Bedroom", n)
        if m and p.get("beds") and int(float(p["beds"])) != int(m.group(1)):
            warn.append(f"{n[:42]}: name says {m.group(1)} bedrooms, beds field says {fmt_num(p['beds'])}")
        if p.get("size") and p.get("lot") and float(p["size"]) > float(p["lot"]):
            warn.append(f"{n[:42]}: built {p['size']} m2 exceeds lot {p['lot']} m2")
        if p.get("size") and float(p["size"]) > 1500:
            warn.append(f"{n[:42]}: built area {p['size']} m2 looks like square feet")
        if not (p.get("slug") or "").strip():
            warn.append(f"{n[:42]}: no slug yet (uuid URL in use)")
        if not p.get("price"):
            warn.append(f"{n[:42]}: missing price")
        if not (p.get("photos") or []):
            warn.append(f"{n[:42]}: no photos")
    for n, c in names.items():
        if c > 1:
            warn.append(f"duplicate listing name x{c}: {n[:42]}")
    for b in posts:
        if not b.get("meta_desc"):
            warn.append(f"post '{(b.get('title') or '')[:38]}': no meta description")
    for s in schools:
        if s.get("lat") is None:
            warn.append(f"school '{(s.get('name') or '')[:38]}': no map pin")
    if warn:
        print(f"AUDIT: {len(warn)} data warning(s) — review, build continues:")
        for w in warn:
            print("  WARN", w)


def main():
    for d in ("property", "school", "blog"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)

    def read(name):
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            return f.read()

    props = fetch("properties?select=*&status=in.(active,sold)&order=sort_order.asc,created_at.desc")
    schools = fetch("schools?select=*&status=eq.published&order=sort_order.asc")
    posts = fetch("blog_posts?select=*&status=eq.published&order=created_at.desc")
    try:
        devs = fetch("developments?select=*&status=eq.published&order=sort_order.asc")
    except Exception:
        devs = []  # table not created yet; site builds without development pages

    validate(props, schools, posts)

    urls = []
    urls += build_properties(read("property-detail.html"), props)
    urls += build_schools(read("school.html"), schools)
    urls += build_posts(read("blog-post.html"), posts)
    if devs:
        urls += build_developments(read("development.html"), devs)
    bake_roots(props, schools, posts, devs)
    import glob as _g
    for f in _g.glob(os.path.join(ROOT, "blog", "*", "index.html")) + _g.glob(os.path.join(ROOT, "school", "*", "index.html")):
        body = open(f, encoding="utf-8").read()
        marker = 'class="article-body"' if "/blog/" in f.replace(os.sep, "/") else 'class="sch-body"'
        if marker not in body:
            continue
        # Rendered content only — stop at the first script so the page's own
        # markdown-parser source can never false-positive the scan.
        seg = body.split(marker, 1)[1].split("<script", 1)[0]
        if re.search(r"\]\((https?:|mailto:)", seg) or "**" in seg:
            print(f"  WARN raw markdown leaked in {os.path.relpath(f, ROOT)}")
    total = write_sitemap(urls)

    n_prop = sum(1 for u in urls if u[0].startswith("/property/"))
    n_sch = sum(1 for u in urls if u[0].startswith("/school/"))
    n_blog = sum(1 for u in urls if u[0].startswith("/blog/"))
    print(f"build OK: {n_prop} properties, {n_sch} schools, {n_blog} posts, sitemap {total} urls")


if __name__ == "__main__":
    main()
