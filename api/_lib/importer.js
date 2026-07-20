// ============================================================
// KRAIN → SoldByTiago importer: shared server-side library.
//
// Runs inside Vercel Node functions only (never shipped to the client).
// Contains: URL safety checks (allowlist + SSRF guards), the polite
// fetcher, and the source-adapter registry. Adapters extract listing
// data from pages the importing user is authorized to republish —
// the tool only ever fetches the single URL the admin submits.
//
// No secrets live here: the Supabase key used for auth verification is
// the public anon key, and all database/storage writes happen in the
// admin's browser under their own authenticated session (RLS-enforced).
// ============================================================
'use strict';

const dns = require('dns').promises;
const net = require('net');

// ── configuration ────────────────────────────────────────────
const SB_URL = 'https://xjliwfmugylwxlrwyvmh.supabase.co';
const SB_ANON_KEY = 'sb_publishable_YHOe_eAJzuWpzbFD_tO-4A_vuvnSHum'; // public by design

// Hosts the importer may fetch LISTING PAGES from.
const PAGE_HOSTS = new Set([
  'krainrealestate.com',
  'www.krainrealestate.com',
  'mls.propertyshelf.com',
  'www.propertyshelf.com',
]);

// Hosts the importer may download IMAGES from (listing-media CDNs).
const IMAGE_HOSTS = new Set([
  'media-production.lp-cdn.com', // Luxury Presence CDN (KRAIN's media)
]);

const FETCH_TIMEOUT_MS = 15000;
const IMAGE_TIMEOUT_MS = 20000;
const MAX_HTML_BYTES = 3 * 1024 * 1024;   // 3 MB page cap
const MAX_IMAGE_BYTES = 4 * 1024 * 1024;  // 4 MB per image (Vercel response cap ~4.5 MB)
const MAX_REDIRECTS = 3;
const UA = 'SoldByTiago-Importer/1.0 (authorized listing import; contact: tiago@soldbytiago.com)';

// Unit conversion constants (exact where defined, high precision otherwise).
const SQFT_PER_SQM = 10.7639104167;   // 1 m² = 10.7639104167 ft²
const SQM_PER_ACRE = 4046.8564224;    // exact (international acre)
const SQM_PER_HECTARE = 10000;        // exact

// ── auth: verify the caller's Supabase session server-side ───
// The admin UI sends the logged-in user's access token; we confirm it
// against Supabase Auth. Anonymous callers are rejected, so the fetch
// proxy can't be used by anyone who isn't signed in to the admin.
async function verifyAdminToken(token) {
  if (!token || typeof token !== 'string' || token.length < 20) return null;
  try {
    const r = await fetch(`${SB_URL}/auth/v1/user`, {
      headers: { apikey: SB_ANON_KEY, Authorization: `Bearer ${token}` },
      signal: AbortSignal.timeout(8000),
    });
    if (!r.ok) return null;
    const u = await r.json();
    return u && u.id ? { id: u.id, email: u.email || '' } : null;
  } catch {
    return null;
  }
}

// ── crude per-instance rate limiting (best effort) ───────────
const rateBuckets = new Map();
function rateLimit(key, max, windowMs) {
  const now = Date.now();
  const arr = (rateBuckets.get(key) || []).filter((t) => now - t < windowMs);
  if (arr.length >= max) return false;
  arr.push(now);
  rateBuckets.set(key, arr);
  return true;
}

// ── SSRF-safe URL validation ─────────────────────────────────
function isPrivateIp(ip) {
  if (net.isIPv6(ip)) {
    const low = ip.toLowerCase();
    return low === '::1' || low.startsWith('fe80') || low.startsWith('fc') ||
           low.startsWith('fd') || low.startsWith('::ffff:127.') || low === '::';
  }
  const p = ip.split('.').map(Number);
  return p[0] === 10 || p[0] === 127 || p[0] === 0 ||
         (p[0] === 172 && p[1] >= 16 && p[1] <= 31) ||
         (p[0] === 192 && p[1] === 168) ||
         (p[0] === 169 && p[1] === 254) ||
         p[0] >= 224;
}

