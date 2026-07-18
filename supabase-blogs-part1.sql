-- NEW BLOG POSTS - PART 1 of 2 (articles 1-5: community guides)
-- Run in Supabase SQL Editor. Safe to re-run (replaces these slugs only).
DELETE FROM blog_posts WHERE slug IN ('hacienda-pinilla-communities-amenities-guide', 'reserva-conchal-real-estate-communities-guide', 'senderos-tamarindo-real-estate-guide', 'tamarindo-park-real-estate-buyers-guide', 'las-ventanas-playa-grande-real-estate-guide', 'mar-vista-flamingo-real-estate-guide', 'costa-rica-property-due-diligence-checklist', 'costa-rica-property-water-letter-guide', 'costa-rica-property-title-plano-catastrado-guide', 'buying-land-guanacaste-zoning-water-building-checklist');

INSERT INTO blog_posts (title, slug, category, status, readtime, excerpt, meta_desc, body, cover_url)
VALUES ('Hacienda Pinilla Communities and Amenities: The Complete Buyer''s Guide',
        'hacienda-pinilla-communities-amenities-guide',
        'guide', 'published', '4 min read',
        'Every amenity, beach and property type inside the 4,500-acre Hacienda Pinilla resort south of Tamarindo - compiled from the resort''s own published materials, with the questions buyers should verify before purchasing.',
        'Hacienda Pinilla buyer''s guide: the golf course, Beach Club, equestrian center, four beaches, property types and verification questions - sourced from official materials.',
        '**Quick answer:** Hacienda Pinilla is a 4,500-acre gated beach and golf resort south of Tamarindo in Guanacaste, Costa Rica. According to [the resort''s own materials](https://www.haciendapinilla.com/), it spans roughly three miles of Pacific coastline, contains an 18-hole golf course, a beachfront Beach Club, an equestrian center, tennis courts, trail networks and a small market, and its residential offering runs from condominiums and golf-course homes to beachfront estates and titled building lots. This guide compiles what the resort publishes, notes what it does not, and lists the questions a buyer should verify before making an offer.

## Where it is

Hacienda Pinilla sits on the coast south of Tamarindo, in the Santa Cruz canton of Guanacaste. The nearest international airport is Liberia (LIR). Rather than quote a drive time here, every listing on this site shows a computed driving time to LIR on its own page - use that for the specific property you are considering.

## The beaches

The property fronts several beaches. Playa Avellanas, at the southern end, is one of Guanacaste''s best-known surf breaks. Playa Mansita and Playa Bonita sit within the resort itself - Mansita directly in front of the JW Marriott hotel - and Playa Langosta lies just north toward Tamarindo. All beaches in Costa Rica are public by law up to the 50-meter public zone; what a gated community controls is land access through its property, not the sand itself. (For how coastal land ownership actually works, see my guide to [titled vs. concession beachfront](https://soldbytiago.com/blog/titled-vs-concession-beachfront-costa-rica/).)

## The golf course

Per [the resort''s golf page](https://www.haciendapinilla.com/golf.html), the 18-hole course was designed by Mike Young, plays to par 72 at up to about 7,200 yards, and holds an Audubon Cooperative Sanctuary designation for its conservation practices. The resort publishes a nine-hole option, a practice area, a pro shop and a restaurant-bar at the clubhouse, with current rates and tee times listed on that page.

## The rest of the amenities

The resort''s [amenities page](https://www.haciendapinilla.com/amenities.html) lists the beachfront Beach Club, tennis and pickleball, an equestrian center, mountain-bike and hiking trails through tropical dry forest, and the Pinilla Market for basics. The JW Marriott Guanacaste Resort & Spa operates inside the property, adding hotel restaurants and a spa. Amenity access, membership terms and any usage fees vary by what you buy and are set by the resort and the relevant associations - confirm the current terms in writing for the specific property before you offer.

## Property types and neighborhoods

Hacienda Pinilla has been developed in phases since the 1990s and is organized into distinct sections rather than one uniform product: beachfront and estate homes, golf-course neighborhoods (Reserva de Golf, for example, is a defined 136-lot neighborhood along the course), condominium sections, and titled homesites where buyers design and build. Each section has its own governance and fee structure layered under the master resort.

## What Hacienda Pinilla does not publish

Current HOA fees per neighborhood, rental-program rules, and per-section construction guidelines are not published openly and change over time. Treat any figure you read on a third-party site - including price or fee ranges - as a starting point to verify, not a fact. Before an offer, request in writing:

- The current fee schedule for the specific neighborhood, plus the master resort obligations
- The neighborhood''s construction guidelines and approval process, if you plan to build
- Rental rules for the section, if income matters to your plan
- The HOA''s financial statements and any planned special assessments

## Buying here

I sell in Hacienda Pinilla more than in any other community on this coast, and my agent''s-eye view - who it fits, honest trade-offs, and my current listings inside the resort - lives on my [Hacienda Pinilla community page](https://soldbytiago.com/development/hacienda-pinilla/). You can browse every current listing at [soldbytiago.com/properties](https://soldbytiago.com/properties.html).

## Sources & Verification

- [Hacienda Pinilla - official site](https://www.haciendapinilla.com/) - resort overview and contact
- [Hacienda Pinilla - golf](https://www.haciendapinilla.com/golf.html) - course details, designer, rates
- [Hacienda Pinilla - amenities](https://www.haciendapinilla.com/amenities.html) - Beach Club, equestrian, trails
- Resort-specific claims above are attributed to Hacienda Pinilla''s published materials; fee, rule and availability details must be confirmed directly with the resort and the relevant homeowners associations.

---

**About this article.** Written for SoldByTiago by [Tiago Leao](https://soldbytiago.com/about.html), a real estate agent with KRAIN Luxury Real Estate in Guanacaste, Costa Rica. Last reviewed: July 18, 2026. This article is general education, not legal, tax, or investment advice. Rules, fees and procedures change - verify everything that matters to your purchase with a Costa Rican attorney and the official sources linked above before acting.',
        '');

INSERT INTO blog_posts (title, slug, category, status, readtime, excerpt, meta_desc, body, cover_url)
VALUES ('Reserva Conchal Real Estate: Residential Communities, Golf and Beach Club Guide',
        'reserva-conchal-real-estate-communities-guide',
        'guide', 'published', '4 min read',
        'The seventeen residential communities of Reserva Conchal, the golf course, Beach Club, Westin and W hotels, and the questions buyers should verify before purchasing - sourced from the resort''s official materials.',
        'Reserva Conchal buyer''s guide: all 17 residential communities, golf, Beach Club, resort access, security and the buyer verification checklist - from official sources.',
        '**Quick answer:** Reserva Conchal is a roughly 2,300-acre master-planned beach, golf and residential community behind Playa Conchal in Guanacaste, Costa Rica. According to [the resort''s official site](https://reservaconchal.com/), its residential offering spans seventeen named communities - from condominiums and townhomes to custom homes and building lots - alongside a championship golf course, a private Beach Club, and two international hotels, the all-inclusive Westin and the W Costa Rica. This guide compiles what the resort publishes and the questions every buyer should verify before purchasing.

## The setting

Reserva Conchal rises behind Playa Conchal, the crushed-shell beach between Brasilito and Puerto Viejo bay, in the Santa Cruz canton. The towns of Brasilito and Playa Flamingo are immediately north; Liberia international airport (LIR) is the region''s air gateway - each listing on this site computes its own drive time to LIR, so check the specific property page rather than relying on a general figure.

## Seventeen residential communities

Per [Reserva Conchal''s real-estate pages](https://reservaconchal.com/real-estate/), the residential communities are named for local flora - many for trees native to Guanacaste - and some are as small as five residences. The official list: Aromo, Bougainvillea, Carao, Ceibo, Cocobolo, Cortez Amarillo, Guayacan, Jobo, Laurel, Llama del Bosque, Malinche, Melinas, Roble Sabana, Sanara, Sauco, Solaris, and The W Residences. The mix runs from golf-view condominiums to ocean-view custom homes and premium lots (the [Laurel](https://reservaconchal.com/laurel/) section, for example, is marketed as forest-side building lots).

Each community has its own character, administration and fee structure - a fact that matters enormously at purchase time, because two similar-looking condos in different sections can carry different monthly costs and rules.

## Golf, Beach Club and resort access

The resort''s course is a Robert Trent Jones II design that the resort and its operators publish as a par-71 championship layout, certified as an Audubon sanctuary. The private Beach Club sits directly on Playa Conchal. Because the Westin and W operate inside the same gates, owners live alongside a functioning hospitality operation - which is precisely the appeal for some buyers and the deal-breaker for others.

Reserva Conchal also publishes an unusual sustainability profile for this coast: per [its official site](https://reservaconchal.com/), the community runs on renewable energy with onsite recycling, a water-treatment facility, and what it describes as the country''s first desalination plant. Those are the resort''s own claims - meaningful ones for long-term water security in dry Guanacaste, and worth asking about in detail during due diligence.

## Security and property management

The community is gated with controlled access. Property management, rental programs and club-access terms are structured per community and per ownership type. Before buying, have your attorney confirm which club and resort privileges actually convey with the specific unit - do not assume the marketing brochure''s amenity list applies identically to every property.

## What to verify before purchasing

- The current HOA/condo fee schedule for the specific community, and the master obligations above it
- Beach Club and golf access terms for that ownership type, in writing
- Rental-program rules and any revenue splits, if you plan to rent
- The community''s financial statements, reserves and any planned assessments
- Water, as everywhere in Guanacaste: how the specific section is served and what the resort''s infrastructure commitments are (see my guide to [water letters](https://soldbytiago.com/blog/costa-rica-property-water-letter-guide/))
- The full [due-diligence checklist](https://soldbytiago.com/blog/costa-rica-property-due-diligence-checklist/) that applies to any Costa Rica purchase

## Buying here

My agent''s-eye view of Conchal - who it fits, trade-offs against neighboring communities, and how it compares to Hacienda Pinilla or Mar Vista - is on my [Reserva Conchal community page](https://soldbytiago.com/development/reserva-conchal/). Relocating families should also note that [CRIA, the U.S.-accredited international school](https://soldbytiago.com/school/costa-rica-international-academy/), operates about 500 meters from the entrance.

## Sources & Verification

- [Reserva Conchal - official site](https://reservaconchal.com/) - community overview and sustainability claims
- [Reserva Conchal - real estate](https://reservaconchal.com/real-estate/) - the residential communities
- [Reserva Conchal - Laurel](https://reservaconchal.com/laurel/) - example of a current lot offering
- Community counts, names and sustainability claims are the resort''s published statements; fees, rules and access terms must be confirmed per community with the administration and your attorney.

---

**About this article.** Written for SoldByTiago by [Tiago Leao](https://soldbytiago.com/about.html), a real estate agent with KRAIN Luxury Real Estate in Guanacaste, Costa Rica. Last reviewed: July 18, 2026. This article is general education, not legal, tax, or investment advice. Rules, fees and procedures change - verify everything that matters to your purchase with a Costa Rican attorney and the official sources linked above before acting.',
        '');

INSERT INTO blog_posts (title, slug, category, status, readtime, excerpt, meta_desc, body, cover_url)
VALUES ('Senderos Tamarindo: Property, Amenities and Location Guide',
        'senderos-tamarindo-real-estate-guide',
        'guide', 'published', '4 min read',
        'What the Senderos development publishes about its homesites, Natural Modern architecture, Puerta de Sal beach club and location above Tamarindo - plus what buyers should request before offering.',
        'Senderos Tamarindo buyer''s guide: homesites, design code, the Puerta de Sal beach club, gated access and the documents to request before an offer - sourced from the developer.',
        '**Quick answer:** Senderos is a gated residential community in the hills directly above Tamarindo, Guanacaste. According to [the developer''s official site](https://senderos-cr.com/community/), the community offers homesites and architect-designed homes under a "Natural Modern" design code, with walking trails, pools, tennis, gardens and a private beach club - Puerta de Sal - where the Tamarindo estuary meets the ocean. The developer''s own published figures put the community about five minutes from Tamarindo''s beach and restaurants and roughly an hour from Liberia airport.

## The concept

Senderos is one of only a handful of true gated communities in Tamarindo proper. The developer''s stated concept is a master-planned hillside neighborhood above the town: privacy, security and views, close enough to walk-or-five-minute-drive into Costa Rica''s best-known surf town. Views from the ridge take in the Pacific, the estuary and the Las Baulas National Marine Park - protected land, which is relevant if long-term view protection matters to you.

## Homes and lots

Most of the offering is homesites - the developer markets generous lots, many in the half-acre range, with ocean, valley or forest orientations - which buyers pair with the community''s roster of approved architects to design and build under the "Natural Modern" guidelines. Finished architect-designed homes resell occasionally. The design-code approach is deliberate: it trades some freedom for architectural coherence across the community.

## Puerta de Sal - the private beach club

Per [the developer''s beach-club pages](https://senderos-cr.com/puerta-de-sal-private-beach-club/), Puerta de Sal opened in late 2025 at the estuary mouth with an oceanfront pool, dining in partnership with Pangas, a spa treatment room, concierge and towel service, firepits and direct sand access, with membership described as limited. Club membership terms, costs and transferability are exactly the kind of thing to confirm in writing during due diligence - marketing pages describe amenities, not your contractual rights.

## Infrastructure and daily life

The development sits behind the Garden Plaza commercial area, which the developer notes includes an Automercado supermarket - the largest in the area - and the region''s only movie theater. Inside the gates the developer publishes resort-style pools, tennis, a gym, kilometers of trails, organic gardens, playgrounds and a dog park, with a sports-and-wellness "Valley Club" planned. Planned amenities deserve their own scrutiny: ask what is contractually committed versus conceptual.

## What to request before making an offer

- The current design guidelines and the architect-approval process, with timelines
- HOA structure, current fees and what they cover; developer obligations during build-out
- Puerta de Sal membership terms: cost, transfer on resale, guest and rental-tenant rules
- Water and utilities commitments for your specific lot (see [what a water letter is](https://soldbytiago.com/blog/costa-rica-property-water-letter-guide/) and why it matters before building)
- The registered plano catastrado for the lot and a boundary confirmation (see my guide to [titles and survey plans](https://soldbytiago.com/blog/costa-rica-property-title-plano-catastrado-guide/))
- Construction rules: build timelines, height limits, and what happens if you hold the lot unbuilt

## Current listings

My current Tamarindo listing [Casa Hanna](https://soldbytiago.com/property/casa-hanna-tamarindo/) sits in these same hills above town - and my agent''s-eye view of Senderos itself, including how it compares to Tamarindo Park next door, is on my [Senderos community page](https://soldbytiago.com/development/senderos-tamarindo/). For everything currently for sale, see [all listings](https://soldbytiago.com/properties.html).

## Sources & Verification

- [Senderos - community](https://senderos-cr.com/community/) - developer''s concept, amenities and location figures
- [Senderos - Puerta de Sal](https://senderos-cr.com/puerta-de-sal-private-beach-club/) - beach club description
- Distances, amenity lists and the design-code description are the developer''s published claims. Membership terms, HOA figures and construction rules are not published in full and must be requested directly and reviewed with your attorney.

---

**About this article.** Written for SoldByTiago by [Tiago Leao](https://soldbytiago.com/about.html), a real estate agent with KRAIN Luxury Real Estate in Guanacaste, Costa Rica. Last reviewed: July 18, 2026. This article is general education, not legal, tax, or investment advice. Rules, fees and procedures change - verify everything that matters to your purchase with a Costa Rican attorney and the official sources linked above before acting.',
        '');

INSERT INTO blog_posts (title, slug, category, status, readtime, excerpt, meta_desc, body, cover_url)
VALUES ('Tamarindo Park Real Estate: A Buyer''s Guide to the New Community',
        'tamarindo-park-real-estate-buyers-guide',
        'guide', 'published', '4 min read',
        'What the Tamarindo Park developer publishes about the Hilltop phase, Richard Müller homes, sustainability commitments and amenities - and the documents buyers should request in a young development.',
        'Tamarindo Park buyer''s guide: the Hilltop phase, Richard Müller-designed homes, developer sustainability claims, and the HOA and construction documents to request.',
        '**Quick answer:** Tamarindo Park is a new master-planned gated community on the reforested hillside between Tamarindo and Playa Langosta in Guanacaste. According to [the developer''s official site](https://tamarindopark.com/), the property covers about 37 hectares (roughly 91 acres), the master plan contemplates around 220 tropical-contemporary homes delivered in phases, and the developer states a commitment to keeping as much as 75% of the property natural. The first phase - the Hilltop - launched with 32 homes plus building lots, with homes designed by Costa Rican architect Richard Müller.

## Location

The site occupies the hills connecting Tamarindo to Playa Langosta - effectively the last large undeveloped parcel between the two. The developer describes the Hilltop phase as about a ten-minute walk from the beach and downtown Tamarindo. Tamarindo''s services, restaurants and surf are the immediate draw; Langosta''s quieter beach sits on the other side. For families, Tamarindo''s international schools - [Educarte](https://soldbytiago.com/school/educarte/) and [Journey School](https://soldbytiago.com/school/journey-school-tamarindo/) - are a short drive.

## Development layout and property types

Per [the developer''s news updates](https://tamarindopark.com/news/the-continuous-progress-in-hilltop/), Phase I (the Hilltop) sits at the community entrance and consists of 32 homes plus a release of lots, with the first thirteen homes reported delivered. Homes are designed under Richard Müller - one of Costa Rica''s most established residential architects - ranging from four to eight bedrooms, and the developer describes them as tailored to each homesite, often designed around existing trees. Later phases extend the master plan toward the ~220-home total.

## Amenities - planned versus delivered

The developer''s published amenity plan includes a wellness and fitness center, a sports club, an ocean-view sunset club, paddle courts, a community garden, hiking and mountain-bike trails and a small commercial area. In any young community, the honest question is not "what is planned" but "what is delivered, and what is contractually committed with dates." Ask for that distinction in writing.

## Sustainability claims

The developer states that roughly 75% of the property will remain natural and describes reforestation, permaculture and regenerative-agriculture practices. These are the developer''s own commitments - attributed here to Tamarindo Park''s published materials - and a buyer who values them should ask how they are legally anchored: in the master plan, the HOA covenants, or marketing language alone. The difference matters.

## HOA and construction documents to request

- The HOA''s formation documents, current budget and fee schedule, and who controls the HOA during build-out (developer vs. owners)
- Delivery timelines for your phase''s amenities, and remedies if they slip
- Construction guidelines: what you may build on a lot, approval process, and any build-time requirements
- Utility commitments for your lot - water especially (read [what a water letter is](https://soldbytiago.com/blog/costa-rica-property-water-letter-guide/) before you buy any lot in Guanacaste)
- The lot''s registered survey plan and boundaries ([how planos catastrados work](https://soldbytiago.com/blog/costa-rica-property-title-plano-catastrado-guide/))
- The full [due-diligence checklist](https://soldbytiago.com/blog/costa-rica-property-due-diligence-checklist/) with your attorney

## Buying here

A young development is a different risk profile from a 20-year-old neighborhood: the upside of early pricing against the execution risk of phased delivery. My agent''s-eye view - including how Tamarindo Park compares with neighboring [Senderos](https://soldbytiago.com/development/senderos-tamarindo/) - is on my [Tamarindo Park community page](https://soldbytiago.com/development/tamarindo-park/). For current availability in and around Tamarindo, [browse my listings](https://soldbytiago.com/properties.html) or ask me directly.

## Sources & Verification

- [Tamarindo Park - official site](https://tamarindopark.com/) - master plan, size, sustainability commitments
- [Tamarindo Park - Hilltop progress](https://tamarindopark.com/news/the-continuous-progress-in-hilltop/) - phase status and deliveries
- Home counts, the 75% preservation figure, walk-time and amenity plans are the developer''s published claims and should be re-verified at contract time; HOA and construction rules are not fully published and must be requested.

---

**About this article.** Written for SoldByTiago by [Tiago Leao](https://soldbytiago.com/about.html), a real estate agent with KRAIN Luxury Real Estate in Guanacaste, Costa Rica. Last reviewed: July 18, 2026. This article is general education, not legal, tax, or investment advice. Rules, fees and procedures change - verify everything that matters to your purchase with a Costa Rican attorney and the official sources linked above before acting.',
        '');

INSERT INTO blog_posts (title, slug, category, status, readtime, excerpt, meta_desc, body, cover_url)
VALUES ('Las Ventanas de Playa Grande: Community and Property Guide',
        'las-ventanas-playa-grande-real-estate-guide',
        'guide', 'published', '4 min read',
        'The nine subdivisions, private water system and amenities of Las Ventanas de Playa Grande, per the community''s published materials - with the HOA and building questions buyers should verify.',
        'Las Ventanas de Playa Grande buyer''s guide: 380 acres, 73 properties, nine subdivisions, private water concession, amenities and buyer verification questions.',
        '**Quick answer:** Las Ventanas de Playa Grande is a low-density gated community on the ridge between Playa Grande and Playa Conchal in Guanacaste. Per [the community''s official site](https://www.ventanasplayagrande.com/) and its local brokerage materials, the property spans about 380 acres holding just 73 properties across nine small subdivisions, with an ocean-view clubhouse, sport courts, trails, a community organic garden - and, unusually for this coast, its own concessioned water well serving the community.

## Location

The community sits on elevated land between two very different marquee beaches: Playa Grande - a renowned surf beach inside Las Baulas National Marine Park, famous as a leatherback turtle nesting site - and Playa Conchal''s white shell sand. Tamarindo sits across the estuary to the south (by road, substantially farther than it looks across the water). Liberia airport is the air gateway; check any specific listing''s page on this site for its computed drive time.

## The nine subdivisions

Las Ventanas is organized into nine named subdivisions - La Sabana, El Roble, Caracara, El Camino, Catalinas, Altamar, Jaguarundi, San Pedro and Cenizaros - each holding a handful of properties. Published lot characteristics vary by section; the La Sabana quintas, for example, are marketed at roughly 1.2 to 2.26 acres each, and El Roble''s sites are marketed for their views over the Catalinas islands. With 73 total properties, inventory at any moment is structurally scarce: a mix of finished hillside homes, quintas and unbuilt acreage.

## Amenities

The community''s published amenity list includes a west-facing clubhouse with an infinity pool near the top of Cerro Almendro, a tennis and pickleball court, a soccer field, a skate park and playground, several kilometers of jungle trails, and a community organic garden. Roads are paved and the entrance is gated 24/7 per the community''s materials.

## Water - the detail that matters most

Las Ventanas publishes that it operates its own concessioned water well for the community. In seasonally dry Guanacaste, a community''s water arrangement is one of the most consequential facts about it - it determines whether you can get the availability letter needed for a building permit. Local brokerages have published HOA fees of around $388 per month including water; that figure is third-party-reported, so treat it as unverified until the association confirms current dues in writing. My full explainer on [how water letters work in Costa Rica](https://soldbytiago.com/blog/costa-rica-property-water-letter-guide/) applies doubly to any lot purchase here.

## Building at Las Ventanas

Most purchases are lot-plus-build. The community has design guidelines; their current text, approval process and any build-time rules are not fully published, so request them directly before offering. Then run the standard land checks - survey, access, setbacks, permits - from my [Guanacaste land-buying checklist](https://soldbytiago.com/blog/buying-land-guanacaste-zoning-water-building-checklist/).

## What to verify before purchasing

- Current HOA dues and exactly what they cover (including the water arrangement), from the association directly
- The water concession''s status and capacity commitments for new construction
- Design guidelines and approval process for your subdivision
- The lot''s registered plano and physical boundaries ([why this matters](https://soldbytiago.com/blog/costa-rica-property-title-plano-catastrado-guide/))
- Resale context: with 73 properties, comparable sales are few - price with professional help

## Current listings nearby

My current Playa Grande listings include [Casa Flores del Mar](https://soldbytiago.com/property/casa-flores-del-mar-playa-grande/) and [Casa Uchuva](https://soldbytiago.com/property/casa-uchuva-playa-grande/). My agent''s-eye view of Las Ventanas - who it fits and its honest trade-offs - is on my [Las Ventanas community page](https://soldbytiago.com/development/las-ventanas-playa-grande/).

## Sources & Verification

- [Las Ventanas de Playa Grande - official site](https://www.ventanasplayagrande.com/) - community overview, water system, amenities
- Subdivision names, lot sizes and amenity details also appear in local brokerage materials; the ~$388/month HOA figure is brokerage-published and must be confirmed with the association
- [Las Baulas National Marine Park](https://www.sinac.go.cr/) (SINAC) - the protected area context for Playa Grande

---

**About this article.** Written for SoldByTiago by [Tiago Leao](https://soldbytiago.com/about.html), a real estate agent with KRAIN Luxury Real Estate in Guanacaste, Costa Rica. Last reviewed: July 18, 2026. This article is general education, not legal, tax, or investment advice. Rules, fees and procedures change - verify everything that matters to your purchase with a Costa Rican attorney and the official sources linked above before acting.',
        '');

-- Verify Part 1: should return 5
SELECT count(*) FROM blog_posts WHERE slug IN ('hacienda-pinilla-communities-amenities-guide', 'reserva-conchal-real-estate-communities-guide', 'senderos-tamarindo-real-estate-guide', 'tamarindo-park-real-estate-buyers-guide', 'las-ventanas-playa-grande-real-estate-guide', 'mar-vista-flamingo-real-estate-guide', 'costa-rica-property-due-diligence-checklist', 'costa-rica-property-water-letter-guide', 'costa-rica-property-title-plano-catastrado-guide', 'buying-land-guanacaste-zoning-water-building-checklist');
