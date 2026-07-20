// POST /api/import-image  { url }
// Auth: Authorization: Bearer <Supabase access token of the logged-in admin>.
// Downloads ONE authorized listing image from an allowlisted media CDN and
// returns the bytes. The admin's browser then uploads them to SoldByTiago's
// own Supabase Storage under the admin's authenticated session — the public
// site never hotlinks the source CDN.
'use strict';

const lib = require('./_lib/importer.js');

const OK_TYPES = new Set(['image/jpeg', 'image/png', 'image/webp', 'image/avif']);

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
  if (!lib.rateLimit(`img:${user.id}`, 200, 300_000)) {
    res.status(429).json({ ok: false, error: 'Image download rate limit hit — pause a few minutes.' });
    return;
  }

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  const rawUrl = body && body.url;
  if (!rawUrl) {
    res.status(400).json({ ok: false, error: 'Missing "url".' });
    return;
  }

  const check = await lib.validateUrl(rawUrl, lib.IMAGE_HOSTS);
  if (!check.ok) {
    res.status(400).json({ ok: false, error: check.error });
    return;
  }

  let img;
  try {
    img = await lib.safeFetch(check.url, lib.IMAGE_HOSTS, {
      timeoutMs: lib.IMAGE_TIMEOUT_MS,
      maxBytes: lib.MAX_IMAGE_BYTES,
      accept: 'image/*',
    });
  } catch (e) {
    const timedOut = /abort|timeout/i.test(String(e && e.name) + String(e && e.message));
    res.status(502).json({ ok: false, error: timedOut ? 'Image download timed out.' : 'Could not reach the image host.' });
    return;
  }
  if (!img.ok) {
    res.status(502).json({ ok: false, error: img.error });
    return;
  }
  if (!OK_TYPES.has(img.contentType)) {
    res.status(422).json({ ok: false, error: `Not an importable image (content-type ${img.contentType || 'unknown'}).` });
    return;
  }
  if (img.body.length < 1024) {
    res.status(422).json({ ok: false, error: 'Image is under 1 KB — likely broken or a placeholder.' });
    return;
  }

  res.setHeader('Content-Type', img.contentType);
  res.setHeader('X-Import-Source-Url', encodeURI(rawUrl).slice(0, 900));
  res.status(200).send(img.body);
};