async function validateUrl(rawUrl, allowedHosts) {
  let u;
  try { u = new URL(String(rawUrl)); } catch { return { ok: false, error: 'That is not a valid URL.' }; }
  if (u.protocol !== 'https:') return { ok: false, error: 'Only https:// URLs are supported.' };
  if (u.username || u.password) return { ok: false, error: 'URLs with credentials are not allowed.' };
  const host = u.hostname.toLowerCase();
  if (net.isIP(host)) return { ok: false, error: 'IP-address URLs are not allowed.' };
  if (!allowedHosts.has(host)) {
    return { ok: false, error: `Domain "${host}" is not on the importer's approved source list.` };
  }
  try {
    const addrs = await dns.lookup(host, { all: true });
    if (!addrs.length || addrs.some((a) => isPrivateIp(a.address))) {
      return { ok: false, error: 'Source host failed the network safety check.' };
    }
  } catch {
    return { ok: false, error: 'Could not resolve the source host.' };
  }
  return { ok: true, url: u };
}

// Fetch with manual redirect handling so every hop is re-validated
// against the allowlist, plus timeout and size caps.
async function safeFetch(url, allowedHosts, { timeoutMs, maxBytes, accept }) {
  let current = url;
  for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
    const res = await fetch(current.href, {
      redirect: 'manual',
      headers: { 'user-agent': UA, accept: accept || '*/*' },
      signal: AbortSignal.timeout(timeoutMs),
    });
    if (res.status >= 300 && res.status < 400) {
      const loc = res.headers.get('location');
      if (!loc) return { ok: false, status: res.status, error: 'Redirect with no destination.' };
      const nextUrl = new URL(loc, current);
      const check = await validateUrl(nextUrl.href, allowedHosts);
      if (!check.ok) return { ok: false, status: res.status, error: `Blocked redirect: ${check.error}` };
      current = check.url;
      continue;
    }
    if (!res.ok) return { ok: false, status: res.status, error: `Source responded with HTTP ${res.status}.` };
    const lenHeader = Number(res.headers.get('content-length') || 0);
    if (lenHeader && lenHeader > maxBytes) {
      return { ok: false, status: 200, error: `Response too large (${(lenHeader / 1048576).toFixed(1)} MB).` };
    }
    const reader = res.body.getReader();
    const chunks = [];
    let total = 0;
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.length;
      if (total > maxBytes) {
        reader.cancel().catch(() => {});
        return { ok: false, status: 200, error: `Response exceeded the ${(maxBytes / 1048576).toFixed(0)} MB limit.` };
      }
      chunks.push(value);
    }
    return {
      ok: true,
      status: res.status,
      contentType: (res.headers.get('content-type') || '').split(';')[0].trim().toLowerCase(),
      body: Buffer.concat(chunks),
      finalUrl: current.href,
    };
  }
  return { ok: false, status: 0, error: 'Too many redirects.' };
}

// ── small HTML helpers (extraction emits plain text only) ────
function decodeEntities(s) {
  return String(s || '')
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&nbsp;/g, ' ')
    .replace(/&mdash;/g, '—').replace(/&ndash;/g, '–').replace(/&rsquo;/g, '’')
    .replace(/&lsquo;/g, '‘').replace(/&ldquo;/g, '“').replace(/&rdquo;/g, '”');
}
function stripTags(s) {
  return decodeEntities(String(s || '')
    .replace(/<\s*(script|style)[^>]*>[\s\S]*?<\/\s*\1\s*>/gi, ' ')
    .replace(/<br\s*\/?\s*>/gi, '\n')
    .replace(/<\/(p|div|li|h[1-6])>/gi, '\n')
    .replace(/<[^>]+>/g, ' '))
    .replace(/[ \t]+/g, ' ')
    .replace(/ *\n */g, '\n')
    .trim();
}
// Extract the inner HTML of the first ELEMENT carrying `className` in its
// class attribute (the class name also appears in inline <style> blocks, so
// we must match a real opening tag), walking nested same-name tags so we
// stop at the true closing tag.
function balancedBlock(doc, className) {
  const tagRe = new RegExp(`<([a-z][a-z0-9]*)\\b[^>]*class="[^"]*\\b${className}\\b[^"]*"[^>]*>`, 'i');
  const m = tagRe.exec(doc);
  if (!m) return null;
  const tag = m[1].toLowerCase();
  const start = m.index + m[0].length;
  let depth = 1;
  const walkRe = new RegExp(`<${tag}\\b[^>]*>|</${tag}\\s*>`, 'gi');
  walkRe.lastIndex = start;
  let w;
  while ((w = walkRe.exec(doc))) {
    depth += w[0][1] === '/' ? -1 : 1;
    if (depth === 0) return doc.slice(start, w.index);
  }
  return null;
}
function meta(doc, prop) {
  const re = new RegExp(`<meta[^>]+(?:property|name)="${prop}"[^>]+content="([^"]*)"`, 'i');
  const alt = new RegExp(`<meta[^>]+content="([^"]*)"[^>]+(?:property|name)="${prop}"`, 'i');
  const m = doc.match(re) || doc.match(alt);
  return m ? decodeEntities(m[1]) : '';
}

