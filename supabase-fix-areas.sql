-- ═══════════════════════════════════════════════════════════════
--  Fix area units + the "Equiped" typo. Run once in SQL Editor.
--
--  Several listings were entered in SQUARE FEET while the site labels
--  areas m². But NOT all of them — the data is mixed, so this converts
--  listing-by-listing instead of blanket-dividing. Evidence used:
--    · Casa Hanna desc says 366 m²      → its 3,940 field is sq ft ✓
--    · Golondrinas desc says 4,833 sq ft → matches its field, sq ft ✓
--    · Casa Hijau desc says 300 m² + 689 m² → size AND lot are sq ft ✓
--    · Villa Las Brisas desc says 7,654 sq ft = its 711 m² field → ALREADY m², untouched
--    · Diria 512 desc says 1,249 sq ft = its 116 m² field → ALREADY m², untouched
--  After this, every size/lot is m²; the site displays m² + ft² together.
-- ═══════════════════════════════════════════════════════════════

UPDATE properties SET size = 273            WHERE id = 'e4f7876f-6226-4e3b-b576-3def68102ca4'; -- Casa Coyote        (2,939 sqft; lot 1,611 m² correct — house no longer "bigger than its lot")
UPDATE properties SET size = 391            WHERE id = '843a8b0b-910d-4bc7-91cb-e78fb71870a5'; -- Casa Flores del Mar (4,209 sqft)
UPDATE properties SET size = 325, lot = 325 WHERE id = 'f785fcd1-a6e9-4191-97b4-5be64cbb4c57'; -- Enclave C5         (3,496 in BOTH fields = same-unit duplicate entry)
UPDATE properties SET size = 300            WHERE id = '47978e51-8443-46c7-9ed9-9c647c9a63ae'; -- Villa Calypso      (3,229 sqft; lot 5,200 m² desc-confirmed, untouched)
UPDATE properties SET size = 366            WHERE id = '7239fe66-32d5-4b90-a21f-44f3c749d39f'; -- Casa Hanna         (3,940 sqft; desc: 366 m²)
UPDATE properties SET size = 263            WHERE id = '56bb618c-5571-4cce-ad83-04b82026e0f9'; -- Multi-Home Avellanas (2,831 sqft)
UPDATE properties SET size = 449            WHERE id = 'adef907b-5eff-4c56-814e-079adb714c36'; -- Casa Golondrinas   (desc: 4,833 sq ft)
UPDATE properties SET size = 300, lot = 689 WHERE id = 'e6552762-7495-459f-8bdb-7ccc0fbca9c0'; -- Casa Hijau         (desc: 300 m² house, 689 m² lot)

-- Untouched because they are already metric (verified against their own
-- descriptions or sanity): Villa Las Brisas 711, Mareas I 1,106,
-- Casa Nya 1,082, Casa Uchuva 333, Diria 512 116, Mareas III (no size).

-- "Fully Equiped Kitchen" → "Fully Equipped Kitchen" (Hanna, Multi-Home, Nya)
UPDATE properties
SET features = array_replace(features, 'Fully Equiped Kitchen', 'Fully Equipped Kitchen')
WHERE 'Fully Equiped Kitchen' = ANY(features);

-- Verify: sizes should now read like real houses (263–1,106 m²),
-- and no features row should contain "Equiped".
SELECT name, size AS m2_built, lot AS m2_lot
FROM properties WHERE status IN ('active','sold')
ORDER BY sort_order;
