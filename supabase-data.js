// ═══════════════════════════════════════════════════════════════
//  Supabase Data Loader — shared by all public pages
//  Reads config from localStorage (set by admin panel)
// ═══════════════════════════════════════════════════════════════

(function() {
  'use strict';

  const DEFAULT_SB_URL = 'https://xjliwfmugylwxlrwyvmh.supabase.co';
  const DEFAULT_SB_KEY = 'sb_publishable_YHOe_eAJzuWpzbFD_tO-4A_vuvnSHum';
  const DEFAULT_MAPBOX_KEY = 'pk.eyJ1IjoidGlhZ29sZWFvcmVhbHR5IiwiYSI6ImNtcGI2ZmJ4MzE1eDMydXExZ3dpNDRoNmsifQ.otE9ctfSu7jpJ5OmL_Ts0g';

  const SB_URL = localStorage.getItem('tl_sb_url') || DEFAULT_SB_URL;
  const SB_KEY = localStorage.getItem('tl_sb_key') || DEFAULT_SB_KEY;

  if (!SB_URL || !SB_KEY) {
    console.log('[Supabase] No config found — using static content');
    return;
  }

  // Lightweight fetch wrapper (no SDK needed for read-only)
  async function sbFetch(table, params) {
    const url = new URL(`${SB_URL}/rest/v1/${table}`);
    if (params) Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
    const res = await fetch(url, {
      headers: {
        'apikey': SB_KEY,
        'Authorization': `Bearer ${SB_KEY}`,
        'Content-Type': 'application/json'
      }
    });
    if (!res.ok) throw new Error(`Supabase fetch error: ${res.status}`);
    return res.json();
  }

  // ── Expose globally ─────────────────────────────────────────
  window.TL = {
    // Load all active properties
    async getProperties() {
      try {
        return await sbFetch('properties', {
          'status': 'eq.active',
          'order': 'sort_order.asc,created_at.desc',
          'select': '*'
        });
      } catch (e) {
        console.error('[Supabase] Failed to load properties:', e);
        return null; // null = fallback to static
      }
    },

    // Load featured properties (for homepage)
    async getFeaturedProperties() {
      try {
        return await sbFetch('properties', {
          'status': 'eq.active',
          'featured': 'eq.true',
          'order': 'sort_order.asc,created_at.desc',
          'select': '*'
        });
      } catch (e) {
        console.error('[Supabase] Failed to load featured properties:', e);
        return null;
      }
    },

    // Load a single property by ID
    async getProperty(id) {
      try {
        const data = await sbFetch('properties', {
          'id': `eq.${id}`,
          'select': '*'
        });
        return data && data.length > 0 ? data[0] : null;
      } catch (e) {
        console.error('[Supabase] Failed to load property:', e);
        return null;
      }
    },

    // Load all published blog posts
    async getBlogPosts() {
      try {
        return await sbFetch('blog_posts', {
          'status': 'eq.published',
          'order': 'created_at.desc',
          'select': '*'
        });
      } catch (e) {
        console.error('[Supabase] Failed to load blog posts:', e);
        return null;
      }
    },

    // Load a single blog post by slug
    async getBlogPost(slug) {
      try {
        const data = await sbFetch('blog_posts', {
          'slug': `eq.${slug}`,
          'select': '*'
        });
        return data && data.length > 0 ? data[0] : null;
      } catch (e) {
        console.error('[Supabase] Failed to load blog post:', e);
        return null;
      }
    },

    // Mapbox key
    getMapboxKey() {
      return localStorage.getItem('tl_mapbox_key') || DEFAULT_MAPBOX_KEY;
    },

    // Check if Supabase is configured
    isConnected() {
      return !!(SB_URL && SB_KEY);
    }
  };
})();
