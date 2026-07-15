-- ═══════════════════════════════════════════════════════════════
--  SCHOOLS + PROPERTY SCORES — Tiago Leao Real Estate
--  Run this once in Supabase Dashboard > SQL Editor.
--
--  Adds:
--    1. A `schools` table (one row per campus).
--    2. Three score columns on `properties` (walk / beach / airport).
--    3. Seed data for the 10 Gold Coast schools.
--
--  Writes are restricted to logged-in users from the start, matching
--  supabase-security.sql. Do not loosen these to `public`.
-- ═══════════════════════════════════════════════════════════════

-- ── 1. Schools table ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS schools (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL DEFAULT '',
  slug TEXT UNIQUE DEFAULT '',
  -- Canonical town string, matching the wording used in properties.location
  -- so school pages and community pages can cross-link.
  town TEXT DEFAULT '',
  address TEXT DEFAULT '',
  -- Free text, not an enum: these vary too much to constrain.
  grades TEXT DEFAULT '',
  curriculum TEXT DEFAULT '',
  languages TEXT DEFAULT '',
  accreditation TEXT DEFAULT '',
  tuition TEXT DEFAULT '',
  founded TEXT DEFAULT '',
  website TEXT DEFAULT '',
  -- Pinned via the satellite map in the admin. Nearby-school lookups on a
  -- property page are computed from these, so an unpinned school (NULL)
  -- is simply skipped rather than placed at 0,0 off the coast of Africa.
  lat DOUBLE PRECISION,
  lng DOUBLE PRECISION,
  excerpt TEXT DEFAULT '',
  meta_desc TEXT DEFAULT '',
  body TEXT DEFAULT '',
  cover_url TEXT DEFAULT '',
  photos TEXT[] DEFAULT '{}',
  status TEXT DEFAULT 'published' CHECK (status IN ('draft','published')),
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Defined in supabase-setup.sql, but recreated here so this script stands
-- alone if the tables were ever rebuilt without it.
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS schools_updated_at ON schools;
CREATE TRIGGER schools_updated_at
  BEFORE UPDATE ON schools
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ── 2. Property score columns ─────────────────────────────────
-- NULL means "not measured" and the tile is hidden, which is different
-- from 0. Do not default these to 0.
ALTER TABLE properties ADD COLUMN IF NOT EXISTS walk_score INTEGER;
ALTER TABLE properties ADD COLUMN IF NOT EXISTS beach_minutes INTEGER;
ALTER TABLE properties ADD COLUMN IF NOT EXISTS beach_mode TEXT;   -- 'walk' | 'drive'
ALTER TABLE properties ADD COLUMN IF NOT EXISTS airport_minutes INTEGER;

-- ── 3. Row level security ─────────────────────────────────────
ALTER TABLE schools ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Public can read published schools" ON schools;
CREATE POLICY "Public can read published schools"
  ON schools FOR SELECT USING (status = 'published');

DROP POLICY IF EXISTS "Auth can insert schools" ON schools;
CREATE POLICY "Auth can insert schools"
  ON schools FOR INSERT TO authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "Auth can update schools" ON schools;
CREATE POLICY "Auth can update schools"
  ON schools FOR UPDATE TO authenticated USING (true);
DROP POLICY IF EXISTS "Auth can delete schools" ON schools;
CREATE POLICY "Auth can delete schools"
  ON schools FOR DELETE TO authenticated USING (true);

-- ── 4. Seed the 10 schools ────────────────────────────────────
-- Every value below is quoted from each school's own website (fetched
-- 2026-07-14). Blank = the school does not publish it. Nothing here is
-- estimated — if it is not on their site, it is empty on purpose.
-- lat/lng are intentionally NULL: Costa Rican addresses do not geocode
-- reliably, so each campus gets pinned by hand in the admin.
INSERT INTO schools (name, slug, town, address, grades, curriculum, languages, accreditation, tuition, founded, website, excerpt, sort_order)
VALUES
  ('Costa Rica International Academy (CRIA)', 'costa-rica-international-academy', 'Brasilito',
   '500 meters south of Reserva Conchal, Brasilito, Guanacaste',
   'Early Years – Secondary', 'U.S.-accredited bilingual', 'English and Spanish', 'US and MEP accredited', '', '2000',
   'https://criacademy.com/',
   'U.S.-accredited bilingual school on a 32-acre campus near Reserva Conchal, serving the Gold Coast since 2000.', 1),

  ('La Paz Community School — Cabo Velas Campus', 'la-paz-community-school-cabo-velas', 'Brasilito',
   '400 meters east of the entrance to the Mar Vista project, Brasilito, Cabo Velas, Santa Cruz, Guanacaste',
   'PreK – 12', 'International Baccalaureate (IB), experiential learning', 'Bilingual dual-language immersion',
   'IB World School; ACEP; College Board', '', '',
   'https://www.lapazschool.org/en/',
   'IB World School between Flamingo and Brasilito, built around dual-language immersion and experiential learning.', 2),

  ('La Paz Community School — Tempisque Campus', 'la-paz-community-school-tempisque', 'Palmira',
   '300 northwest from Do IT Center Lagar entrance to Papagayo, Comunidad, Palmira, Carrillo, Guanacaste',
   'PreK – 12', 'International Baccalaureate (IB), experiential learning', 'Bilingual dual-language immersion',
   'IB World School; ACEP; College Board', '', '',
   'https://www.lapazschool.org/en/',
   'La Paz''s second campus, inland near Palmira in Carrillo, running the same IB dual-language program.', 3),

  ('Journey School of Costa Rica — Tamarindo', 'journey-school-tamarindo', 'Tamarindo',
   '300 metros norte de JSM, Tamarindo, Santa Cruz, Guanacaste',
   'Pre-K – 12', 'International Baccalaureate (IB), project-based learning', 'Spanish and English',
   'IB; Middle States Association; MEP; UNESCO Associated Schools Network; Council of International Schools', '', '',
   'https://journeyschoolofcostarica.com/',
   'Authorized IB World School in Tamarindo offering the IB Diploma Programme with project-based learning.', 4),

  ('Del Mar Academy', 'del-mar-academy', 'Nosara',
   'Nosara, Guanacaste',
   'Pre-K – 12', 'Montessori through IB Diploma Programme', 'Spanish and English',
   'IB World School; MEP', '', '',
   'https://www.delmaracademy.com/',
   'Nosara IB World School on an 11-acre campus, running Montessori in the early years into the IB Diploma.', 5),

  ('Educarte', 'educarte', 'Huacas',
   '3km del cruce de Huacas hacia Villa Real, La Garita, Guanacaste',
   'Preescolar – Secundaria', 'Bilingual, MEP-certified', 'Spanish and English',
   'MEP certified; Programa Bandera Azul', '$125 per month (preescolar and primaria)', '',
   'https://educartecostarica.com/inicio',
   'Bilingual MEP-certified school near Huacas, and the only school on this list that publishes its tuition.', 6),

  ('Lakeside International School', 'lakeside-international-school', 'Sardinal',
   'Tablazo de Sardinal, Carrillo, Guanacaste',
   'PreK – 12', 'Integrated curriculum, Multiple Intelligences model', 'English and Spanish',
   'Ecological Blue Flag', '', '',
   'https://www.lakeside.school/',
   'Bilingual PreK–12 school inland from Playas del Coco, built on an integrated Multiple Intelligences curriculum.', 7),

  ('Pacífico Internacional', 'pacifico-internacional', 'Villareal',
   '300m oeste y 50m norte del Eco lodge El Sabanero, Cañafistula, Villareal, Santa Cruz, Guanacaste',
   'Preschool – middle school', 'Waldorf-inspired', 'Bilingual', '', '', '',
   'https://waldorf.cr/',
   'Waldorf-inspired school in the hills at Cañafistula, just inland from Tamarindo.', 8),

  ('TIDE Academy', 'tide-academy', 'Tamarindo',
   'Tamarindo, Guanacaste', '', '', '', '', '', '',
   'https://www.tideacademy.com/',
   'Tamarindo school built for students whose interests run past a conventional academic structure — roughly 80 students from 17 countries, at an 8:1 student-teacher ratio.', 9),

  ('Dolphin''s Academy', 'dolphins-academy', 'Playas del Coco',
   'Playas del Coco, Guanacaste',
   'Elementary', 'Bilingual', 'Bilingual', 'Curricula in alliance with Oxford University and Cambridge University', '', '',
   'https://www.dolphinsacademycr.com/',
   'Bilingual elementary school in Playas del Coco, with curricula developed in alliance with Oxford and Cambridge.', 10)
ON CONFLICT (slug) DO NOTHING;
