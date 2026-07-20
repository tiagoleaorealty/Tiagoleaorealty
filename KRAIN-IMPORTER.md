# KRAIN → SoldByTiago Property Importer

Private admin tool that imports **approved, authorized** KRAIN listings into the
existing SoldByTiago property system. It fetches only the single URL the admin
submits, imports nothing silently, publishes nothing without explicit review +
an authorization confirmation, and never modifies the public website design.

**URL:** `/admin/import-property/` (rewrites to `admin-import.html`). Login = the
same Supabase Auth account as `admin.html`.

---

## 1. Architecture summary

```
Admin browser (admin-import.html, Supabase Auth session)
   │  POST /api/import-fetch {url}          ── Vercel Node function
   │     └─ verifies the Supabase session token server-side,
   │        validates URL (https, domain allowlist, DNS/SSRF guard,
   │        re-validated redirects, 15 s timeout, 3 MB cap),
   │        runs the matching source adapter → normalized JSON
   │  POST /api/import-image {url}          ── same guards, image hosts only,
   │        MIME + size checks → returns bytes
   │
   ├─ ALL persistence happens in the browser under the logged-in user's
   │  session (RLS-enforced; no service keys anywhere):
   │     property_imports  (private drafts / audit / permission records)
   │     properties        (the existing public table — publish step only)
   │     storage 'photos'  (originals + optimized display copies)
   │
   └─ Page/canonical/OG/JSON-LD/sitemap generation stays 100 % in the
      existing build.py Vercel build — the importer writes a normal
      properties row and reminds you to trigger a site build.
```

Existing system (audit, 2026-07-19): static HTML/CSS/JS on Vercel · Supabase
(Postgres + Storage, RLS locked: anon = read-only, writes require Supabase
Auth) · `build.py` bakes `/property/<slug>/` pages, canonicals, Open Graph,
JSON-LD and `sitemap.xml` on every deploy · admin.html manages properties.
**No duplicate property database was created** — imports live in one new
private table and publishing writes the normal `properties` row.

## 2. Property-schema audit → field map

| properties column | Public-page use | Type | Required | KRAIN source field | Validation |
|---|---|---|---|---|---|
| name | H1, cards, title, JSON-LD | text | yes | `<h1>` first `\|` segment | non-empty (blocking) |
| slug | clean URL `/property/<slug>/` | text unique | yes | generated: `slugify(name+location)`, kept stable on update | unique (auto `-suffix` retry) |
| price | display everywhere; JSON-LD offers parses digits | text | yes | spec pair whose key contains "price" (`Sales Price`, `Reduced Price`) | non-empty (blocking); non-USD → warning, never auto-converted |
| type | filters, meta | enum home/condo/villa/land/commercial | yes | `Type` pair mapped (Residential→home, Condominium→condo, …) | must be chosen (blocking) |
| status | badges, filters, baking | enum active/pending/sold | yes | **never guessed** — LP pages don't render it as text | must be chosen (blocking) |
| location | cards, JSON-LD address, **community-page matcher** | text | yes | `Neighborhood` pair | non-empty (blocking) |
| address | property page | text | no | not on LP pages | — |
| beds | cards, filters | numeric | residential | `total bedrooms` | blocking if residential and empty |
| baths | cards | numeric | residential | `full + 0.5×half` (or total) | blocking if residential and empty; full+half≠total → blocking contradiction |
| size (m²) | page shows m² + ft² | numeric | no | area pair (living/interior) via unit conversion | >1500 m² warn (sqft suspicion); >lot warn; =lot warn |
| lot (m²) | page shows m² + ft² + acres | numeric | no | area pair (lot/land/acre) | conversion shown source+normalized |
| short_desc | cards one-liner ≤120 | text | no | — (admin writes) | info if empty |
| description | page body | text | yes | `.property-description__main` plain text | blocking if empty; source-text use requires description authorization; investment-claims regex → warning |
| features | chips | text[] | no | interior+exterior features, pool, view, parking | — |
| photos | gallery; photos[0] = hero | text[] | yes ≥1 | lp-cdn gallery (originals `media/<uuid>`) | hero required (blocking); copied-to-own-storage required |
| lat/lng | map pin | float | no | `.property-map__canvas` data-lat/lng | info if missing (map hides) |
| featured / sort_order | homepage / ordering | bool/int | auto | new imports: featured=false, sort_order=max+1 (appended) | — |
| walk_score, beach_minutes, beach_mode, airport_minutes | "around" tiles (null hides) | numeric/text | no | not provided by KRAIN — manual only | distances must not be invented |

KRAIN fields with **no public column** (MLS ID, source listing UUID, source URL,
listing agent, brokerage, year built, HOA, garage, stories, view, water source,
appliances, permission record, snapshots) are stored privately in
`property_imports` — visible in the importer, never rendered publicly.

