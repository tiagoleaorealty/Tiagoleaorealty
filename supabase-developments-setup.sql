-- ═══════════════════════════════════════════════════════════════
--  RESIDENTIAL DEVELOPMENTS — table + 8 researched seeds
--  (Pacifico and Reserva de Golf were dropped from the lineup.)
--  Run once in Supabase SQL Editor. Safe to re-run (idempotent-ish).
--  Facts sidebar fields (HOA, rental rules, construction, title,
--  price range) are BLANK on purpose: they are rarely published and
--  only Tiago can verify them — fill via the admin. The write-ups
--  carry researched, attributed material with qualified language.
-- ═══════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS developments (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL DEFAULT '',
  slug TEXT UNIQUE DEFAULT '',
  town TEXT DEFAULT '',
  -- matches properties.location so current listings auto-attach
  match_location TEXT DEFAULT '',
  established TEXT DEFAULT '',
  price_range TEXT DEFAULT '',
  hoa_fees TEXT DEFAULT '',
  amenities TEXT DEFAULT '',
  beach_access TEXT DEFAULT '',
  rental_rules TEXT DEFAULT '',
  construction_rules TEXT DEFAULT '',
  title_structure TEXT DEFAULT '',
  best_for TEXT DEFAULT '',
  lat DOUBLE PRECISION,
  lng DOUBLE PRECISION,
  excerpt TEXT DEFAULT '',
  meta_desc TEXT DEFAULT '',
  body TEXT DEFAULT '',
  cover_url TEXT DEFAULT '',
  photos TEXT[] DEFAULT '{}',
  status TEXT DEFAULT 'published' CHECK (status IN ('draft','published')),
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$ BEGIN NEW.updated_at = NOW(); RETURN NEW; END; $$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS developments_updated_at ON developments;
CREATE TRIGGER developments_updated_at BEFORE UPDATE ON developments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

ALTER TABLE developments ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Public can read published developments" ON developments;
CREATE POLICY "Public can read published developments"
  ON developments FOR SELECT USING (status = 'published');
DROP POLICY IF EXISTS "Auth can insert developments" ON developments;
CREATE POLICY "Auth can insert developments" ON developments FOR INSERT TO authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "Auth can update developments" ON developments;
CREATE POLICY "Auth can update developments" ON developments FOR UPDATE TO authenticated USING (true);
DROP POLICY IF EXISTS "Auth can delete developments" ON developments;
CREATE POLICY "Auth can delete developments" ON developments FOR DELETE TO authenticated USING (true);


INSERT INTO developments (name, slug, town, match_location, established, excerpt, body, sort_order)
VALUES ('Hacienda Pinilla', 'hacienda-pinilla', 'Avellanas', 'Hacienda Pinilla', '', '4,500 gated acres between Tamarindo and Avellanas — golf, beach club, three miles of coastline, and the deepest resale market of any resort community on this coast.', 'Hacienda Pinilla is the community I sell in more than any other, so consider this the insider version.

It is a 4,500-acre gated resort spanning roughly three miles of coastline south of Tamarindo, with an 18-hole golf course, a beachfront Beach Club, tennis and pickleball, an equestrian center, mountain-bike and hiking trails, a small market, and a collection of distinct neighborhoods — from golf-course homes to beachfront estates.

## What makes it different

Scale and maturity. Pinilla has been building since the 1990s, so you are buying into an established community with real infrastructure, a functioning HOA structure, and — crucially — a genuine resale market. Several of my current listings are here, from around $2.6M to $5.3M, which tells you the segment: this is the blue-chip end of the coast.

The beaches matter too: Avellanas on the south end is one of the best surf beaches in Guanacaste, and Langosta sits just north.

## Who it fits

Buyers who want resort infrastructure without a resort crowd — Pinilla is quiet, spread out, and residential in feel. Golfers, obviously. And anyone who wants strong rental fundamentals with luxury finish; the vacation-rental market here is well established.

## Honest considerations

Distances inside the property are real — you will drive to the Beach Club and to town. HOA fees, rental rules and per-neighborhood construction guidelines vary by section and change; I confirm current figures for the specific neighborhood before any offer, so ask.

## Alternatives to compare

Reserva Conchal for a more hotel-anchored resort feel, Mar Vista for larger lots at lower entry prices.', 1)
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location,
  established = EXCLUDED.established, excerpt = EXCLUDED.excerpt, body = EXCLUDED.body,
  sort_order = EXCLUDED.sort_order;

INSERT INTO developments (name, slug, town, match_location, established, excerpt, body, sort_order)
VALUES ('Reserva Conchal', 'reserva-conchal', 'Brasilito', 'Reserva Conchal', '', 'Guanacaste''s most complete resort community — Robert Trent Jones II golf, the Westin and W hotels, and a beach club on Playa Conchal itself.', 'Reserva Conchal is the most hotel-anchored community on this coast — and depending on the buyer, that is either exactly the point or the reason to look next door.

The development sits directly behind Playa Conchal, the crushed-shell beach that shows up on every list of Costa Rica''s best. Inside: a Robert Trent Jones II championship golf course (7,021 yards, par 71, Audubon-certified since 2001), a beach club right on Conchal, spa, trails, and two international hotels — the all-inclusive Westin and the W Costa Rica.

## What makes it different

The hotel infrastructure. Owners get resort services most communities simply cannot offer, and the rental market benefits from the brand pull of the Westin and W. Current residential phases include the Sanara residences and Laurel forest-view lots, alongside established condo and villa neighborhoods.

CRIA — the U.S.-accredited international school — is 500 meters from the entrance, which quietly makes Conchal one of the most practical choices on this coast for relocating families.

## Who it fits

Buyers who want turnkey, amenity-rich ownership with strong rental branding, and families who want the school run to be five minutes.

## Honest considerations

You are inside a resort: expect resort pacing, resort fees, and rules designed around a hospitality operation. Concierge-managed communities carry meaningful HOA and club costs — I confirm the current fee schedule and rental program terms for the specific sub-community before any offer.

## Alternatives to compare

Hacienda Pinilla for more land and a quieter feel, Mar Vista next door for larger private lots, Las Catalinas for walkable-town living instead of resort living.', 2)
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location,
  established = EXCLUDED.established, excerpt = EXCLUDED.excerpt, body = EXCLUDED.body,
  sort_order = EXCLUDED.sort_order;

INSERT INTO developments (name, slug, town, match_location, established, excerpt, body, sort_order)
VALUES ('Senderos', 'senderos-tamarindo', 'Tamarindo', 'Senderos', '', 'Tamarindo''s largest luxury gated community — 110 hillside acres above town with a private beach club at the estuary and ''Natural Modern'' architecture.', 'Senderos is the answer to a question Tamarindo buyers kept asking: how do I live five minutes from town without living *in* town?

It is a roughly 110-acre gated community in the hills above Tamarindo — one of only a handful of true gated communities here — with sweeping views over the ocean, the Las Baulas National Marine Park and the estuary. The development''s own numbers: five minutes to Tamarindo''s beach and restaurants, about 1.8 km to the sand, and roughly an hour to Liberia airport.

## What makes it different

Two things. First, the private beach club, Puerta de Sal, at the mouth of the estuary — membership is deliberately limited, and it gives Senderos owners something almost nothing in central Tamarindo offers: a private foothold on the water. Second, the architectural discipline: homes follow the community''s "Natural Modern" principles with vetted architects, so the build quality and coherence are unusually high for this coast.

There is also a Garden Plaza with shops and cafés at the entrance, gated 24/7 security, and a planned sports and wellness Valley Club.

## Who it fits

Buyers who want walkable-ish proximity to Tamarindo''s restaurants and surf with privacy, security and views — especially those planning to build.

## Honest considerations

Much of Senderos is still build-out: you are often buying a homesite plus a construction project, with design guidelines to follow. HOA fees and rental rules come from the developer''s current schedule — I confirm them per lot before any offer.

## Alternatives to compare

Tamarindo Park next door in the Langosta hills, or a finished home in central Tamarindo if you want zero construction wait.', 3)
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location,
  established = EXCLUDED.established, excerpt = EXCLUDED.excerpt, body = EXCLUDED.body,
  sort_order = EXCLUDED.sort_order;

INSERT INTO developments (name, slug, town, match_location, established, excerpt, body, sort_order)
VALUES ('Tamarindo Park', 'tamarindo-park', 'Tamarindo', 'Tamarindo Park', '', 'The newest gated community in Tamarindo — a planned 220-home village in the reforested hills between Tamarindo and Langosta, designed by Richard Müller.', 'Tamarindo Park is the newest of Tamarindo''s gated communities, carved into the reforested hillside that connects Tamarindo to Playa Langosta.

The master plan calls for around 220 tropical-contemporary homes designed under Richard Müller — one of Costa Rica''s most established architects — with a spa and wellness center, sports club, hiking trails and paddle courts. Phase I, the Hilltop, launched with 32 homes and a first release of lots.

## What makes it different

Position and design pedigree. The site sits between the two beaches, so you are minutes from both Tamarindo''s energy and Langosta''s quiet. And because it is a ground-up master plan rather than an accumulation of lots, the architectural consistency will be closer to Senderos or Las Catalinas than to an older subdivision.

## Who it fits

Early buyers who want new construction at pre-build-out pricing in a location that cannot be replicated — there is no more undeveloped hillside between Tamarindo and Langosta. Also buyers comfortable with a community that is still becoming itself.

## Honest considerations

This is a young development: amenities arrive in phases, and you are betting on execution. That bet has upside — early phases of successful communities on this coast have historically been rewarded — but it is a different risk profile from buying into a 20-year-old neighborhood. Delivery timelines, HOA structure and rental rules come from the current developer documents; I walk through them with buyers before any commitment.

## Alternatives to compare

Senderos for a more established version of the same idea, Langosta itself for finished beachside homes, Hacienda Pinilla for resort-scale maturity.', 4)
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location,
  established = EXCLUDED.established, excerpt = EXCLUDED.excerpt, body = EXCLUDED.body,
  sort_order = EXCLUDED.sort_order;

INSERT INTO developments (name, slug, town, match_location, established, excerpt, body, sort_order)
VALUES ('Las Ventanas de Playa Grande', 'las-ventanas-playa-grande', 'Playa Grande', 'Las Ventanas', '', 'A 380-acre, 73-property community on the ridge between Playa Grande and Playa Conchal — the lowest-density gated community on this coast.', 'Las Ventanas is the low-density outlier: 380 acres holding just 73 properties, spread across nine small subdivisions on the panoramic ridge between Playa Grande and Playa Conchal.

That ratio — over five acres of land per property — is the whole story. The quintas in La Sabana run 1.2 to 2.26 acres each; El Roble''s sites look out over the Catalinas islands. Around seventy people live here full-time, which gives Ventanas something rare among view communities: an actual neighborhood, not a rental compound.

## What makes it different

Privacy per dollar, and self-sufficiency. The community runs its own concessioned water supply — a bigger deal in Guanacaste than most buyers realize — and local brokerages have published HOA fees around $388 per month including water (verify current figures; fees change). Amenities are genuinely communal: an ocean-view clubhouse with pool, tennis and pickleball courts, a soccer field, a skate park and trail network. Liberia airport is about 50 minutes.

## Who it fits

Buyers who want land, views and quiet over walk-to-dinner convenience — especially full-time relocators and builders who want acreage without ranch-level remoteness.

## Honest considerations

You will drive for everything: beaches, groceries, restaurants. Most purchases here are lot-plus-build, with community design guidelines to follow. And low density cuts both ways — fewer neighbors also means fewer comparables when you eventually sell.

## Alternatives to compare

Mar Vista for a larger community with similar lot sizes, Playa Grande town for surf-first living closer to the sand, Hacienda Pinilla for amenities at scale.', 5)
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location,
  established = EXCLUDED.established, excerpt = EXCLUDED.excerpt, body = EXCLUDED.body,
  sort_order = EXCLUDED.sort_order;

INSERT INTO developments (name, slug, town, match_location, established, excerpt, body, sort_order)
VALUES ('Mar Vista', 'mar-vista', 'Brasilito', 'Mar Vista', '', '750 acres between Brasilito and Flamingo — 5,000 m² lots, 30 km of paved roads, a third of the land preserved, and La Paz school at the entrance.', 'Mar Vista is the community families keep landing on once they map the school run — La Paz Community School''s Cabo Velas campus sits at its entrance, and no other large community on this coast can say that.

The development covers about 750 acres between Brasilito and Playa Flamingo, overlooking Conchal bay, with four neighborhoods — three of them built around lots averaging 5,000 m² (roughly 1.25 acres). Infrastructure is the serious kind: 30+ kilometers of paved roads, underground utilities, 24/7 gated security. A community clubhouse, resort-style infinity pool, onsite dining, night-lit clay tennis courts, eight pickleball courts, and trail networks round it out. About a third of the acreage is committed as nature preserve.

## What makes it different

Land and the school. Where Conchal sells resort services and Pinilla sells maturity, Mar Vista sells space — big private lots at entry prices generally below the beachfront resorts — plus the only situation on the coast where an accredited international school is inside the gate''s shadow.

## Who it fits

Relocating families, and buyers who want to build a substantial home on real acreage while staying ten minutes from Flamingo and Conchal.

## Honest considerations

Mar Vista is still building out; parts of it are lots and construction rather than finished streetscape. It sits on the hillside, not the sand — beach trips are a short drive. HOA fees and build guidelines come from the current community documents; I confirm them per neighborhood before any offer.

## Alternatives to compare

Las Ventanas for even lower density, Catalina Cove for a smaller established version of the big-lot idea, Reserva Conchal for resort amenities instead of acreage.', 6)
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location,
  established = EXCLUDED.established, excerpt = EXCLUDED.excerpt, body = EXCLUDED.body,
  sort_order = EXCLUDED.sort_order;

INSERT INTO developments (name, slug, town, match_location, established, excerpt, body, sort_order)
VALUES ('Catalina Cove', 'catalina-cove', 'Brasilito', 'Catalina Cove', '2005', 'An established 40-hectare community in Brasilito — around 100 oversized lots, mature trees, full-time neighbors, and some of the most accessible entry prices behind this coastline.', 'Catalina Cove is the quiet achiever of the Brasilito corridor — established in 2005, roughly 40 hectares, and organized around genuinely oversized lots: about 73 parcels averaging 5,000 m² plus 29 more around 2,000 m².

Twenty years of growth means mature trees, settled roads, and a real mix of full-time residents alongside vacation homes — the kind of lived-in feel new developments spend a decade chasing.

## What makes it different

Accessibility, in both senses. It is walking-to-short-drive distance from Playa Brasilito, minutes from Conchal and Flamingo — and its entry prices are among the lowest of any gated community in this corridor, with lots recently advertised from around $60,000 and homes from the low $200s (asking prices; verify current availability). For a coast where gated communities often start at seven figures, that is a different market entirely.

## Who it fits

First-time Costa Rica buyers who want gated security and land without resort pricing; builders who want a large flat-ish lot in an established neighborhood; and buyers priced out of Flamingo or Conchal who still want that ten-minute circle.

## Honest considerations

There is no beach club, golf course or resort amenity stack here — this is a residential neighborhood, full stop. The HOA is functioning and fees are modest by coastal standards, but as always I confirm current dues and any build guidelines before an offer.

## Alternatives to compare

Mar Vista for grander infrastructure and the school, Potrero''s Surfside area for beach-walk proximity, Las Ventanas for view acreage.', 7)
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location,
  established = EXCLUDED.established, excerpt = EXCLUDED.excerpt, body = EXCLUDED.body,
  sort_order = EXCLUDED.sort_order;

INSERT INTO developments (name, slug, town, match_location, established, excerpt, body, sort_order)
VALUES ('Las Catalinas', 'las-catalinas', 'Las Catalinas', 'Las Catalinas', '', 'The car-free New Urbanist beach town on Playa Danta — walkable streets, 1,000 acres of tropical forest trails, and architecture found nowhere else in Central America.', 'Las Catalinas is not a gated community in the normal sense — it is a purpose-built, car-free beach town, and there is nothing else like it in Central America.

The town rises straight from Playa Danta in stacked Mediterranean-style streets where cars stay parked at the edge and everything happens on foot: restaurants, shops, plazas, pools. Behind it, around 1,000 acres of tropical dry forest laced with hiking and mountain-biking trails. The design pedigree is New Urbanist to its bones, and it has attracted an international owner base to match.

## What makes it different

Walkability is the entire product. You wake up, walk to coffee, walk to the beach, walk to dinner — a lifestyle simply unavailable anywhere else on this coast. The trail network and beach-town energy make it equally strong as a full-time home or a rental with genuine differentiation.

## Who it fits

Buyers who value urbanism over acreage: no lawn, no car errands, neighbors close by design. Flats have historically entered around the $400,000s with townhomes and villas running from $1M to well past $5M (asking prices; the market moves — I confirm current inventory).

## Honest considerations

Density is the point, so privacy is architectural rather than spatial. Rental and design rules are structured and firm — that protects the town''s coherence, but it is a rulebook you should read before buying, and I go through it with every client. Costs reflect the shared-town infrastructure.

## Alternatives to compare

Nothing directly comparable exists here. Flamingo offers walkable-ish beach living with cars; Senderos offers gated hillside living near a real town.

There is a fuller town guide on my [Las Catalinas community page](https://soldbytiago.com/las-catalinas.html).', 8)
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location,
  established = EXCLUDED.established, excerpt = EXCLUDED.excerpt, body = EXCLUDED.body,
  sort_order = EXCLUDED.sort_order;

-- Verify
SELECT sort_order, name, slug, town FROM developments ORDER BY sort_order;
