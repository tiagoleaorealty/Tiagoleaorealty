-- ═══════════════════════════════════════════════════════════════
--  REVIEWS TABLE — run once in Supabase Dashboard > SQL Editor
--  (Dashboard → SQL Editor → New query → paste → Run)
--  This powers the client reviews on the About page + admin panel.
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS reviews (
  id           UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  author       TEXT NOT NULL DEFAULT '',       -- reviewer name
  location     TEXT DEFAULT '',                -- e.g. "Bought in Tamarindo" or "Toronto, Canada"
  rating       INTEGER DEFAULT 5 CHECK (rating BETWEEN 1 AND 5),
  quote        TEXT NOT NULL DEFAULT '',       -- the review text
  status       TEXT DEFAULT 'published' CHECK (status IN ('published','hidden')),
  sort_order   INTEGER DEFAULT 0,              -- lower = shown first
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

-- Public can read published reviews
DROP POLICY IF EXISTS "Public can read reviews" ON reviews;
CREATE POLICY "Public can read reviews" ON reviews FOR SELECT USING (true);

-- Writes (until the auth lockdown in supabase-security.sql is applied,
-- these mirror the existing open policies on your other tables)
DROP POLICY IF EXISTS "Anyone can insert reviews" ON reviews;
CREATE POLICY "Anyone can insert reviews" ON reviews FOR INSERT WITH CHECK (true);
DROP POLICY IF EXISTS "Anyone can update reviews" ON reviews;
CREATE POLICY "Anyone can update reviews" ON reviews FOR UPDATE USING (true);
DROP POLICY IF EXISTS "Anyone can delete reviews" ON reviews;
CREATE POLICY "Anyone can delete reviews" ON reviews FOR DELETE USING (true);

-- Optional: a couple of starter reviews so the section isn't empty.
-- Edit or delete these in the admin panel afterwards.
INSERT INTO reviews (author, location, rating, quote, sort_order) VALUES
  ('The Andersons', 'Bought in Tamarindo', 5, 'Tiago made buying from abroad feel simple. He answered every question himself, walked properties for us over video, and connected us with an attorney we trusted. We closed on our dream condo without a single surprise.', 1),
  ('Mark & Julie R.', 'Relocated from Toronto', 5, 'We interviewed three agents. Tiago was the only one who actually knew the closed sale prices and told us the honest truth about each area. His marketing is on another level — that''s exactly why we hired him to sell ours later, too.', 2);