## 3. Source-adapter design

`api/_lib/importer.js` exports an adapter registry. Each adapter:

```
{ id, label, supported,
  canHandle(url)     → routes by hostname + path shape
  extract(html, url) → { source, listing, images, missing, flags } }
```

(fetchSource/validateSource live in the shared `validateUrl`/`safeFetch`;
normalizeData is part of `extract`; `source` is the returned metadata.)

| Adapter | Handles | Status |
|---|---|---|
| `krain-lp` | `krainrealestate.com/properties/<slug>` (Luxury Presence SSR pages; lp-cdn media) | **fully supported** |
| `manual` | no fetch — admin-entered listing under written permission | **supported** (see § Manual entry) |
| `krain-idx` | `krainrealestate.com/home-search/…` | **intentionally not auto-imported** — shared MLS/IDX feed (see § IDX / MLS listings) |
| `propertyshelf` | `*.propertyshelf.com` | recognized → same message (host unreachable during development; needs a sample listing) |
| anything else on allowlisted hosts | — | same message |
| non-allowlisted host | — | rejected before any fetch |

Unsupported ⇒ **no partial import, ever** — a page yielding neither a name nor
images is refused with the standard message.

### IDX / MLS listings (`/home-search/…`) — why they are not auto-imported

Investigated 2026-07-20 against a live example (Reserva Conchal Carao T3-3,
`…/home-search/listings/8585740543063911494-Reserva-Conchal-Carao-T3-3-…`).
Two independent reasons, either one sufficient, to keep these out of the
automatic importer:

1. **Rights.** These are shared **MLS/IDX** search results, not KRAIN's own
   listing pages. The example belongs to **Gabriel Araya, Coldwell Banker
   Flamingo** (a different brokerage) and is sourced from **Omni MLS**; the
   feed's own disclaimer states the data is *"intended solely for personal,
   non-commercial use… not to be utilized for any other purposes except to
   identify potential properties for purchase."* KRAIN's right to **display**
   these under IDX is not a right for Tiago to **republish** them as content on
   a separate commercial site. Importing KRAIN's own exclusives (the `/properties/`
   pages) is a different matter and is fully supported.
2. **Access.** The `/home-search/` detail pages are behind Cloudflare's bot
   challenge (HTTP 403 server-side even with full browser headers), and the
   underlying data API (`POST /federation`, GraphQL — reachable server-side)
   has **no public slug→listing lookup**: `mlsListing(displayId, feedIds)`
   needs the internal UUID, which appears only inside the bot-protected page's
   `__NEXT_DATA__`; the browsable `mlsListings` index has no `slug`/`search`
   filter and does not contain every listing; introspection is disabled.
   Pulling these automatically would require defeating the bot challenge —
   which this tool will not do, and which would itself breach the site/MLS
   terms.

**Legitimate paths instead:** (a) if the listing is KRAIN's own, it also exists
at a `krainrealestate.com/properties/<slug>` URL — import that; (b) for a
specific third-party listing Tiago has **written permission** to feature, use
**Manual entry (written permission)** in the importer (below). The importer
will **not** be turned into an automated MLS/IDX republisher.

### Manual entry (written permission) mode

Added 2026-07-20 for the "I have written permission" case. A **＋ Enter a
listing manually** button on the importer's list view opens the same review
workspace with empty fields — nothing is fetched from any source. The admin
types the listing details (with the same m²/ft²/acre conversion helpers and
the same blocking/warning/info validation) and **uploads the photos they are
authorized to use** (reusing the browser-side compress + Supabase Storage
pipeline; the source CDN is never contacted). The permission scope defaults to
`written_permission`, and manual entries carry **extra required compliance
gates** on top of the normal ones: a permission note (who granted permission,
when), the **listing broker/agent attribution** (whose listing it is), and
description-republication authorization when a description is present. Publish,
duplicate detection, draft/audit history and the clean-URL/sitemap bake are all
identical to a fetched import; "Check source for changes" and the source-text
tab are hidden (there is no source page). This gives a proper authorized-import
workflow for permitted third-party listings without scraping the MLS/IDX feed.

`krain-lp` extraction sources (verified against two live fixtures):
`<h1>`, sectioned spec list `features-amenities-list` (`<li><strong>key</strong>
<span class="feature">value</span>`), `.property-description__main` (balanced-tag
walk; class also appears in inline CSS, handled), `.property-agent-cta-info h3.name`,
`.property-map__canvas[data-lat|data-lng]`, org JSON-LD (brokerage name),
`og:image` (hero), lp-cdn `media/<uuid>` URLs (deduped, brokerage logo + agent
portrait excluded), `pageQueryVariables property.id` (source listing UUID).

## 4. Supported KRAIN URL formats