// ── numeric parsing / unit handling ──────────────────────────
function parseMoney(s) {
  const m = String(s || '').match(/([$€£₡])\s*([\d,]+(?:\.\d+)?)/);
  if (!m) return null;
  const currency = { $: 'USD', '€': 'EUR', '£': 'GBP', '₡': 'CRC' }[m[1]] || 'USD';
  return { amount: Number(m[2].replace(/,/g, '')), currency, display: m[0].replace(/\s+/g, '') };
}
function parseAreaValue(s) {
  // "3,500 Sq.Ft." | "1,300 m²" | "0.53 Acres" | "1.2 ha"
  const m = String(s || '').replace(/,/g, '').match(/([\d.]+)\s*(sq\.?\s*ft|sqft|square\s*feet|ft²|m²|m2|sq\.?\s*m|acres?|ac\b|hectares?|ha\b)/i);
  if (!m) return null;
  const v = Number(m[1]);
  const unit = m[2].toLowerCase().replace(/\s|\./g, '');
  if (/^(sqft|squarefeet|ft²|sqf?t?)$/.test(unit) || unit.startsWith('sqft') || unit.startsWith('ft')) return { value: v, unit: 'sqft' };
  if (unit.startsWith('m')) return { value: v, unit: 'sqm' };
  if (unit.startsWith('ac')) return { value: v, unit: 'acre' };
  if (unit.startsWith('h')) return { value: v, unit: 'hectare' };
  return null;
}
function toSqm(a) {
  if (!a) return null;
  switch (a.unit) {
    case 'sqm': return a.value;
    case 'sqft': return a.value / SQFT_PER_SQM;
    case 'acre': return a.value * SQM_PER_ACRE;
    case 'hectare': return a.value * SQM_PER_HECTARE;
    default: return null;
  }
}

// ══════════════════════════════════════════════════════════════
//  ADAPTERS
//  Shared interface: { id, label, canHandle(url), supported,
//                      extract(html, url) -> normalized listing }
// ══════════════════════════════════════════════════════════════

