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

-- APPLIED 2026-07-14. Safe to re-run; it is idempotent.
--
-- Do NOT drop policies by name here. The live database had a second set of
-- open policies under different names ("insert blog", "update blog", ...),
-- so name-based DROPs silently matched nothing while this script still
-- reported "Success" — and Postgres ORs permissive policies together, so the
-- new restrictive ones below changed nothing. The site stayed writable by
-- anyone. Match on what a policy DOES instead.

-- RLS must actually be on, or every policy below is ignored entirely.
ALTER TABLE properties ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;

-- Drop every public/anon WRITE policy, whatever it happens to be named.
-- SELECT policies are left alone so the public site keeps working.
DO $$
DECLARE r record;
BEGIN
  FOR r IN
    SELECT schemaname, tablename, policyname
    FROM pg_policies
    WHERE ((schemaname = 'public'  AND tablename IN ('properties','blog_posts'))
        OR (schemaname = 'storage' AND tablename = 'objects'))
      AND cmd IN ('INSERT','UPDATE','DELETE','ALL')
      AND ('public' = ANY(roles) OR 'anon' = ANY(roles))
  LOOP
    EXECUTE format('DROP POLICY %I ON %I.%I', r.policyname, r.schemaname, r.tablename);
    RAISE NOTICE 'dropped %.% : %', r.schemaname, r.tablename, r.policyname;
  END LOOP;
END $$;

-- Public read stays as-is (site visitors can still see everything)

-- Writes: only authenticated (logged-in) users.
-- Each is dropped first so the whole script can be re-run safely.
DROP POLICY IF EXISTS "Auth can insert properties" ON properties;
CREATE POLICY "Auth can insert properties"
  ON properties FOR INSERT TO authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "Auth can update properties" ON properties;
CREATE POLICY "Auth can update properties"
  ON properties FOR UPDATE TO authenticated USING (true);
DROP POLICY IF EXISTS "Auth can delete properties" ON properties;
CREATE POLICY "Auth can delete properties"
  ON properties FOR DELETE TO authenticated USING (true);

DROP POLICY IF EXISTS "Auth can insert blog posts" ON blog_posts;
CREATE POLICY "Auth can insert blog posts"
  ON blog_posts FOR INSERT TO authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "Auth can update blog posts" ON blog_posts;
CREATE POLICY "Auth can update blog posts"
  ON blog_posts FOR UPDATE TO authenticated USING (true);
DROP POLICY IF EXISTS "Auth can delete blog posts" ON blog_posts;
CREATE POLICY "Auth can delete blog posts"
  ON blog_posts FOR DELETE TO authenticated USING (true);

DROP POLICY IF EXISTS "Auth can upload photos" ON storage.objects;
CREATE POLICY "Auth can upload photos"
  ON storage.objects FOR INSERT TO authenticated WITH CHECK (bucket_id = 'photos');
DROP POLICY IF EXISTS "Auth can update photos" ON storage.objects;
CREATE POLICY "Auth can update photos"
  ON storage.objects FOR UPDATE TO authenticated USING (bucket_id = 'photos');
DROP POLICY IF EXISTS "Auth can delete photos" ON storage.objects;
CREATE POLICY "Auth can delete photos"
  ON storage.objects FOR DELETE TO authenticated USING (bucket_id = 'photos');

-- Verify: every row should read "authenticated", except SELECT rows ("public").
--   SELECT tablename, policyname, cmd, array_to_string(roles, ',') AS roles
--   FROM pg_policies
--   WHERE (schemaname='public'  AND tablename IN ('properties','blog_posts'))
--      OR (schemaname='storage' AND tablename='objects')
--   ORDER BY tablename, cmd;
