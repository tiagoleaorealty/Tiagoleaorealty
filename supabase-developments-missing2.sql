-- RECOVERY: the original seed run lost its last two INSERTs.
-- This restores Pacifico and Reserva de Golf with the enriched content.
-- Safe to re-run.

INSERT INTO developments (name, slug, town, match_location, established, price_range, amenities, beach_access, rental_rules, best_for, excerpt, meta_desc, body, sort_order, status)
VALUES ('Pacifico',
        'pacifico-playas-del-coco',
        'Playas del Coco',
        'Pacifico',
        '2009',
        'Condos from ~$200Ks; homesites from under $100K (asking)',
        'Beachfront Beach Club with shuttle, four lagoon pools, multi-sport complex, fitness center, NIMBU boat club, Village Shops with full supermarket',
        'Private beachfront club on Playas del Coco with resident shuttle',
        'Vacation rentals common; rules vary by sub-association - verify per unit',
        'Rental investors and convenience-first buyers',
        'Playas del Coco''s flagship community - 400+ condos, townhomes and homesites with a beachfront club, boat club, and one of the most complete amenity stacks on the northern coast.',
        'Pacifico Playas del Coco guide: 400+ residences, beachfront Beach Club, four lagoon pools, Village Shops at the gate, real entry prices and trade-offs.',
        'Pacifico is the community that changed how people think about Playas del Coco - a full resort-style neighborhood established in 2009 on about 175 acres, now counting more than 400 residences and one of the most complete amenity stacks on the northern coast.

## The layout

The mix runs from the Na Umi seaside condominiums - five buildings that were the community''s first ocean-view condos - through townhomes and the four-bedroom Bosque Tropic Village homes, up to the Mira estate section at the community''s highest point, where homes reach roughly 6,500 square feet. In all: roughly 240 condos and townhomes plus around 150 homesites, in Mediterranean-influenced coastal architecture.

## The amenities

Four huge free-form lagoon pools meander between the condo buildings. A renovated multi-sport complex covers tennis, pickleball, basketball and mini-soccer, alongside a fitness center. Ownership includes access to the beachfront Pacifico Beach Club - two infinity pools at the sand, a 60-seat air-conditioned restaurant and the Alma Santa kitchen, with shuttle service from the community - plus the NIMBU boat club for getting on the water. At the entrance, the Village Shops put about 25,600 square feet of daily life at the gate: cafés, restaurants (including a Hard Rock Cafe), offices and a full-size supermarket.

## Prices and entry points

Condos have been advertised from around the low $200,000s and homesites from under $100,000 into the mid-$500,000s (asking prices; phases and inventory change - I confirm live availability). For a gated community with a private beachfront club, those are meaningful entry points.

## The town at your gate

Playas del Coco is one of the most established beach towns on the northern coast - a real, year-round community with banks, clinics, pharmacies and restaurants, not a strip that empties in green season. For families, the town also has schooling covered: [Dolphins Academy](https://soldbytiago.com/school/dolphins-academy/) and [Pacífico Internacional](https://soldbytiago.com/school/pacifico-internacional/) both operate in Coco, and both are profiled on my schools page.

## Who it fits

Rental-focused buyers first: 25 to 30 minutes from Liberia airport, a real working town at the gate, and beach-club branding make Pacifico one of the strongest turnkey rental setups in the region. Also first-time buyers and anyone prioritizing convenience over seclusion.

## Honest considerations

This is a large, active community: expect neighbors, rental guests, and an HOA structure scaled to the shared amenities. Fee schedules vary by sub-association, so the same square footage can carry different monthly costs in different buildings - I confirm current figures per unit before any offer. And Coco itself is a working town with real energy: a plus for most buyers, a minus if what you wanted was silence.

## Alternatives to compare

[Las Catalinas](https://soldbytiago.com/development/las-catalinas/) for walkability and architecture, [Reserva Conchal](https://soldbytiago.com/development/reserva-conchal/) for hotel-anchored resort living, [Catalina Cove](https://soldbytiago.com/development/catalina-cove/) for land at lower density.',
        9,
        'published')
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location, established = EXCLUDED.established, price_range = EXCLUDED.price_range, amenities = EXCLUDED.amenities, beach_access = EXCLUDED.beach_access, rental_rules = EXCLUDED.rental_rules, best_for = EXCLUDED.best_for, excerpt = EXCLUDED.excerpt, meta_desc = EXCLUDED.meta_desc, body = EXCLUDED.body, sort_order = EXCLUDED.sort_order, status = EXCLUDED.status;

INSERT INTO developments (name, slug, town, match_location, amenities, beach_access, construction_rules, best_for, excerpt, meta_desc, body, sort_order, status)
VALUES ('Reserva de Golf',
        'reserva-de-golf-hacienda-pinilla',
        'Hacienda Pinilla',
        'Reserva de Golf',
        'All Hacienda Pinilla amenities - golf, Beach Club, equestrian, tennis, trails - plus its own gated entry and circular central park',
        'Walking distance to both Playa Avellanas and Playa Langosta',
        'No time restriction on building - buy and hold, or build immediately',
        'Golf-front living inside Hacienda Pinilla',
        'The golf-course neighborhood inside Hacienda Pinilla - 136 lots along holes 4, 5 and 6, walking distance to both Avellanas and Langosta.',
        'Reserva de Golf guide: the 136-lot neighborhood inside Hacienda Pinilla on holes 4-6, walkable to Avellanas and Langosta - lots, governance, trade-offs.',
        'Reserva de Golf is a neighborhood inside Hacienda Pinilla rather than a standalone community - 136 lots wrapped around holes 4, 5 and 6 of the resort''s Mike Young-designed golf course, with its own gated entry, paved roads, central park and established homeowners association.

## The geography

Its quiet superpower: it sits almost exactly between Playa Avellanas to the south and Playa Langosta to the north, close enough to walk to either - a combination almost nothing else in Pinilla offers. Lots face either the fairways or the neighborhood''s circular central park with its fountain and mature tropical landscaping, so there is no forgotten back row.

## What you get

Inside-the-resort economics with neighborhood scale. Owning here means every Pinilla amenity - the par-72, Audubon-designated golf course with its oceanfront stretch, the beachfront Beach Club, the equestrian center, tennis, the trail network, the JW Marriott''s restaurants and spa - while buying into a defined 136-lot community with stable, established dues rather than estate-scale costs.

And unlike some sections of the resort, Reserva de Golf has no time restriction on building: land buyers can build immediately or hold as long as they want, which makes it one of the cleanest land-banking plays inside Pinilla.

## Homes and lots available

The neighborhood spans two decades of construction vintages, from early builds to brand-new contemporary homes, plus remaining lots facing golf or park. That mix keeps a range of price points alive inside a resort otherwise known for its top end - and it means there is usually something to look at here, whether you want finished or ground-up.

## Who it fits

Golfers first - fairway frontage on a course you can play daily is the point. Buyers who want Pinilla''s full infrastructure at a more contained, neighborly scale. And investors who like the neighborhood''s rental track record: it is one of the more consistently rented sections of the resort.

## Honest considerations

You are subject to two layers of governance - the neighborhood HOA and the master resort - so understand both fee schedules and rule sets before committing; I put current numbers in front of every buyer. Construction vintages vary, so older homes may need updating to rent at the top of the market. And while both beaches are walkable, the Beach Club, the Pinilla Market and the JW Marriott''s restaurants are still a short drive across the resort. Tamarindo is about 20 minutes; Liberia airport is a bit over an hour.

## Alternatives to compare

Elsewhere in [Hacienda Pinilla](https://soldbytiago.com/development/hacienda-pinilla/) for beachfront or estate lots, [Senderos](https://soldbytiago.com/development/senderos-tamarindo/) for build-new near Tamarindo, [Reserva Conchal](https://soldbytiago.com/development/reserva-conchal/) for hotel-resort amenities.',
        10,
        'published')
ON CONFLICT (slug) DO UPDATE SET
  name = EXCLUDED.name, town = EXCLUDED.town, match_location = EXCLUDED.match_location, amenities = EXCLUDED.amenities, beach_access = EXCLUDED.beach_access, construction_rules = EXCLUDED.construction_rules, best_for = EXCLUDED.best_for, excerpt = EXCLUDED.excerpt, meta_desc = EXCLUDED.meta_desc, body = EXCLUDED.body, sort_order = EXCLUDED.sort_order, status = EXCLUDED.status;

-- Verify: should return 10 rows
SELECT sort_order, slug, status FROM developments ORDER BY sort_order;