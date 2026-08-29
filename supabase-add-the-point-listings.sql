-- ═══════════════════════════════════════════════════════════════
--  Add two listings at The Point, Playa Avellanas
--  Run once in the Supabase SQL Editor (Dashboard > SQL Editor).
--
--  Photos are served from this repo at /property-photos/... so they
--  go live with the next Vercel deploy — push the repo BEFORE or with
--  this insert, or the galleries will 404 until you do.
--
--  Source listings (co-broke / shared with written permission):
--    The Point 18 — lxcostarica.com/property/surf-sun-style-villa
--                   (The Agency Costa Rica / Grupo LX — Mitzam Fontiveros)
--    The Point 4  — henkelandwilliamsrealestate.com/listing/the-point-4
--                   (Team Henkel & Williams / Coldwell Banker Tamarindo)
-- ═══════════════════════════════════════════════════════════════

INSERT INTO properties
  (name, slug, price, type, status, location, address, beds, baths, size, lot,
   short_desc, description, features, photos, lat, lng, featured, sort_order)
VALUES
(
  'The Point 18',
  'the-point-18-playa-avellanas',
  '$459,000',
  'home', 'active',
  'The Point, Playa Avellanas',
  '',
  4, 3.5, 303, 330,
  'Brand-new 4-bedroom villa with an independent guest suite, steps from Playa Avellanas inside the gated community of The Point.',
  'Set inside The Point, a gated community of 28 villas roughly 300 meters from the sand at Playa Avellanas, The Point 18 is a newly built four-bedroom villa that puts world-class surf, a resort-style community pool, and Guanacaste''s most relaxed beach town within walking distance.

A Brand-New Contemporary Villa Steps From Playa Avellanas

Completed in 2023, the home offers 303 m² (3,261 sq ft) of living space on a 330 m² lot, plus a 28 m² (301 sq ft) covered parking area with two spaces. Four bedrooms and three and a half bathrooms are split between the main residence and an independent guest suite, giving the layout real flexibility for families, guests, or rental income.

Open-Concept Living That Opens to the Pool

At the center of the main residence, an open-concept living area brings the kitchen, dining, and lounge together under one bright volume. The modern kitchen is anchored by a large island that doubles as a breakfast bar and prep surface, finished with white cabinetry and high-end appliances. Floor-to-ceiling glass doors slide fully open to the terrace, pulling in sunlight, tropical breezes, and green views, and the terrace steps straight out to the community pool.

Four Bedrooms, Including a Private Guest Suite

The main residence holds three spacious bedrooms, each designed around natural light and warm, honest materials. The primary suite opens directly to the terrace through glass sliders and includes an en-suite bath with dual vanities and contemporary finishes. A separate guest suite with its own private entrance and full bathroom rounds out the home — ideal for visiting family and friends, a home office, or short-term rental income.

Life Inside The Point

The Point was developed in four planned phases and designed to sit lightly in its tropical setting. Residents share more than two acres of protected green space, walking trails, a large community pool, a yoga deck, a playground, a pet park, BBQ areas, and open-air gathering spaces, all behind 24/7 gated security. Pets are welcome.

Location: Avellanas, With Tamarindo Close By

Playa Avellanas is a few minutes'' walk away, with consistent surf, wide golden sand, and beachfront dining at Lola''s. Tamarindo and Langosta are roughly 25 to 30 minutes north, and the coming Waldorf Astoria Guanacaste, minutes from the community, should continue to lift values across this stretch of coast. Liberia International Airport (LIR) is about an hour and fifteen minutes away.

Architecturally, the villa keeps to clean lines, natural textures, and a refined tropical aesthetic — the easy, unfussy sophistication that has made Playa Avellanas one of Guanacaste''s most desirable coastal addresses.',
  ARRAY[
    'Brand New (2023)',
    'Gated Community',
    'Steps from the Beach',
    'Independent Guest Suite',
    'Open-Concept Living',
    'Floor-to-Ceiling Glass Doors',
    'Kitchen Island / Breakfast Bar',
    'High-End Appliances',
    'Dual Vanity Primary Bath',
    'Terrace / Patio',
    'Community Pool',
    'Yoga Deck',
    'Playground',
    'Pet Park',
    'BBQ Area',
    'Walking Trails',
    'Protected Green Space',
    '24/7 Security',
    'Pets Allowed',
    'Split A/C Units',
    'Cross-Ventilation',
    '2 Covered Parking Spaces'
  ],
  ARRAY[
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/01-aerial-6.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/02-entrance-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/03-living-room-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/04-living-room-2.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/05-dining-room-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/06-kitchen-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/07-kitchen-2.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/08-kitchen-4.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/09-terrace-2.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/10-terrace-3.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/11-master-bedroom-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/12-master-bathroom-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/13-master-bathroom-2.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/14-shower-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/15-secondary-bedroom-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/16-secondary-bedroom-2.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/17-secondary-bedroom-3.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/18-secondary-bedroom-4.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/19-secondary-bedroom-5.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/20-secondary-bathroom-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/21-secondary-bathroom-2.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/22-social-area-2.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/23-social-area-6.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/24-view-1.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/25-aerial-4.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/26-aerial-2.jpg',
    'https://soldbytiago.com/property-photos/the-point-18-avellanas/27-playa-avellanas-1.jpg'
  ],
  10.236993, -85.833148,
  FALSE,
  (SELECT COALESCE(MAX(sort_order), 0) + 1 FROM properties)
),
(
  'The Point 4',
  'the-point-4-playa-avellanas',
  '$365,000',
  'home', 'active',
  'The Point, Playa Avellanas',
  '',
  2, 2, 105, 223,
  'Turnkey, fully furnished 2-bedroom villa with a proven vacation-rental track record, minutes from Playa Avellanas.',
  'The Point 4 is a fully furnished, turnkey two-bedroom villa inside The Point, the gated community just minutes from the sand at Playa Avellanas. It is already operating as a high-performing vacation rental, which makes it one of the more straightforward entry points into Guanacaste beach real estate at this price.

Turnkey and Move-In Ready

Professionally designed and sold fully furnished, the 105 m² home sits on a 223 m² lot with two bedrooms and two bathrooms. Contemporary tropical architecture meets relaxed coastal living here: soaring ceilings, expansive glass, and an open-concept layout that connects the indoor living spaces to lush tropical gardens and shaded outdoor entertaining areas. Warm natural finishes, mature landscaping, and abundant natural light give the property a private, quiet feel.

A Proven Rental Performer

This is not a projection. The villa has an established track record as a vacation rental, with strong occupancy, excellent guest reviews, and visibility across the major booking platforms. For a buyer who wants income from day one without a renovation or furnishing project, that history is the point.

Gated Community Amenities

Ownership at The Point includes 24/7 security, a large community pool, and beautifully landscaped common areas set against Costa Rica''s natural surroundings.

Location: Minutes From Avellanas Surf and Dining

The home is a short distance from the surf, beaches, and beachfront restaurants of Playa Avellanas, and stays within easy reach of Tamarindo and Daniel Oduber Quirós International Airport (LIR) in Liberia.

Turnkey convenience, modern tropical design, proven rental performance, and a prime beachside location — an unusually complete package in one of Costa Rica''s most sought-after coastal destinations.',
  ARRAY[
    'Turnkey',
    'Fully Furnished',
    'Proven Vacation Rental',
    'Gated Community',
    'Close to the Beach',
    'High Ceilings',
    'Open-Concept Living',
    'Expansive Glass',
    'Tropical Gardens',
    'Outdoor Entertaining Area',
    'Community Pool',
    'Landscaped Common Areas',
    '24/7 Security'
  ],
  ARRAY[
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/01.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/02.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/03.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/04.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/05.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/06.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/07.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/08.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/09.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/10.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/11.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/12.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/13.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/14.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/15.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/16.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/17.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/18.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/19.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/20.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/21.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/22.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/23.jpg',
    'https://soldbytiago.com/property-photos/the-point-4-avellanas/24.jpg'
  ],
  10.236993, -85.833148,
  FALSE,
  (SELECT COALESCE(MAX(sort_order), 0) + 2 FROM properties)
);

-- Verify
SELECT name, slug, price, beds, baths, size, lot, array_length(photos, 1) AS photo_count, sort_order
FROM properties
WHERE slug IN ('the-point-18-playa-avellanas', 'the-point-4-playa-avellanas');
