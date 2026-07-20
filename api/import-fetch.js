// POST /api/import-fetch  { url }
// Auth: Authorization: Bearer <Supabase access token of the logged-in admin>.
// Fetches ONE admin-submitted listing URL from an allowlisted source domain,
// runs the matching source adapter, and returns normalized listing JSON.
// Never writes anywhere; all persistence happens in the admin's browser
// under their authenticated Supabase session.
'use strict';

const lib = require('./_lib/importer.js');

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.status(405).json({ ok: false, error: 'POST only.' });
    return;
  }

  const token = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  const user = await lib.verifyAdminToken(token);
  if (!user) {
    res.status(401).json({ ok: false, error: 'Sign in to the admin first.' });
    return;
  }
  if (!lib.rateLimit(`fetch:${user.id}`, 20, 60_000)) {
    res.status(429).json({ ok: false, error: 'Too many imports in a row — wait a minute and try again.' });
    return;
  }

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  const rawUrl = body && body.url;
  if (!rawUrl) {
    res.status(400).json({ ok: false, error: 'Missing "url".' });
    return;
  }

  const check = await lib.validateUrl(rawUrl, lib.PAGE_HOSTS);
  if (!check.ok) {
    res.status(400).json({ ok: false, error: check.error });
    return;
  }

  const adapter = lib.findAdapter(check.url);
  if (!adapter) {
    res.status(422).json({ ok: false, error: 'This KRAIN listing format is not currently supported.' });
    return;
  }
  if (!adapter.supported) {
    res.status(422).json({ ok: false, error: adapter.reason, source_type: adapter.id, source_label: adapter.label });
    return;
  }

  let page;
  try {
    page = await lib.safeFetch(check.url, lib.PAGE_HOSTS, {
      timeoutMs: lib.FETCH_TIMEOUT_MS,
      maxBytes: lib.MAX_HTML_BYTES,
      accept: 'text/html,application/xhtml+xml',
    });
  } catch (e) {
    const timedOut = /abort|timeout/i.test(String(e && e.name) + String(e && e.message));
    res.status(502).json({ ok: false, error: timedOut ? 'The source page timed out.' : 'Could not reach the source page.' });
    return;
  }
  if (!page.ok) {
    const gone = page.status === 404 || page.status === 410;
    res.status(502).json({
      ok: false,
      error: gone ? 'The source listing page no longer exists (removed or unpublished).' : page.error,
      source_gone: gone,
    });
    return;
  }
  if (!/html/.test(page.contentType)) {
    res.status(422).json({ ok: false, error: `Expected an HTML page, got ${page.contentType || 'unknown content'}.` });
    return;
  }

  let extracted;
  try {
    extracted = adapter.extract(page.body.toString('utf-8'), check.url);
  } catch (e) {
    console.error('adapter extract failed:', adapter.id, e && e.message);
    res.status(422).json({ ok: false, error: 'This KRAIN listing format is not currently supported.' });
    return;
  }

  // A page that yields neither a name nor any images is a format change —
  // refuse rather than import partial data silently.
  if (!extracted.listing.name && extracted.images.length === 0) {
    res.status(422).json({ ok: false, error: 'This KRAIN listing format is not currently supported.' });
    return;
  }

  res.status(200).json({
    ok: true,
    source_type: adapter.id,
    source_label: adapter.label,
    fetched_by: user.email,
    final_url: page.finalUrl,
    ...extracted,
  });
};