- ✅ `https://krainrealestate.com/properties/<slug>` (and `www.`)
- ⛔ `https://krainrealestate.com/home-search/listings/<id>` → clean unsupported message
- ⛔ `https://mls.propertyshelf.com/…` → clean unsupported message

## 5. Database migration

`supabase-importer-setup.sql` — one private table `property_imports`
(workflow status, source identity incl. MLS/agent/brokerage, the full
authorization record, `source_snapshot`, editable `draft`, `validation`,
`images` provenance, append-only `history`, publish linkage, sync state)
+ indexes + RLS: **authenticated-only, zero anon policies**. Run once in the
Supabase SQL Editor. `properties` schema is untouched.

## 6. Storage configuration

Existing public bucket `photos` (uploads already authenticated-only via RLS).
Importer writes under `photos/import/<import-id>/`:
`NN-<name>-<uuid8>-orig.jpg` (preserved original bytes) and
`NN-<name>-<uuid8>.jpg` (≤1600 px, ~q0.72 display copy used in `photos[]`).
Source URL of every image is preserved in the import record. No hotlinking.

## 7. Authorization controls

Import records: source URL/provider/listing-ID/MLS/agent/brokerage, importing
user (auth email), dates, permission scope (own listing / KRAIN exclusive /
brokerage-approved / MLS syndication / written permission), permission note,
and three explicit flags (images / description / sync authorized). Publishing
is blocked until the master checkbox — *"I confirm that I am authorized to
republish this listing and its selected media on SoldByTiago"* — plus a scope
are set. Selected images additionally require the image flag; using the source
description requires the description flag. Internal compliance record only.

## 8. Validation system

Client-side engine, re-runs on every edit; classifications:
**Blocking** (publish disabled): missing name/price/status/type/location,
missing beds/baths on residential, contradictory source bathroom counts,
missing description, no copied hero image, missing authorizations/scope.
**Warning:** non-USD currency, built>lot, built=lot, built>1500 m², unparsable
source area, site baths > source total, low-res (<800 px) selections, failed
downloads, investment-performance claims in the description.
**Info:** missing coords/summary, every "Not provided by source" field, source
flags. Missing values display as **"Not provided by source"** — nothing is
invented, including status (always a deliberate choice).

## 9. Image-import system

Grid of all source images (lazy previews) → select/deselect, drag-reorder,
★ hero, per-image alt text. "Copy selected" (gated on authorization) fetches
via `/api/import-image` (original first, 2560-px rendition fallback — recorded),
measures dimensions, flags `low-res` / byte-identical `duplicate` / broken
previews, uploads original + optimized copy to own storage, and lists every
failure with its exact reason. Only copied display URLs can publish.

## 10. Draft & publish workflow

Statuses: `imported → needs_review → ready → published`, plus
`update_available` and `archived`. Publish (never automatic from Import):
re-validate → duplicate check → update-existing / create-new / cancel modal
(defaults to update when the source listing ID matches) → writes the
`properties` row (slug logic identical to admin.html; new rows appended via
`sort_order = max+1`, `featured = false`) → links the import + audit event →
offers the existing Vercel deploy-hook build so the clean URL, canonical,
OG, JSON-LD and sitemap bake exactly like every other listing. No UUID or
query-string public URLs are ever created.

## 11. Duplicate detection

At import, in the workspace banner, and again at publish: source URL,
source listing UUID, MLS ID (against other imports incl. their published
properties) + name prefix, coordinates (±0.0007°), exact address (against
live properties). Price/status conflicts with the chosen existing listing are
shown in the publish modal before overwrite. Image similarity beyond
byte-signature dedupe: see Limitations.

## 12. Synchronization

Manual **"Check source for changes"** (architecture ready for scheduling —
see § 16): re-fetches, diffs the stored snapshot field-by-field (+ images
added/removed, status), saves the new snapshot + diff, sets
`update_available`, and shows an approve-per-field modal that edits only the
**draft** — republishing is a further explicit step; public content is never
auto-overwritten and properties are never auto-deleted. A source page that
turns sold/withdrawn/removed (404/410) raises a red high-priority banner.

## 13. Import history

Append-only `history` events (imported, draft_saved with the full draft,
images_copied, marked_ready, published incl. the exact row written,
sync_checked, sync_applied, draft_restored, archived) with user + timestamp.
History modal can **restore any previously saved draft**.

## 14. Security

Supabase Auth required for the UI, the API endpoints (token verified
server-side against `/auth/v1/user`), all DB writes (RLS: authenticated-only;
`property_imports` has no anon access at all) and storage uploads. The API
holds no secrets, validates URLs server-side (https-only, no credentials/IP
hosts, strict domain allowlists, DNS resolution with private/link-local/
multicast rejection, per-hop redirect re-validation), enforces timeouts
(15 s/20 s), size caps (3 MB HTML, 4 MB image), image MIME allowlist
(jpeg/png/webp/avif), and per-user rate limits (20 fetches/min,
200 images/5 min, best-effort per instance). Extraction emits plain text only —
scripts, forms, iframes and tracking markup never survive. Overwriting an
existing listing always requires the explicit modal choice.

