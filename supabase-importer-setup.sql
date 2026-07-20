-- ============================================================
-- KRAIN → SoldByTiago property importer: private draft/audit table.
-- Run ONCE in the Supabase SQL Editor. Idempotent.
--
-- Design notes:
--  * The public `properties` table stays the single source of truth for
--    the website — this table holds ONLY private importer state: drafts,
--    the raw source snapshot, the authorization/permission record, image
--    provenance, validation results, sync diffs and an append-only history.
--  * PRIVATE table: RLS on, NO anon policies at all. Only authenticated
--    (logged-in admin) users can read or write. The public site never
--    touches it.
-- ============================================================

CREATE TABLE IF NOT EXISTS property_imports (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- workflow
  import_status TEXT DEFAULT 'imported' CHECK (import_status IN
    ('imported','needs_review','ready','published','update_available','archived')),

  -- source identity
  source_url TEXT NOT NULL,
  source_provider TEXT DEFAULT '',        -- 'krain-lp' | 'krain-idx' | 'propertyshelf' | ...
  source_listing_id TEXT DEFAULT '',      -- provider's internal id (LP page UUID)
  source_mls_id TEXT DEFAULT '',          -- e.g. RS2600630
  source_agent TEXT DEFAULT '',
  source_brokerage TEXT DEFAULT '',
  source_updated_at TEXT DEFAULT '',      -- as reported by source; '' = not provided

  -- authorization / compliance record (internal, never rendered publicly)
  permission_scope TEXT DEFAULT '' CHECK (permission_scope IN
    ('', 'own_listing','krain_exclusive','brokerage_approved','mls_syndication','written_permission')),
  permission_note TEXT DEFAULT '',
  images_authorized BOOLEAN DEFAULT FALSE,
  description_authorized BOOLEAN DEFAULT FALSE,
  sync_authorized BOOLEAN DEFAULT FALSE,
  authorization_confirmed BOOLEAN DEFAULT FALSE,  -- the "I confirm I am authorized…" checkbox
  imported_by TEXT DEFAULT '',            -- auth email of the importing user

  -- data
  source_snapshot JSONB,                  -- adapter output at import time (normalized, untouched)
  draft JSONB,                            -- editable working copy (properties-row shape + extras)
  validation JSONB,                       -- latest validation run [{level,code,message}]
  images JSONB DEFAULT '[]'::jsonb,       -- [{source_url, original_url, display_url, selected, hero, alt, width, height, bytes, status, error}]
  history JSONB DEFAULT '[]'::jsonb,      -- append-only [{at,user,event,details}]

  -- publish linkage
  published_property_id UUID REFERENCES properties(id) ON DELETE SET NULL,
  published_at TIMESTAMPTZ,
  published_by TEXT DEFAULT '',

  -- sync
  last_sync_check TIMESTAMPTZ,
  sync_diff JSONB,                        -- latest field-by-field diff awaiting approval

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Fast duplicate lookups
CREATE INDEX IF NOT EXISTS property_imports_source_url_idx ON property_imports (lower(source_url));
CREATE INDEX IF NOT EXISTS property_imports_source_listing_idx ON property_imports (source_listing_id);
CREATE INDEX IF NOT EXISTS property_imports_mls_idx ON property_imports (source_mls_id);
CREATE INDEX IF NOT EXISTS property_imports_status_idx ON property_imports (import_status);

ALTER TABLE property_imports ENABLE ROW LEVEL SECURITY;

-- Authenticated-only access. Deliberately NO anon/public policy: this table
-- holds internal compliance records and source snapshots.
DROP POLICY IF EXISTS "Auth can select imports" ON property_imports;
CREATE POLICY "Auth can select imports"
  ON property_imports FOR SELECT TO authenticated USING (true);
DROP POLICY IF EXISTS "Auth can insert imports" ON property_imports;
CREATE POLICY "Auth can insert imports"
  ON property_imports FOR INSERT TO authenticated WITH CHECK (true);
DROP POLICY IF EXISTS "Auth can update imports" ON property_imports;
CREATE POLICY "Auth can update imports"
  ON property_imports FOR UPDATE TO authenticated USING (true);
DROP POLICY IF EXISTS "Auth can delete imports" ON property_imports;
CREATE POLICY "Auth can delete imports"
  ON property_imports FOR DELETE TO authenticated USING (true);
