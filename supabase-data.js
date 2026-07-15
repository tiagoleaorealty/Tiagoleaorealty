// ═══════════════════════════════════════════════════════════════
//  Supabase Data Loader — shared by all public pages
//  Reads config from localStorage (set by admin panel)
// ═══════════════════════════════════════════════════════════════

(function() {
  'use strict';

  const DEFAULT_SB_URL = 'https://xjliwfmugylwxlrwyvmh.supabase.co';
  const DEFAULT_SB_KEY = 'sb_publishable_YHOe_eAJzuWpzbFD_tO-4A_vuvnSHum';
  const DEFAULT_MAPBOX_KEY = 'pk.eyJ1IjoidGlhZ29sZWFvcmVhbHR5IiwiYSI6ImNtcThwNHVqcDBjNm0yc3BxZ3Njc25tcXkifQ.BBoP6va0fmx0mRdLZ2_tzw';

  const SB_URL = localStorage.getItem('tl_sb_url') || DEFAULT_SB_URL;
  const SB_KEY = localStorage.getItem('tl_sb_key') || DEFAULT_SB_KEY;

  if (!SB_URL || !SB_KEY) {
    console.log('[Supabase] No config found — using static content');
    return;
  }

  // Escape HTML special chars so DB text can never inject markup/scripts
  // when pages render it via innerHTML (XSS protection).
  function escapeHTML(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function sanitize(value) {
    if (typeof value === 'string') return escapeHTML(value);
    if (Array.isArray(value)) return value.map(sanitize);
    if (value && typeof value === 'object') {
      const out = {};
      for (const k of Object.keys(value)) out[k] = sanitize(value[k]);
      return out;
    }
    return value;
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
    return sanitize(await res.json());
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

    // Load all published schools
    async getSchools() {
      try {
        return await sbFetch('schools', {
          'status': 'eq.published',
          'order': 'sort_order.asc,name.asc',
          'select': '*'
        });
      } catch (e) {
        console.error('[Supabase] Failed to load schools:', e);
        return null;
      }
    },

    // Load a single published school by slug
    async getSchool(slug) {
      try {
        const data = await sbFetch('schools', {
          'slug': `eq.${slug}`,
          'status': 'eq.published',
          'select': '*'
        });
        return data && data.length > 0 ? data[0] : null;
      } catch (e) {
        console.error('[Supabase] Failed to load school:', e);
        return null;
      }
    },

    // Straight-line km between two lat/lng points (haversine). Used to pick the
    // schools nearest a listing. Deliberately not sold as a drive time —
    // Guanacaste roads bend around rivers and hills, so the real drive is
    // always longer than this number.
    distanceKm(lat1, lng1, lat2, lng2) {
      const R = 6371;
      const toRad = d => d * Math.PI / 180;
      const dLat = toRad(lat2 - lat1);
      const dLng = toRad(lng2 - lng1);
      const a = Math.sin(dLat / 2) ** 2 +
                Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
      return 2 * R * Math.asin(Math.sqrt(a));
    },

    // The `limit` schools closest to a point, each with a `distance_km` added.
    // Schools with no pin are skipped rather than treated as 0,0.
    async getNearbySchools(lat, lng, limit = 3) {
      if (lat == null || lng == null) return [];
      const schools = await this.getSchools();
      if (!schools) return [];
      return schools
        .filter(s => s.lat != null && s.lng != null)
        .map(s => ({ ...s, distance_km: this.distanceKm(+lat, +lng, +s.lat, +s.lng) }))
        .sort((a, b) => a.distance_km - b.distance_km)
        .slice(0, limit);
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

    // Load published client reviews (About page)
    async getReviews() {
      try {
        return await sbFetch('reviews', {
          'status': 'eq.published',
          'order': 'sort_order.asc,created_at.desc',
          'select': '*'
        });
      } catch (e) {
        // A 404 means the reviews table has not been created yet — an expected
        // state, not a failure. about.html falls back to its built-in reviews.
        // Only shout about errors that are actually wrong.
        if (/404/.test(e.message)) {
          console.info('[Supabase] No reviews table yet — using the built-in reviews.');
        } else {
          console.error('[Supabase] Failed to load reviews:', e);
        }
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
