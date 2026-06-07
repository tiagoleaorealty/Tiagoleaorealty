-- ═══════════════════════════════════════════════════════════════
--  TIAGO LEAO REAL ESTATE — Supabase Database Setup
--  Run this in your Supabase SQL Editor (Dashboard > SQL Editor)
-- ═══════════════════════════════════════════════════════════════

-- 1. Properties table
CREATE TABLE IF NOT EXISTS properties (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL DEFAULT '',
  price TEXT DEFAULT '',
  type TEXT DEFAULT 'home' CHECK (type IN ('home','condo','villa','land','commercial')),
  status TEXT DEFAULT 'active' CHECK (status IN ('active','pending','sold')),
  location TEXT DEFAULT '',
  address TEXT DEFAULT '',
  beds NUMERIC DEFAULT 0,
  baths NUMERIC DEFAULT 0,
  size NUMERIC DEFAULT 0,
  lot NUMERIC DEFAULT 0,
  short_desc TEXT DEFAULT '',
  description TEXT DEFAULT '',
  features TEXT[] DEFAULT '{}',
  photos TEXT[] DEFAULT '{}',
  lat DOUBLE PRECISION,
  lng DOUBLE PRECISION,
  featured BOOLEAN DEFAULT FALSE,
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Blog posts table
CREATE TABLE IF NOT EXISTS blog_posts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL DEFAULT '',
  slug TEXT UNIQUE DEFAULT '',
  category TEXT DEFAULT 'market' CHECK (category IN ('market','lifestyle','guide','investment','news')),
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft','published')),
  readtime TEXT DEFAULT '',
  excerpt TEXT DEFAULT '',
  meta_desc TEXT DEFAULT '',
  body TEXT DEFAULT '',
  cover_url TEXT DEFAULT '',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Enable Row Level Security (RLS)
ALTER TABLE properties ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;

-- 4. Public read access (anyone can view published data on your site)
CREATE POLICY "Public can read active properties"
  ON properties FOR SELECT
  USING (true);

CREATE POLICY "Public can read published blog posts"
  ON blog_posts FOR SELECT
  USING (true);

-- 5. Authenticated write access (only logged-in admin can create/update/delete)
--    Using anon key + service role for admin, so we allow all for now.
--    For production, switch to auth-based policies.
CREATE POLICY "Admin can insert properties"
  ON properties FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Admin can update properties"
  ON properties FOR UPDATE
  USING (true);

CREATE POLICY "Admin can delete properties"
  ON properties FOR DELETE
  USING (true);

CREATE POLICY "Admin can insert blog posts"
  ON blog_posts FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Admin can update blog posts"
  ON blog_posts FOR UPDATE
  USING (true);

CREATE POLICY "Admin can delete blog posts"
  ON blog_posts FOR DELETE
  USING (true);

-- 6. Auto-update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER properties_updated_at
  BEFORE UPDATE ON properties
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER blog_posts_updated_at
  BEFORE UPDATE ON blog_posts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- 7. Create storage bucket for property photos
--    Go to Storage in your Supabase dashboard and create a bucket called "photos"
--    Set it to PUBLIC so images can be served directly via URL.
--    Or run this:
INSERT INTO storage.buckets (id, name, public) VALUES ('photos', 'photos', true)
  ON CONFLICT (id) DO NOTHING;

-- 8. Storage policies — allow public read, authenticated upload
CREATE POLICY "Public can view photos"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'photos');

CREATE POLICY "Anyone can upload photos"
  ON storage.objects FOR INSERT
  WITH CHECK (bucket_id = 'photos');

CREATE POLICY "Anyone can update photos"
  ON storage.objects FOR UPDATE
  USING (bucket_id = 'photos');

CREATE POLICY "Anyone can delete photos"
  ON storage.objects FOR DELETE
  USING (bucket_id = 'photos');
