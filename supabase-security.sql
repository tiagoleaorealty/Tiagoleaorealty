-- ═══════════════════════════════════════════════════════════════
--  SECURITY LOCKDOWN — Tiago Leao Real Estate
--  Run this in Supabase Dashboard > SQL Editor
--
--  WHY: The current policies let ANYONE with the public site key
--  insert/update/delete properties, blog posts, and photos.
--  This restricts writes to a logged-in admin user only.
--
--  BEFORE RUNNING:
--  1. In Supabase Dashboard > Authentication > Users, click
--     "Add user" and create a user with your email + a strong
--     password. This will be your admin login.
--  2. Tell Claude the user is created, so admin.html gets a real
--     login form wired to Supabase Auth (writes will fail from
--     the admin panel until that is done).
-- ═══════════════════════════════════════════════════════════════

-- Drop the wide-open write policies
DROP POLICY IF EXISTS "Admin can insert properties"  ON properties;
DROP POLICY IF EXISTS "Admin can update properties"  ON properties;
DROP POLICY IF EXISTS "Admin can delete properties"  ON properties;
DROP POLICY IF EXISTS "Admin can insert blog posts"  ON blog_posts;
DROP POLICY IF EXISTS "Admin can update blog posts"  ON blog_posts;
DROP POLICY IF EXISTS "Admin can delete blog posts"  ON blog_posts;
DROP POLICY IF EXISTS "Anyone can upload photos"     ON storage.objects;
DROP POLICY IF EXISTS "Anyone can update photos"     ON storage.objects;
DROP POLICY IF EXISTS "Anyone can delete photos"     ON storage.objects;

-- Public read stays as-is (site visitors can still see everything)

-- Writes: only authenticated (logged-in) users
CREATE POLICY "Auth can insert properties"
  ON properties FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Auth can update properties"
  ON properties FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Auth can delete properties"
  ON properties FOR DELETE TO authenticated USING (true);

CREATE POLICY "Auth can insert blog posts"
  ON blog_posts FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Auth can update blog posts"
  ON blog_posts FOR UPDATE TO authenticated USING (true);
CREATE POLICY "Auth can delete blog posts"
  ON blog_posts FOR DELETE TO authenticated USING (true);

CREATE POLICY "Auth can upload photos"
  ON storage.objects FOR INSERT TO authenticated WITH CHECK (bucket_id = 'photos');
CREATE POLICY "Auth can update photos"
  ON storage.objects FOR UPDATE TO authenticated USING (bucket_id = 'photos');
CREATE POLICY "Auth can delete photos"
  ON storage.objects FOR DELETE TO authenticated USING (bucket_id = 'photos');