## 15. Test results (2026-07-19)

Adapter + API logic (real `importer.js` executed in a browser JS engine
against two saved live KRAIN fixtures — Casa Hanna, Villa Los Monos):
**44/44 assertions pass** — unit conversions, adapter routing,
allowlist/scheme rejection, name/price (incl. "Reduced Price" key)/beds/
full-half-total baths/MLS/type-mapping/coords/agent/brokerage/neighborhood/
year-built extraction, 2050-char clean description, hero-first image order
(42 and 120-image galleries), logo/portrait exclusion, "not provided" flags
for status/areas, no invented year_built.

UI (real page, real extracted data): login gate renders; workspace populates
every field; 6 correct blocking errors pre-review; publish disabled until
review complete then enabled; image toggle/hero/reorder; conversion lines
(366 m² = 3,940 ft²; 1,300 m² = 13,993 ft² = 0.32 acres); duplicate banner via
name+coords; publish modal with update/create choice + price-conflict note;
contradictory-baths → blocking; investment-claims → warning; mobile 375 px:
single-column, 2-up images, no horizontal scroll.

Remaining spec-16 items that require the deployed Vercel runtime + a live
login (network failure paths, real image download/storage upload, draft
persistence, publish, sitemap/canonical after build): scripted in
**§ Post-deploy verification** below and run with the first authorized
listing. Fixtures are real public pages; no client data is in test data.

## 16. Adding a future API or feed

Add an object to `ADAPTERS` in `api/_lib/importer.js` implementing
`{ id, label, supported: true, canHandle(url), extract(html|json, url) }`,
add its hosts to `PAGE_HOSTS`/`IMAGE_HOSTS`, and return the same normalized
shape (`source / listing / images / missing / flags`) — the UI, validation,
drafts, publishing, dedupe and sync all work unchanged. For a JSON/XML/CSV
feed or an official KRAIN API, `extract` parses the payload instead of HTML;
for authenticated feeds add the credential as a Vercel env var read inside
the function (never in client code).

## 17. Files created / changed

- **new** `supabase-importer-setup.sql` — private `property_imports` table + RLS
- **new** `api/_lib/importer.js` — safety layer + adapter registry
- **new** `api/import-fetch.js`, `api/import-image.js` — Vercel functions
- **new** `admin-import.html` — the importer UI
- **new** `KRAIN-IMPORTER.md` — this document
- **changed** `vercel.json` — rewrite `/admin/import-property/` → `/admin-import.html`
- **changed** `robots.txt` — Disallow `/admin-import.html`, `/admin/`, `/api/`
- `properties` table, public pages, build.py: **untouched**

## Setup (once)

1. Run `supabase-importer-setup.sql` in the Supabase SQL Editor.
2. Push to GitHub → Vercel deploys the functions + page automatically.
3. Open `https://soldbytiago.com/admin/import-property/`, sign in with the
   admin account.

## Deployment / rollback

Normal git push (no env vars, no new services). Rollback = revert the commit;
the `property_imports` table is inert without the UI.

## Post-deploy verification (with the first authorized listing)

Import → confirm every field against the source page (nothing invented) →
copy images (authorized) → draft saved → publish → trigger site build → check
`/property/<slug>/` clean URL, canonical, OG, JSON-LD, presence in
properties-page filters and `sitemap.xml` → confirm the import record holds
the source snapshot + permission record privately.

## Known limitations

- **Source "updated date" and listing status** aren't exposed by LP pages —
  status is always a deliberate manual choice.
- **Scheduled (unattended) sync** isn't wired: checks are one click, manual.
  Scheduling would need a Vercel cron + a server-side write credential
  (service-role env var) — deliberately not added while the no-secrets
  design holds.
- **Image similarity** dedupe is byte/dimension-signature only (no perceptual
  hashing); identical photos re-exported by the CDN could slip through.
- **IDX / home-search / Propertyshelf** URLs are intentionally not
  auto-imported (shared third-party MLS feed under personal/non-commercial
  licence terms, plus bot-protected pages with no public slug lookup) — clean
  refusal message, no partial imports. See § IDX / MLS listings.
- **Rate limiting** is per-function-instance (serverless best effort); the
  real gate is that every call requires a valid admin login.
- **HOA frequency, canton/province, furnished** etc. aren't structured on the
  source pages; whatever appears in spec pairs is shown, the rest is
  "Not provided by source".
- Vercel response caps mean images >4 MB fall back to the 2560-px CDN
  rendition (recorded per image as `rendition`).
