// Edge Middleware — legacy property URLs.
//
// /property-detail.html?id=<uuid>  →  308 to /property/<slug>/  (query DROPPED)
// Unknown uuid-format ids          →  real 404
// Non-uuid ids (slugs passed as id)→  308 to /property/<id>/
// No id at all                     →  fall through (the template is also the
//                                     internal rewrite target for clean URLs)
//
// vercel.json keeps equivalent query redirects as a fallback; middleware runs
// first on Vercel, so destinations from here carry no query string.
// Regenerate the map from Supabase if property ids ever change.

const ID_TO_SLUG = {
  "e4f7876f-6226-4e3b-b576-3def68102ca4": "casa-coyote-playas-del-coco",
  "843a8b0b-910d-4bc7-91cb-e78fb71870a5": "casa-flores-del-mar-playa-grande",
  "f785fcd1-a6e9-4191-97b4-5be64cbb4c57": "enclave-c5-playa-avellanas",
  "47978e51-8443-46c7-9ed9-9c647c9a63ae": "villa-calypso-tamarindo",
  "29562190-c1b0-483c-974b-3014656d3df5": "casa-uchuva-playa-grande",
  "7239fe66-32d5-4b90-a21f-44f3c749d39f": "casa-hanna-tamarindo",
  "56bb618c-5571-4cce-ad83-04b82026e0f9": "multi-home-property-playa-avellanas",
  "f46ee5c9-f438-44d6-a22b-c852eea40500": "diria-512-tamarindo",
  "00ad65c3-5ec2-44a7-ac76-ee933af9b3ee": "mareas-iii-hacienda-pinilla",
  "12fcb6c9-4088-404b-9092-a061cf067e16": "villa-las-brisas-29-hacienda-pinilla",
  "37bf40df-3bbf-4aff-8566-76fbcbcf9303": "mareas-i-hacienda-pinilla",
  "adef907b-5eff-4c56-814e-079adb714c36": "casa-golondrinas-hacienda-pinilla",
  "e6552762-7495-459f-8bdb-7ccc0fbca9c0": "casa-hijau-marbella",
  "262abf92-5ce0-4514-89e1-1d49996c2288": "casa-nya-hacienda-pinilla"
};

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export const config = { matcher: "/property-detail.html" };

export default function middleware(request) {
  const url = new URL(request.url);
  const id = url.searchParams.get("id");
  if (!id) return; // bare template request: let routing continue untouched

  const slug = ID_TO_SLUG[id];
  if (slug) {
    return Response.redirect(new URL("/property/" + slug + "/", url.origin), 308);
  }
  if (UUID_RE.test(id)) {
    // A uuid we have never issued: a true 404, not a soft redirect.
    return new Response("Not found", { status: 404 });
  }
  // Anything else is treated as a slug typed into the old parameter.
  return Response.redirect(new URL("/property/" + encodeURIComponent(id) + "/", url.origin), 308);
}
