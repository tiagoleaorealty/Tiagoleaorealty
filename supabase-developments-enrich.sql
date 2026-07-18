-- ENRICHED COMMUNITY WRITE-UPS - run once in Supabase SQL Editor.
-- Expands all 8 development pages with researched, attributed detail
-- and fills public sidebar facts. Safe to re-run.
-- (Pacifico and Reserva de Golf were removed from the lineup 2026-07-18.)
BEGIN;

UPDATE developments SET
  body = 'Hacienda Pinilla is the community I sell in more than any other, so consider this the insider version.

It is a 4,500-acre gated resort south of Tamarindo with roughly three miles of Pacific coastline - big enough that it fronts four different beaches, each with its own personality. Playa Avellanas on the south end is one of Guanacaste''s most celebrated surf breaks, home of the beach restaurant half the coast drives to on weekends. Playa Mansita, in front of the JW Marriott, is the calm, swimmable family beach. Playa Bonita is the quiet one in between, and Playa Langosta marks the northern edge, minutes from Tamarindo. Very few buyers realize one property covers all four.

## The golf

The 18-hole course was designed by Mike Young - par 72, stretching to about 7,200 yards from the back tees, with its signature stretch running along the ocean. It holds an Audubon Cooperative Sanctuary designation for its conservation work, and it is set up to be playable rather than punishing: there is a nine-hole option, a practice area with balls included, a pro shop and a bar-restaurant at the clubhouse. Current rates and tee times are published on [the resort''s golf page](https://www.haciendapinilla.com/golf.html).

## The rest of the amenity stack

The beachfront Beach Club anchors social life; around it sit tennis and pickleball courts, a full equestrian center, a network of mountain-bike and hiking trails threading the tropical dry forest, and the Pinilla Market for everyday basics. The JW Marriott Guanacaste inside the gates adds hotel restaurants and a spa a few minutes from any neighborhood.

## What makes it different

Scale and maturity. Pinilla has been building since the 1990s, so you are buying into an established community with real infrastructure, a functioning HOA structure, and - crucially - a genuine resale market. It is not one product but a collection of distinct neighborhoods: beachfront estates, golf-course homes wrapped right around the fairways, condo sections, and titled homesites for buyers who want to build.

Several of my current listings are in Pinilla, from around $2.6M to $5.3M, which tells you the core segment: this is the blue-chip end of the coast - though condos and building lots trade well below that.

## Who it fits

Buyers who want resort infrastructure without a resort crowd - Pinilla is quiet, spread out, and residential in feel. Golfers, obviously. Families who want a surf beach and a calm beach in the same zip code. And anyone who wants strong rental fundamentals with luxury finish: the vacation-rental market here is deep and well established.

## Honest considerations

Distances inside the property are real - you will drive to the Beach Club, to golf, and to town. Tamarindo''s restaurants are about 20 minutes away, and Liberia airport is a bit over an hour. HOA fees, rental rules and construction guidelines vary by neighborhood and change over time; I confirm current figures for the specific section before any offer, so ask.

## Alternatives to compare

[Reserva Conchal](https://soldbytiago.com/development/reserva-conchal/) for a more hotel-anchored resort feel, [Mar Vista](https://soldbytiago.com/development/mar-vista/) for larger lots at lower entry prices, [Senderos](https://soldbytiago.com/development/senderos-tamarindo/) for build-new living five minutes from Tamarindo.',
  meta_desc = 'Hacienda Pinilla guide from a local agent: 4,500 acres, four beaches, Mike Young golf, Beach Club, JW Marriott, homes and lots, and the honest trade-offs.',
  best_for = 'Golfers, luxury buyers, established rental investors',
  amenities = 'Mike Young 18-hole golf (par 72), beachfront Beach Club, tennis & pickleball, equestrian center, spa, mountain-bike and hiking trails, Pinilla Market, JW Marriott inside the gates',
  beach_access = 'Four beaches inside the property - Avellanas, Mansita, Bonita and Langosta - plus a beachfront Beach Club',
  established = '1990s',
  rental_rules = 'Vacation rentals well established; rules vary by neighborhood - confirm per section'
WHERE slug = 'hacienda-pinilla';

UPDATE developments SET
  body = 'Reserva Conchal is one of the most complete resort communities on this coast - and easily the most hotel-anchored, which depending on the buyer is either exactly the point or the reason to look next door.

The numbers first: roughly 2,300 acres (about 930 hectares) rising behind Playa Conchal, the crushed-shell beach that shows up on every list of Costa Rica''s finest. Inside the gates: a Robert Trent Jones II championship golf course - 7,021 yards, par 71, an Audubon-certified sanctuary since 2001 - a private beach club directly on Conchal''s sand, a spa, gym and trail network, and two international hotels, the all-inclusive Westin and the W Costa Rica.

## Seventeen neighborhoods, one master plan

Residential Conchal is organized into seventeen sub-communities named for native trees and flowers - Bougainvillea, Malinche, Roble Sabana, Jobo, Carao, Guayacan and the rest - each with its own character, its own administration, and its own fee structure. The range runs from golf-view condos and townhomes to custom ocean-view estates and building lots. Current-generation projects include the Sanara residences (28 units in the latest phase), the Laurel forest-view lots, and Solaris, the newest condominium project.

Local brokerages list condos from the mid-$500,000s for smaller units to more than $2 million for ocean-view penthouses (asking prices; the mix changes constantly - I confirm live inventory before you fall in love with a floor plan).

## The beach and the club

Playa Conchal is named for what it is made of - millions of crushed shells that give the water its clarity - and the community''s private Beach Club sits directly on that sand, so your beach day starts on one of the country''s most photographed beaches. Club life comes with pools, dining, and spa and gym access, and because the Westin and W operate inside the same gates, owners tap hotel-grade restaurants, service staff and event infrastructure that a purely residential community could never sustain.

## The school, quietly the killer feature

[CRIA](https://soldbytiago.com/school/costa-rica-international-academy/) - the U.S.-accredited international school - is 500 meters from the entrance, which makes Conchal one of the most practical choices on this coast for relocating families. A five-minute school run does not exist anywhere else at this level of community. There is a full CRIA profile on my schools page.

## Who it fits

Buyers who want turnkey, amenity-rich ownership with strong rental branding - the Westin and W give owner rentals real marketing gravity - plus families anchoring on CRIA, and golfers who want a championship course as their home track.

## Honest considerations

You are inside a resort: expect resort pacing, resort rules, and fee schedules designed around a hospitality operation. Concierge-managed communities carry meaningful HOA and club costs, and each of the seventeen sub-communities prices differently - I confirm the current fee schedule, club access terms and rental program rules for the specific section before any offer.

## Getting there

Under an hour from Liberia international airport; Flamingo and Brasilito are about ten minutes away, with the new Flamingo marina just up the road.

## Alternatives to compare

[Hacienda Pinilla](https://soldbytiago.com/development/hacienda-pinilla/) for more land and a quieter feel, [Mar Vista](https://soldbytiago.com/development/mar-vista/) next door for large private lots, [Las Catalinas](https://soldbytiago.com/development/las-catalinas/) for walkable-town living instead of resort living.',
  meta_desc = 'Reserva Conchal guide: 2,300 acres behind Playa Conchal, Robert Trent Jones II golf, Westin and W hotels, 17 neighborhoods, prices and honest trade-offs.',
  best_for = 'Turnkey resort buyers and relocating families (CRIA next door)',
  amenities = 'Robert Trent Jones II golf (par 71, Audubon-certified), private Beach Club on Playa Conchal, Westin & W hotels, spa, gym, trails',
  beach_access = 'Private beach club directly on Playa Conchal',
  price_range = 'Condos from the mid-$500Ks to $2M+ penthouses (asking)',
  rental_rules = 'Owner rental programs available; terms vary by sub-community - confirm per unit'
WHERE slug = 'reserva-conchal';

UPDATE developments SET
  body = 'Senderos is the answer to a question Tamarindo buyers kept asking: how do I live five minutes from town without living *in* town?

It is a roughly 110-acre gated community in the hills above Tamarindo - one of only a handful of true gated communities here - with sweeping views over the Pacific, the estuary, and the Las Baulas National Marine Park. Much of what you see from the ridge is protected parkland, which is the closest thing a view has to a warranty on this coast. The development''s own numbers: five minutes to Tamarindo''s beach and restaurants, about 1.8 km to the sand, and roughly an hour to Liberia airport.

## Puerta de Sal - the beach club

This is the piece that changed the equation. Puerta de Sal, the community''s private beach club, opened in late 2025 where the estuary meets the ocean: an oceanfront pool, dining by Pangas, a spa treatment room, concierge and towel service, firepits, hanging swings, shaded lounges and direct access to the sand. Membership is deliberately limited, and it gives Senderos owners something almost nothing in central Tamarindo offers - a private foothold on the water.

## The community itself

Homes follow Senderos'' "Natural Modern" design principles through a roster of vetted architects, so build quality and architectural coherence are unusually high for this coast. Inside the gates: resort-style pools, tennis, a gym, kilometers of walking trails winding through green spaces and art installations, organic gardens, playgrounds and a dog park, with a sports-and-wellness Valley Club planned.

At the entrance sits the Garden Plaza, home to Automercado - the largest supermarket in the area - and the region''s only movie theater. The daily-logistics problem that plagues most hillside communities is solved at the gate.

## Homes and lots available

Most of the inventory is homesites - generous ones, many in the half-acre range, with ocean, valley or forest orientations - which you pair with one of the community''s vetted architects to design and build. Finished architect-designed villas do come to market as early owners resell, but they move quickly; if you want finished rather than ground-up, tell me early and I will watch for it.

## Who it fits

Buyers who want walkable-ish proximity to Tamarindo''s restaurants and surf with privacy, security and views - especially those planning to build a serious home rather than inherit someone else''s compromises. It also suits families: the gate, the trails and the playgrounds make it one of the few genuinely kid-friendly setups this close to town, and both [Educarte](https://soldbytiago.com/school/educarte/) and [Journey School](https://soldbytiago.com/school/journey-school-tamarindo/) are minutes away.

## Honest considerations

Much of Senderos is still build-out: you are often buying a homesite plus a construction project, with design guidelines to follow - a feature for long-term coherence, but a commitment in time and attention. HOA fees, beach-club membership terms and rental rules come from the developer''s current schedule; I confirm them per lot before any offer.

## Alternatives to compare

[Tamarindo Park](https://soldbytiago.com/development/tamarindo-park/) next door in the Langosta hills for the newer version of the same idea, [Hacienda Pinilla](https://soldbytiago.com/development/hacienda-pinilla/) for resort-scale maturity ten minutes south, or a finished home in central Tamarindo if you want zero construction wait.',
  meta_desc = 'Senderos Tamarindo guide: gated hillside community with the Puerta de Sal beach club, Natural Modern architecture, half-acre homesites and honest trade-offs.',
  best_for = 'Build-your-own buyers who want privacy five minutes from town',
  amenities = 'Puerta de Sal private beach club, resort pools, tennis, gym, trails, organic gardens, playgrounds, dog park, Garden Plaza with Automercado and cinema at the entrance',
  beach_access = 'About 1.8 km to Playa Tamarindo; private Puerta de Sal beach club at the estuary mouth',
  construction_rules = '"Natural Modern" design code with vetted architects'
WHERE slug = 'senderos-tamarindo';

UPDATE developments SET
  body = 'Tamarindo Park is the newest of Tamarindo''s gated communities, carved into the reforested hillside that connects Tamarindo to Playa Langosta - the last large piece of undeveloped land between the two.

The site covers about 37 hectares (91 acres), and the developer has committed to keeping roughly 75% of it natural, leaning on reforestation, permaculture and regenerative-agriculture practices rather than maximum-density planning. The master plan calls for around 220 tropical-contemporary homes, delivered in phases.

## The Hilltop - Phase I

The first phase sits at the community''s entrance, perched on a hilltop with ocean views and about a ten-minute walk from the beach and downtown Tamarindo. It launched with 32 homes plus a first release of building lots, and the developer reports the first thirteen homes already delivered.

Every house is designed under Richard Müller, one of Costa Rica''s most established residential architects. His homes here run four to eight bedrooms and are tailored to each homesite - often designed around existing trees rather than through them. KRAIN, my brokerage, has represented turnkey homes in the Hilltop collection, so I have seen the build quality up close.

## Amenities - phased

The plan includes a wellness and fitness center, a sports club, an ocean-view sunset club, paddle courts, a community garden, hiking and mountain-bike trails, and a small commercial space. As with any young community, these arrive in stages - my advice is always to buy on what is delivered plus what is contractually committed, not on renderings.

## What makes it different

Position and design pedigree. The site sits between the two beaches, so you are minutes from both Tamarindo''s energy and Langosta''s quiet - and because it is a ground-up master plan under a single architect rather than an accumulation of lots, the finished community will have an architectural consistency closer to Senderos or Las Catalinas than to an older subdivision. The 75% preservation commitment is also unusual at this scale.

## Who it fits

Early buyers who want new construction at pre-build-out pricing in a location that cannot be replicated - there is no more undeveloped hillside between Tamarindo and Langosta. Also buyers who care about the sustainability posture, and families: Tamarindo''s international schools, [Educarte](https://soldbytiago.com/school/educarte/) and [Journey School](https://soldbytiago.com/school/journey-school-tamarindo/), are both a short drive away.

## Honest considerations

This is a young development: you are betting on execution. That bet has upside - early phases of successful communities on this coast have historically been rewarded - but it is a different risk profile from buying into a 20-year-old neighborhood. Delivery timelines, HOA structure and rental rules come from the current developer documents; I walk through them with buyers before any commitment.

## Alternatives to compare

[Senderos](https://soldbytiago.com/development/senderos-tamarindo/) for the more established version of the same idea, Playa Langosta itself for finished beachside homes, [Hacienda Pinilla](https://soldbytiago.com/development/hacienda-pinilla/) for resort-scale maturity.',
  meta_desc = 'Tamarindo Park guide: the new Richard Müller-designed gated community between Tamarindo and Langosta - Hilltop phase, amenities, lots and honest trade-offs.',
  best_for = 'Early buyers who want new construction between two beaches',
  amenities = 'Planned in phases: wellness & fitness center, sports club, ocean-view sunset club, paddle courts, community garden, hiking and mountain-bike trails',
  beach_access = 'About a 10-minute walk from the Hilltop to Tamarindo beach and town',
  established = '2020s',
  construction_rules = 'Richard Müller-designed homes; developer plan keeps ~75% of the site natural'
WHERE slug = 'tamarindo-park';

UPDATE developments SET
  body = 'Las Ventanas is the low-density outlier of this coast: 380 acres holding just 73 properties, spread across nine small subdivisions on the panoramic ridge between Playa Grande and Playa Conchal.

That ratio - over five acres of land per property - is the whole story. The quintas of La Sabana run 1.2 to 2.26 acres each. El Roble''s sites look straight out over the Catalinas islands. The remaining subdivisions - Caracara, El Camino, Catalinas, Altamar, Jaguarundi, San Pedro and Cenizaros - stair-step across the ridge, each holding just a handful of properties. Around seventy people live here full-time, which gives Ventanas something rare among view communities: an actual neighborhood, not a rental compound.

## Self-sufficiency, engineered

The community runs its own concessioned water well - a far bigger deal in seasonally dry Guanacaste than most buyers realize - and the water cost is folded into the HOA. Local brokerages publish fees around $388 per month including water (verify current figures; fees change). Roads are paved throughout, the gate is staffed 24/7, and the infrastructure was clearly built for the long haul rather than the sales brochure.

## Amenities

The west-facing clubhouse sits in La Sabana near the top of Cerro Almendro: an infinity pool, sunset views over the Pacific, and the community''s natural gathering point. Around it are a tennis and pickleball court, a soccer field, a skate park and playground, more than five kilometers of jungle trails, and a community organic garden planted with some 150 fruiting trees plus medicinal plants and herbs. For a 73-property community, that is an unusually complete list.

## The setting

Playa Grande - one of Costa Rica''s most consistent surf beaches, inside the Las Baulas National Marine Park - is minutes in one direction; Playa Conchal''s white shell sand is minutes in the other. Liberia airport is about 50 minutes. You sit on elevated land between two of the coast''s marquee beaches while paying ridge-land prices rather than beachfront ones.

## Homes and lots available

Inventory is a mix of finished hillside homes, quintas with standing houses, and raw acreage lots across the nine subdivisions. With only 73 properties in existence, listings are structurally scarce - at any given time a handful of options exist, which is exactly why owners here tend to hold. Most purchases are still lot-plus-build, with community design guidelines to follow.

## Who it fits

Buyers who want land, views and quiet over walk-to-dinner convenience - especially full-time relocators, families (the skate park, playground and garden are used daily), and builders who want real acreage without ranch-level remoteness.

## Honest considerations

You will drive for everything: beaches, groceries, restaurants. Building here means working within the community''s design guidelines and managing a construction project remotely or in person. And low density cuts both ways - fewer neighbors also means fewer comparables when you eventually sell, so pricing a resale takes more work.

## Alternatives to compare

[Mar Vista](https://soldbytiago.com/development/mar-vista/) for a larger community with similar lot sizes and more amenities, Playa Grande town for surf-first living closer to the sand, [Hacienda Pinilla](https://soldbytiago.com/development/hacienda-pinilla/) for amenities at scale.',
  meta_desc = 'Las Ventanas de Playa Grande guide: 380 acres, 73 properties, nine subdivisions, its own water supply, ocean-view clubhouse - and the honest trade-offs.',
  best_for = 'Land, views and quiet - full-time relocators and builders',
  amenities = 'Ocean-view clubhouse with infinity pool, tennis & pickleball, soccer field, skate park, playground, community organic garden, 5+ km of jungle trails, private water well',
  beach_access = 'Short drive to both Playa Grande and Playa Conchal (no walk-to-beach)',
  hoa_fees = '~$388/month including water (published by local brokers - verify current)'
WHERE slug = 'las-ventanas-playa-grande';

UPDATE developments SET
  body = 'Mar Vista is the community families keep landing on once they map the school run - [La Paz Community School''s Cabo Velas campus](https://soldbytiago.com/school/la-paz-community-school-cabo-velas/) sits at its entrance, and no other large community on this coast can say that. The school is bilingual and profiled in full on my schools page; for relocating parents, having it inside the community''s front door changes the entire daily equation.

The development covers about 750 acres on the hillside between Brasilito and Playa Flamingo, looking over Conchal bay, the Catalinas islands and the new Flamingo marina. Four neighborhoods share the land - three of them built around lots averaging 5,000 m², roughly 1.25 acres - and about a third of the total acreage is committed as nature preserve, so the green in the views stays green.

## Infrastructure first

This is Mar Vista''s quiet flex: more than 30 kilometers of paved internal roads, underground utilities throughout, and 24/7 gated security. Underground power matters more here than buyers expect - it is rarer than it should be on this coast, and it changes both the sightlines and the storm-season experience.

## The clubhouse and amenities

The clubhouse anchors community life: an infinity-edge pool with a swim-up bar, Gracia - the onsite restaurant with ocean views - a fitness center, a yoga pavilion, a game room and a playground. Outside: night-lit clay tennis courts, eight pickleball courts, and groomed hiking and biking trails running through the preserved terrain.

## Homes and lots available

Mar Vista is a mix of finished custom homes, homes under construction, and titled building lots, so buyers can enter at very different points: buy land and design from scratch, or buy a completed home with the infrastructure already proven. Land entry prices generally sit below the beachfront resort communities nearby.

## Getting there and getting around

Brasilito''s beach town is at the bottom of the hill, Flamingo and its recently opened full-service marina are a few minutes up the road, and Playa Conchal is a short drive - three very different beaches inside a ten-minute circle. Liberia international airport is under an hour.

## Who it fits

Relocating families first - school at the gate, space to breathe, and a genuine village of other families around you. And buyers who want to build a substantial home on real acreage while keeping resort-town conveniences within that ten-minute circle.

## Honest considerations

Mar Vista is still building out; parts of it are lots and construction rather than finished streetscape. It sits on the hillside, not the sand - beach trips are a short drive, not a stroll. HOA fees and build guidelines come from the current community documents; I confirm them per neighborhood before any offer.

## Alternatives to compare

[Las Ventanas](https://soldbytiago.com/development/las-ventanas-playa-grande/) for even lower density, [Catalina Cove](https://soldbytiago.com/development/catalina-cove/) for a smaller, established version of the big-lot idea, [Reserva Conchal](https://soldbytiago.com/development/reserva-conchal/) for resort amenities instead of acreage.',
  meta_desc = 'Mar Vista guide: 750 acres between Brasilito and Flamingo - 5,000 m² lots, serious infrastructure, clubhouse dining, La Paz school onsite, honest trade-offs.',
  best_for = 'Relocating families (La Paz onsite) and acreage builders',
  amenities = 'Clubhouse with infinity pool & swim-up bar, Gracia restaurant, fitness center, yoga pavilion, night-lit clay tennis, 8 pickleball courts, hiking & biking trails, La Paz school campus onsite',
  beach_access = 'Short drive to Brasilito, Flamingo and Conchal beaches'
WHERE slug = 'mar-vista';

UPDATE developments SET
  body = 'Catalina Cove is the quiet achiever of the Brasilito corridor - established in 2005, roughly 40 hectares, and organized around genuinely oversized lots: about 73 parcels averaging 5,000 m² plus 29 more around 2,000 m².

Twenty years of growth means mature trees, wildlife corridors, settled paved roads, and a real mix of full-time residents alongside vacation homes - the kind of lived-in feel new developments spend a decade chasing.

## Walk to two beaches

The community sits behind Playa Brasilito - a Blue Flag beach with a working beach town attached - about a ten-minute walk from the gate, and Playa Conchal''s white shell sand is roughly a twenty-minute walk beyond that. Brasilito town brings restaurants, cafés and small groceries within strolling distance; Flamingo and its new marina are a few minutes by car. On a coast where "walk to the beach" usually costs seven figures, this is the exception.

## What it costs

Entry prices are among the most accessible of any gated community in this corridor: lots have been advertised from around $60,000 and homes from around $230,000 (asking prices; verify current availability). The HOA is modest too - local brokerages publish fees around $150 per month (verify current) - covering the gate, roads and common areas rather than a resort payroll.

## What makes it different

Accessibility, in both senses. You get gated security, big flat-ish lots and two walkable beaches at prices that simply do not exist in Flamingo, Conchal or the resort communities - because you are not paying for a golf course, a beach club or a hotel brand. For buyers who would rather own the land than rent the lifestyle, the math is compelling.

## Who it fits

First-time Costa Rica buyers who want gated security and land without resort pricing; builders who want a large lot in an established neighborhood with the infrastructure already settled; and buyers priced out of Flamingo or Conchal who still want that ten-minute circle around them.

## Honest considerations

There is no beach club, golf course or resort amenity stack here - this is a residential neighborhood, full stop, and your recreation happens at the beaches and in town. Homes span twenty years of construction styles, so quality varies house to house. As always, I confirm current dues and any build guidelines before an offer. Liberia airport is just under an hour away.

## Alternatives to compare

[Mar Vista](https://soldbytiago.com/development/mar-vista/) up the hill for grander infrastructure and the school, [Las Ventanas](https://soldbytiago.com/development/las-ventanas-playa-grande/) for view acreage, Surfside in Potrero for a beach-town grid with a similar value profile.',
  meta_desc = 'Catalina Cove guide: established Brasilito community from 2005 - oversized lots, low HOA, walk to two beaches, real entry prices and honest trade-offs.',
  best_for = 'First-time Costa Rica buyers - value, land and walkability',
  amenities = '24/7 gated entry, paved roads, mature trees and green areas - residential by design, no resort amenity stack',
  beach_access = '~10-minute walk to Playa Brasilito; ~20-minute walk to Playa Conchal',
  price_range = 'Lots from ~$60K; homes from ~$230K (asking - verify current)',
  hoa_fees = '~$150/month (published by local brokers - verify current)',
  rental_rules = 'Vacation rentals present throughout the community - confirm current rules'
WHERE slug = 'catalina-cove';

UPDATE developments SET
  body = 'Las Catalinas is not a gated community in the normal sense - it is a purpose-built, car-free beach town, and there is nothing else like it in Central America.

The story matters here. Atlanta entrepreneur Charles Brewer acquired this stretch of coast in the mid-2000s and set out to build a New Urbanist town - a place where daily life happens on foot and where streets, plazas and public spaces matter as much as the homes. Two decades on, the result is around 180 residences and growing, hotels including Santarena and the adults-only Casa Chameleon, restaurants, cafés, shops and offices stacked in Mediterranean-inspired streets that rise straight from the sand of Playa Danta. Cars stay parked at the edge of town; luggage moves by porter and everything else moves on foot or by bike.

## The trails and the beaches

Behind the town, roughly 1,000 acres of protected tropical dry forest carry a 42-kilometer network of hiking, running and mountain-biking trails - among the most extensive community trail systems in the country. Playa Danta out front is calm and swimmable, with paddleboards and kayaks in constant rotation, and Playa Dantita is a short walk north. The Beach Club adds an ocean-view lap pool, a kids'' pool, a lounging pool and a hot plunge.

## Homes available

The range runs from one-bedroom flats to full townhomes and villas, all built to the town''s architectural code. Flats have historically entered around the $400,000s, with townhomes and villas from $1 million to well past $5 million (asking prices; the market moves - I confirm current inventory). Short-term rentals are an established part of the town''s economy, with a formal rental program many owners use - the walkability and trail network give rentals here genuine differentiation.

## Who it fits

Buyers who value urbanism over acreage: no lawn, no car errands, neighbors close by design. You wake up, walk to coffee, walk to the beach, walk to dinner - a lifestyle simply unavailable anywhere else on this coast. It works equally well as a full-time home, a lock-and-leave, or a rental property with a story to tell.

## Honest considerations

Density is the point, so privacy is architectural rather than spatial. Rental and design rules are structured and firm - that protects the town''s coherence, but it is a rulebook you should read before buying, and I go through it with every client. Costs reflect the shared-town infrastructure. And while the town covers daily needs, bigger shopping runs mean driving toward Flamingo or Potrero.

## Alternatives to compare

Nothing directly comparable exists here. Flamingo offers walkable-ish beach living with cars, [Senderos](https://soldbytiago.com/development/senderos-tamarindo/) offers gated hillside living near a real town, and [Reserva Conchal](https://soldbytiago.com/development/reserva-conchal/) offers resort-style amenities behind one of the country''s most famous beaches.

There is a fuller town guide on my [Las Catalinas community page](https://soldbytiago.com/las-catalinas.html).',
  meta_desc = 'Las Catalinas guide: Costa Rica''s car-free beach town on Playa Danta - the architecture, Beach Club, 42 km of trails, prices and honest trade-offs.',
  best_for = 'Walkable-town lovers and design-driven buyers',
  amenities = 'Beach Club pools, 42 km hiking & mountain-bike trail network, plazas, restaurants, shops, hotels, car-free streets',
  beach_access = 'The town fronts Playa Danta; Playa Dantita is a short walk north',
  established = 'Mid-2000s',
  price_range = 'Flats from the ~$400Ks; villas $1M-$5M+ (asking)',
  rental_rules = 'Short-term rentals well established; formal town rental program - rules apply',
  construction_rules = 'Town architectural code governs all construction'
WHERE slug = 'las-catalinas';

COMMIT;

-- Verify: every row should show a body of 2,800+ characters
SELECT slug, length(body) AS body_chars, best_for FROM developments ORDER BY sort_order;