// ── KRAIN brokerage/exclusive pages (Luxury Presence platform) ──
const krainLp = {
  id: 'krain-lp',
  label: 'KRAIN brokerage listing (krainrealestate.com/properties/…)',
  supported: true,
  canHandle(u) {
    return /(^|\.)krainrealestate\.com$/.test(u.hostname) && /^\/properties\/[^/]+\/?$/.test(u.pathname);
  },
  extract(html, url) {
    const doc = html;
    const missing = [];
    const flags = [];

    // Title / name
    const h1m = doc.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
    const fullTitle = h1m ? stripTags(h1m[1]).replace(/\s+/g, ' ').trim() : meta(doc, 'og:title');
    const name = (fullTitle.split('|')[0] || '').trim();

    // Spec table: sectioned <li><strong>key</strong><span class="feature">value</span></li>
    const sections = {};
    const pairs = {};
    const secRe = /<h3 class="features-amenities-title">([^<]*)<\/h3>\s*<ul class="features-amenities-list">([\s\S]*?)<\/ul>/g;
    let sm;
    while ((sm = secRe.exec(doc))) {
      const secName = decodeEntities(sm[1]).trim();
      sections[secName] = {};
      const liRe = /<li><strong>([^<]*)<\/strong><span class="feature">([^<]*)<\/span><\/li>/g;
      let lm;
      while ((lm = liRe.exec(sm[2]))) {
        const k = decodeEntities(lm[1]).trim();
        const v = decodeEntities(lm[2]).trim();
        sections[secName][k] = v;
        pairs[k.toLowerCase()] = v;
      }
    }
    const pair = (...keys) => {
      for (const k of keys) if (pairs[k.toLowerCase()] != null) return pairs[k.toLowerCase()];
      return null;
    };

    // Price: any Financial-section (or global) key containing "price" with a money value.
    let price = null, priceLabel = null;
    for (const [k, v] of Object.entries(pairs)) {
      if (/price/i.test(k)) {
        const p = parseMoney(v);
        if (p) { price = p; priceLabel = k; break; }
      }
    }
    if (!price) {
      const p = parseMoney(meta(doc, 'og:description'));
      if (p) { price = p; priceLabel = 'og:description'; flags.push('Price taken from page meta description — verify.'); }
    }
    if (!price) missing.push('price');

    // Beds / baths
    const num = (s) => (s == null || s === '' ? null : Number(String(s).replace(/[^\d.]/g, '')) || null);
    const beds = num(pair('total bedrooms', 'bedrooms', 'beds'));
    const bathsFull = num(pair('full bathrooms', 'full bathroom'));
    const bathsHalf = num(pair('half bathrooms', 'half bathroom'));
    const bathsTotal = num(pair('total bathrooms', 'bathrooms'));
    if (beds == null) missing.push('bedrooms');
    if (bathsTotal == null && bathsFull == null) missing.push('bathrooms');
    if (bathsTotal != null && bathsFull != null) {
      const expected = bathsFull + (bathsHalf || 0);
      if (expected !== bathsTotal) flags.push(`Bathroom counts disagree: full ${bathsFull} + half ${bathsHalf || 0} ≠ total ${bathsTotal}.`);
    }

    // Areas — generic: any pair mentioning living/lot/area/acreage
    const area = { pairs: {}, built_m2: null, lot_m2: null };
    for (const [k, v] of Object.entries(pairs)) {
      if (/living|interior.*(space|area)|lot|acre|land\s*(size|area)|total\s*area|construction/i.test(k)) {
        const parsed = parseAreaValue(v);
        area.pairs[k] = { raw: v, parsed };
        if (parsed) {
          const sqm = toSqm(parsed);
          if (/living|interior|construction/i.test(k) && area.built_m2 == null) area.built_m2 = sqm;
          if (/lot|land|acre/i.test(k) && area.lot_m2 == null) area.lot_m2 = sqm;
        }
      }
    }
    if (area.built_m2 == null) missing.push('built area');
    if (area.lot_m2 == null) missing.push('lot area');

    // Description: balanced block of .property-description__main
    let description = '';
    const descHtml = balancedBlock(doc, 'property-description__main');
    if (descHtml) {
      description = stripTags(descHtml).replace(/\n{3,}/g, '\n\n').trim();
    }
    if (!description) missing.push('description');

    // Agent
    const agentBlock = balancedBlock(doc, 'property-agent-cta-info') || '';
    const agentM = agentBlock.match(/<h3 class="name">[\s\S]*?>([^<]+)</);
    const agent = agentM ? decodeEntities(agentM[1]).trim() : null;
    if (!agent) missing.push('listing agent');

    // Brokerage from the site's own organization JSON-LD (not invented).
    let brokerage = null;
    const orgM = doc.match(/"@type":\s*"RealEstateAgent"[\s\S]{0,400}?"name":\s*"([^"]+)"/);
    if (orgM) brokerage = decodeEntities(orgM[1]);

    // Coordinates from the property map element
    let lat = null, lng = null;
    const mapTag = doc.match(/<[^>]*property-map__canvas[^>]*>/);
    if (mapTag) {
      const latM = mapTag[0].match(/data-lat="([-\d.]+)"/);
      const lngM = mapTag[0].match(/data-lng="([-\d.]+)"/);
      if (latM && lngM) { lat = Number(latM[1]); lng = Number(lngM[1]); }
    }
    if (lat == null) missing.push('coordinates');

    // Status: LP pages rarely render it as text; look for a badge, else null.
    let statusRaw = null;
    const statusM = doc.match(/class="[^"]*(?:property|listing)-status[^"]*"[^>]*>\s*([^<]{2,30}?)\s*</i);
    if (statusM) statusRaw = decodeEntities(statusM[1]).trim();
    if (!statusRaw) missing.push('status');

    // Video / virtual tour: only concrete embeds, never guessed.
    const vidM = doc.match(/<iframe[^>]+src="(https:\/\/(?:www\.)?(?:youtube\.com\/embed|player\.vimeo\.com\/video)\/[^"]+)"/);
    const tourM = doc.match(/https:\/\/my\.matterport\.com\/show\/[^"'\s]+/);

    // Images: lp-cdn media UUIDs in order of first appearance.
    // Excluded: the brokerage logo/photo from org JSON-LD and the agent portrait.
    const exclude = new Set();
    const orgBlock = doc.match(/"@type":\s*"RealEstateAgent"[\s\S]{0,1200}/);
    if (orgBlock) for (const mm of orgBlock[0].matchAll(/media\/([a-f0-9-]{36})/g)) exclude.add(mm[1]);
    for (const mm of doc.matchAll(/<img[^>]+class="[^"]*portrait[^"]*"[^>]*>/g)) {
      for (const um of mm[0].matchAll(/media\/([a-f0-9-]{36})/g)) exclude.add(um[1]);
    }
    const heroUuid = (meta(doc, 'og:image').match(/media\/([a-f0-9-]{36})/) || [])[1] || null;
    const seen = new Set();
    const images = [];
    for (const mm of doc.matchAll(/https:\/\/media-production\.lp-cdn\.com\/(?:cdn-cgi\/image\/[^"'\s\\)]*?\/https:\/\/media-production\.lp-cdn\.com\/)?media\/([a-f0-9-]{36})/g)) {
      const uuid = mm[1];
      if (seen.has(uuid) || exclude.has(uuid)) continue;
      seen.add(uuid);
      images.push(uuid);
    }
    if (heroUuid && seen.has(heroUuid)) {
      images.splice(images.indexOf(heroUuid), 1);
      images.unshift(heroUuid);
    }
    const mkImg = (uuid) => ({
      uuid,
      original_url: `https://media-production.lp-cdn.com/media/${uuid}`,
      full_url: `https://media-production.lp-cdn.com/cdn-cgi/image/format=jpeg,quality=90,fit=scale-down,width=2560/https://media-production.lp-cdn.com/media/${uuid}`,
      preview_url: `https://media-production.lp-cdn.com/cdn-cgi/image/format=auto,quality=70,fit=scale-down,width=480/https://media-production.lp-cdn.com/media/${uuid}`,
    });

    // Source listing UUID (Luxury Presence page element id)
    const idM = doc.match(/pageQueryVariables:\s*\{"property":\{"id":"([a-f0-9-]{36})"/) ||
                doc.match(/pageElementId:\s*"([a-f0-9-]{36})"/);

    // Feature lists → flat chips
    const splitList = (s) => (s ? s.split(/,\s*/).map((x) => x.trim()).filter(Boolean) : []);
    const interior = splitList(pair('other interior features'));
    const exterior = splitList(pair('other exterior features'));
    const appliances = splitList(pair('appliances'));

    const typeRaw = pair('type');
    const typeMap = { residential: 'home', house: 'home', home: 'home', condominium: 'condo', condo: 'condo', villa: 'villa', land: 'land', lot: 'land', commercial: 'commercial' };
    const typeMapped = typeRaw ? (typeMap[typeRaw.toLowerCase()] || null) : null;
    if (!typeRaw) missing.push('property type');
    else if (!typeMapped) flags.push(`Source type "${typeRaw}" has no direct site equivalent — choose manually.`);

    return {
      source: {
        provider: 'krain-lp',
        provider_label: 'KRAIN (Luxury Presence)',
        url: url.href,
        slug: url.pathname.split('/').filter(Boolean).pop(),
        listing_uuid: idM ? idM[1] : null,
        mls_id: pair('mls® id', 'mls id', 'mls#') || null,
        agent, brokerage,
        updated_at: null, // not exposed by source pages
        fetched_at: new Date().toISOString(),
      },
      listing: {
        name: name || null,
        full_title: fullTitle || null,
        price,
        price_label: priceLabel,
        status_raw: statusRaw,
        type_raw: typeRaw || null,
        type_mapped: typeMapped,
        beds,
        baths_full: bathsFull,
        baths_half: bathsHalf,
        baths_total: bathsTotal,
        year_built: num(pair('year built')),
        stories: num(pair('stories')),
        garage_spaces: num(pair('garage space', 'garage spaces')),
        pool: pair('pool'),
        parking: pair('parking'),
        view: pair('view description', 'view'),
        water_source: pair('water source'),
        roof: pair('roof'),
        air_conditioning: pair('air conditioning'),
        flooring: pair('flooring'),
        kitchen: pair('kitchen'),
        laundry: pair('laundry room'),
        neighborhood: pair('neighborhood') || null,
        hoa_amount: parseMoney(pair('hoa fees', 'hoa', 'association fee') || '') || null,
        hoa_frequency: null,
        furnished: pair('furnished'),
        appliances, interior_features: interior, exterior_features: exterior,
        area,
        description,
        lat, lng,
        video_url: vidM ? vidM[1] : null,
        tour_url: tourM ? tourM[0] : null,
        meta_title: meta(doc, 'og:title') || null,
        meta_description: meta(doc, 'og:description') || null,
        spec_sections: sections,
      },
      images: images.map(mkImg),
      missing,
      flags,
    };
  },
};

// ── KRAIN home-search / IDX pages: intentionally NOT auto-imported ──
// These are the shared MLS/IDX feed — mostly OTHER brokerages' listings that
// KRAIN may display under IDX rules, sourced from MLSs (e.g. Omni MLS) whose
// licence typically restricts the data to "personal, non-commercial use".
// Republishing them as content on soldbytiago.com is a different right from
// importing KRAIN's own listings, and the pages are behind bot protection
// with no public slug lookup — so this importer does not pull them
// automatically. Use the listing's own krainrealestate.com/properties/… page
// when it is KRAIN's, or enter a listing you have written permission for by
// hand. See KRAIN-IMPORTER.md § IDX / MLS listings.
const krainIdx = {
  id: 'krain-idx',
  label: 'KRAIN home-search (shared MLS/IDX feed)',
  supported: false,
  reason: 'This is a shared MLS/IDX search result, not a KRAIN listing page. These are often other brokerages’ listings under MLS rules that limit them to personal, non-commercial use, so the importer will not republish them automatically. If it is KRAIN’s own listing, import its krainrealestate.com/properties/… page instead; if you have written permission for a specific third-party listing, add it by hand.',
  canHandle(u) {
    return /(^|\.)krainrealestate\.com$/.test(u.hostname) && /^\/home-search(\/|$)/.test(u.pathname);
  },
};

// ── Propertyshelf: recognized, not yet supported ──
const propertyshelf = {
  id: 'propertyshelf',
  label: 'Propertyshelf MLS',
  supported: false,
  reason: 'This KRAIN listing format is not currently supported. Propertyshelf pages will be added once a sample listing and authorization are confirmed.',
  canHandle(u) {
    return /(^|\.)propertyshelf\.com$/.test(u.hostname);
  },
};

const ADAPTERS = [krainLp, krainIdx, propertyshelf];

function findAdapter(url) {
  return ADAPTERS.find((a) => a.canHandle(url)) || null;
}

module.exports = {
  PAGE_HOSTS, IMAGE_HOSTS,
  FETCH_TIMEOUT_MS, IMAGE_TIMEOUT_MS, MAX_HTML_BYTES, MAX_IMAGE_BYTES,
  SQFT_PER_SQM, SQM_PER_ACRE, SQM_PER_HECTARE,
  verifyAdminToken, rateLimit, validateUrl, safeFetch,
  findAdapter, ADAPTERS,
  _test: { stripTags, decodeEntities, parseMoney, parseAreaValue, toSqm, balancedBlock, meta },
};
