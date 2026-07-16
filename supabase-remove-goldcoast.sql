-- Remove 'Gold Coast' from the database. Supabase does the edits in place.
-- Slugs/URLs stay unchanged (permanent). Safe to run once.

-- 1. Two post titles (set explicitly)
UPDATE blog_posts SET title = 'Guanacaste''s Beach Towns: Tamarindo, Flamingo, Conchal, Potrero & Nosara'
  WHERE slug = 'guanacaste-gold-coast-towns-guide';
UPDATE blog_posts SET title = 'Schools in Guanacaste: A Guide for Relocating Families'
  WHERE slug = 'schools-guanacaste-gold-coast-guide';

-- 2. Schools
UPDATE schools SET
  excerpt = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(excerpt, 'Nosara is not on the Gold Coast in any practical sense', 'Nosara sits apart from the rest of the coast'), 'the Gold Coast of Guanacaste', 'the beach towns of Guanacaste'), 'the Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste''s Gold Coast', 'Guanacaste'), 'Costa Rica''s Gold Coast', 'Guanacaste'), 'on the Gold Coast', 'in Guanacaste'), 'of the Gold Coast', 'of Guanacaste'), 'the Gold Coast', 'this coast'), 'Gold Coast', 'Guanacaste'),
  body    = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(body, 'Nosara is not on the Gold Coast in any practical sense', 'Nosara sits apart from the rest of the coast'), 'the Gold Coast of Guanacaste', 'the beach towns of Guanacaste'), 'the Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste''s Gold Coast', 'Guanacaste'), 'Costa Rica''s Gold Coast', 'Guanacaste'), 'on the Gold Coast', 'in Guanacaste'), 'of the Gold Coast', 'of Guanacaste'), 'the Gold Coast', 'this coast'), 'Gold Coast', 'Guanacaste')
WHERE excerpt ILIKE '%gold coast%' OR body ILIKE '%gold coast%';

-- 3. Blog posts
UPDATE blog_posts SET
  excerpt   = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(excerpt, 'Nosara is not on the Gold Coast in any practical sense', 'Nosara sits apart from the rest of the coast'), 'the Gold Coast of Guanacaste', 'the beach towns of Guanacaste'), 'the Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste''s Gold Coast', 'Guanacaste'), 'Costa Rica''s Gold Coast', 'Guanacaste'), 'on the Gold Coast', 'in Guanacaste'), 'of the Gold Coast', 'of Guanacaste'), 'the Gold Coast', 'this coast'), 'Gold Coast', 'Guanacaste'),
  meta_desc = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(meta_desc, 'Nosara is not on the Gold Coast in any practical sense', 'Nosara sits apart from the rest of the coast'), 'the Gold Coast of Guanacaste', 'the beach towns of Guanacaste'), 'the Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste''s Gold Coast', 'Guanacaste'), 'Costa Rica''s Gold Coast', 'Guanacaste'), 'on the Gold Coast', 'in Guanacaste'), 'of the Gold Coast', 'of Guanacaste'), 'the Gold Coast', 'this coast'), 'Gold Coast', 'Guanacaste'),
  body      = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(body, 'Nosara is not on the Gold Coast in any practical sense', 'Nosara sits apart from the rest of the coast'), 'the Gold Coast of Guanacaste', 'the beach towns of Guanacaste'), 'the Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste''s Gold Coast', 'Guanacaste'), 'Costa Rica''s Gold Coast', 'Guanacaste'), 'on the Gold Coast', 'in Guanacaste'), 'of the Gold Coast', 'of Guanacaste'), 'the Gold Coast', 'this coast'), 'Gold Coast', 'Guanacaste')
WHERE excerpt ILIKE '%gold coast%' OR meta_desc ILIKE '%gold coast%' OR body ILIKE '%gold coast%';

-- 4. Listings
UPDATE properties SET description = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(description, 'Nosara is not on the Gold Coast in any practical sense', 'Nosara sits apart from the rest of the coast'), 'the Gold Coast of Guanacaste', 'the beach towns of Guanacaste'), 'the Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste Gold Coast', 'Guanacaste'), 'Guanacaste''s Gold Coast', 'Guanacaste'), 'Costa Rica''s Gold Coast', 'Guanacaste'), 'on the Gold Coast', 'in Guanacaste'), 'of the Gold Coast', 'of Guanacaste'), 'the Gold Coast', 'this coast'), 'Gold Coast', 'Guanacaste')
WHERE description ILIKE '%gold coast%';

-- Verify: should return no rows.
SELECT 'schools' t, name FROM schools WHERE body ILIKE '%gold coast%' OR excerpt ILIKE '%gold coast%'
UNION ALL SELECT 'blog', title FROM blog_posts WHERE body ILIKE '%gold coast%' OR title ILIKE '%gold coast%' OR excerpt ILIKE '%gold coast%' OR meta_desc ILIKE '%gold coast%'
UNION ALL SELECT 'prop', name FROM properties WHERE description ILIKE '%gold coast%';
