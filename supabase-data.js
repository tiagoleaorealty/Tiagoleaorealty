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
    // Active listings only, by default. Sold ones are opt-in via
    // getProperties({ includeSold: true }) because most callers — the town
    // pages, "You Might Also Like", the school pages — render a card that says
    // "for sale" with no Sold badge. Only the main listings grid is built to
    // show a sold home honestly.
    async getProperties(opts = {}) {
      try {
        return await sbFetch('properties', {
          'status': opts.includeSold ? 'in.(active,sold)' : 'eq.active',
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

    // Liberia international airport (Daniel Oduber Quirós, LIR) — the fixed
    // point every "how far to the airport" question is really asking about.
    LIR: { lat: 10.5933, lng: -85.5444 },

    // Driving minutes from one point to another, via Mapbox. Returns null if
    // there is no key, no route, or the request fails — callers fall back to a
    // manual value or hide the tile. This is what makes airport time automatic:
    // the pin is the only input.
    async getDriveMinutes(fromLat, fromLng, toLat, toLng) {
      const key = this.getMapboxKey();
      if (key == null || fromLat == null || fromLng == null) return null;
      try {
        // Directions, not Matrix: Matrix rejects a single A→B (it needs a 2+
        // element grid). Directions is the point-to-point route.
        const coords = `${fromLng},${fromLat};${toLng},${toLat}`;
        const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${encodeURIComponent(coords)}`
                  + `?overview=false&access_token=${key}`;
        const res = await fetch(url);
        if (!res.ok) return null;
        const data = await res.json();
        const sec = data.routes && data.routes[0] && data.routes[0].duration;
        return sec == null ? null : Math.round(sec / 60);
      } catch (e) {
        console.info('[Mapbox] Drive time unavailable:', e.message);
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
    //
    // Straight-line only — see getNearbySchoolsByDrive, which is what the
    // property pages actually use. Kept as the fallback when the routing call
    // fails, and used to shortlist candidates before routing them.
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

    // The `limit` schools nearest by ACTUAL DRIVING TIME.
    //
    // Straight-line distance is wrong on this coast, and not by a little. From
    // Playa Grande, TIDE Academy is 5.7 km away across the Tamarindo estuary —
    // which you cannot drive across. The real trip is 21 km and 38 minutes
    // around it. Ranking by crow-flies put TIDE 2nd when it is really 5th, and
    // buried CRIA, which is genuinely the closest school by road.
    //
    // One Mapbox Matrix request covers every school at once. Falls back to
    // straight-line if routing is unavailable, so the section never breaks.
    async getNearbySchoolsByDrive(lat, lng, limit = 3) {
      if (lat == null || lng == null) return [];
      const all = await this.getSchools();
      if (!all) return [];
      const pinned = all.filter(s => s.lat != null && s.lng != null);
      if (!pinned.length) return [];

      // Matrix caps at 25 coordinates per request, so shortlist by straight
      // line first. 24 is far more than the 3 we show, and cheap insurance
      // against the school list growing.
      const shortlist = pinned
        .map(s => ({ ...s, distance_km: this.distanceKm(+lat, +lng, +s.lat, +s.lng) }))
        .sort((a, b) => a.distance_km - b.distance_km)
        .slice(0, 24);

      const key = this.getMapboxKey();
      const byLine = () => shortlist.slice(0, limit);
      if (!key) return byLine();

      try {
        const coords = [[+lng, +lat], ...shortlist.map(s => [+s.lng, +s.lat])]
          .map(c => c.join(',')).join(';');
        const url = `https://api.mapbox.com/directions-matrix/v1/mapbox/driving/${encodeURIComponent(coords)}`
                  + `?sources=0&annotations=duration,distance&access_token=${key}`;
        const res = await fetch(url);
        if (!res.ok) return byLine();
        const data = await res.json();
        const durations = (data.durations && data.durations[0] || []).slice(1);
        const distances = (data.distances && data.distances[0] || []).slice(1);
        if (durations.length !== shortlist.length) return byLine();

        return shortlist
          .map((s, i) => ({
            ...s,
            // null duration = Mapbox found no road route at all.
            drive_minutes: durations[i] == null ? null : Math.round(durations[i] / 60),
            road_km: distances[i] == null ? null : distances[i] / 1000
          }))
          .filter(s => s.drive_minutes != null)
          .sort((a, b) => a.drive_minutes - b.drive_minutes)
          .slice(0, limit);
      } catch (e) {
        console.info('[Mapbox] Drive times unavailable, using straight-line distance:', e.message);
        return byLine();
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
