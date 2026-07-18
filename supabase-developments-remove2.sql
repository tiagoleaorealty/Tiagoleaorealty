-- REMOVE Pacifico and Reserva de Golf from the communities system,
-- and update the two write-ups that linked to them. Safe to re-run.
BEGIN;

DELETE FROM developments WHERE slug IN ('pacifico-playas-del-coco','reserva-de-golf-hacienda-pinilla');

UPDATE developments SET body = 'Hacienda Pinilla is the community I sell in more than any other, so consider this the insider version.

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

[Reserva Conchal](https://soldbytiago.com/development/reserva-conchal/) for a more hotel-anchored resort feel, [Mar Vista](https://soldbytiago.com/development/mar-vista/) for larger lots at lower entry prices, [Senderos](https://soldbytiago.com/development/senderos-tamarindo/) for build-new living five minutes from Tamarindo.'
WHERE slug = 'hacienda-pinilla';

UPDATE developments SET body = 'Las Catalinas is not a gated community in the normal sense - it is a purpose-built, car-free beach town, and there is nothing else like it in Central America.

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

There is a fuller town guide on my [Las Catalinas community page](https://soldbytiago.com/las-catalinas.html).'
WHERE slug = 'las-catalinas';

COMMIT;

-- Verify: should return exactly 8 rows
SELECT sort_order, name, slug FROM developments ORDER BY sort_order;