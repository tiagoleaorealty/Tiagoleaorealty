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
        r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
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


def write_page(rel_dir, content):
    d = os.path.join(ROOT, rel_dir)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)


def head_common(doc, title, desc, canon, og_title, og_desc, og_image):
    """Per-page head surgery shared by all three templates."""
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


def ld_script(obj, baked=True):
    attr = ' data-baked="1"' if baked else ""
    return f'<script type="application/ld+json"{attr}>\n{json.dumps(obj, indent=2, ensure_ascii=False)}\n</script>'


# ── properties ───────────────────────────────────────────────────

def build_properties(tpl):
    rows = fetch("properties?select=*&status=in.(active,sold)&order=sort_order.asc,created_at.desc")
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
        canon = f"{SITE}/property/{pid}/"
        desc = one_line(p.get("short_desc") or p.get("description") or f"{name} in {loc}.")
        title = f"{name} | Tiago Leao — Guanacaste Real Estate"
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
            ("stat-sqft", f"{int(float(p['size'])):,}" if p.get("size") else None),
            ("stat-lot", f"{int(float(p['lot'])):,}" if p.get("lot") else None),
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
        doc = sub_once(
            doc, r'<div class="features-grid" id="features-grid"></div>',
            f'<div class="features-grid" id="features-grid">{feats}</div>',
            "features",
        )
        if photos:
            doc = sub_once(
                doc, r'<span class="gallery-placeholder-label">Photo 1</span>',
                f'<img src="{esc(photos[0])}" alt="{esc(name)}" '
                'style="width:100%;height:100%;object-fit:cover;display:block;" />',
                "gallery main photo",
            )

        write_page(f"property/{pid}", doc)
        urls.append((f"/property/{pid}/", (p.get("updated_at") or TODAY)[:10], "0.7", "weekly"))
    return urls


# ── schools ──────────────────────────────────────────────────────

def build_schools(tpl):
    rows = fetch("schools?select=*&status=eq.published&order=sort_order.asc")
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
        doc = sub_once(
            doc, r"</head>", ld_script(ld) + "\n" + ld_script(crumbs) + "\n</head>", "school ld insert"
        )

        write_page(f"school/{slug}", doc)
        urls.append((f"/school/{slug}/", (s.get("updated_at") or TODAY)[:10], "0.6", "monthly"))
    return urls


# ── blog posts ───────────────────────────────────────────────────

def build_posts(tpl):
    rows = fetch("blog_posts?select=*&status=eq.published&order=created_at.desc")
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

        doc = head_common(tpl, f"{title_txt} | Tiago Leao Real Estate", desc, canon, title_txt, desc, og_image)

        upd = (p.get("updated_at") or p.get("created_at") or TODAY)[:10]
        try:
            y, m, d = (int(x) for x in upd.split("-"))
            nice_date = f"{date(y, m, d):%B} {d}, {y}"
        except ValueError:
            nice_date = upd
        byline = (f"By Tiago Leao &middot; KRAIN Luxury Real Estate &middot; Updated {nice_date}"
                  + (f" &middot; {esc(p['readtime'])}" if p.get("readtime") else ""))
        baked = f"""<a href="blog.html" class="article-back">&larr; All Articles</a>
    <div class="article-tag">{esc((p.get("category") or "guide").capitalize())}</div>
    <h1 class="article-title">{esc(title_txt)}</h1>
    <div class="article-byline">{byline}</div>
    <div class="article-body">
      {parse_body(p.get("body"))}
      <div class="article-cta"><p>Interested in learning more?</p><a href="index.html#form-section">Get in Touch &rarr;</a></div>
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
            "author": {"@type": "Person", "name": "Tiago Leao", "url": f"{SITE}/about.html"},
            "publisher": {"@type": "RealEstateAgent", "name": "Tiago Leao Real Estate", "url": SITE},
            "mainEntityOfPage": canon,
        }
        doc = sub_once(doc, r"</head>", ld_script(ld) + "\n</head>", "article ld insert")

        write_page(f"blog/{slug}", doc)
        urls.append((f"/blog/{slug}/", upd, "0.7", "monthly"))
    return urls


# ── sitemap ──────────────────────────────────────────────────────

STATIC_PAGES = [
    ("/", "1.0", "weekly"),
    ("/properties.html", "0.9", "weekly"),
    ("/communities.html", "0.9", "weekly"),
    ("/buyers-guide.html", "0.9", "monthly"),
    ("/sellers-guide.html", "0.9", "monthly"),
    ("/about.html", "0.8", "monthly"),
    ("/schools.html", "0.8", "monthly"),
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
    for path, prio, freq in STATIC_PAGES:
        entries.append((path, TODAY, prio, freq))
    entries.extend(dynamic_urls)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, mod, prio, freq in entries:
        xml.append("  <url>")
        xml.append(f"    <loc>{SITE}{path}</loc>")
        xml.append(f"    <lastmod>{mod}</lastmod>")
        xml.append(f"    <priority>{prio}</priority>")
        xml.append(f"    <changefreq>{freq}</changefreq>")
        xml.append("  </url>")
    xml.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(xml) + "\n")
    return len(entries)


# ── main ─────────────────────────────────────────────────────────

def main():
    for d in ("property", "school", "blog"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)

    def read(name):
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            return f.read()

    urls = []
    urls += build_properties(read("property-detail.html"))
    urls += build_schools(read("school.html"))
    urls += build_posts(read("blog-post.html"))
    total = write_sitemap(urls)

    n_prop = sum(1 for u in urls if u[0].startswith("/property/"))
    n_sch = sum(1 for u in urls if u[0].startswith("/school/"))
    n_blog = sum(1 for u in urls if u[0].startswith("/blog/"))
    print(f"build OK: {n_prop} properties, {n_sch} schools, {n_blog} posts, sitemap {total} urls")


if __name__ == "__main__":
    main()
