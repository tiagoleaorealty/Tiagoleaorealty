-- Descriptive property URLs. Run once. Adds a permanent slug per listing —
-- generated from name + community, then STABLE forever (renames never change it).
ALTER TABLE properties ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

UPDATE properties SET slug = 'casa-coyote-playas-del-coco'          WHERE id = 'e4f7876f-6226-4e3b-b576-3def68102ca4';
UPDATE properties SET slug = 'casa-flores-del-mar-playa-grande'     WHERE id = '843a8b0b-910d-4bc7-91cb-e78fb71870a5';
UPDATE properties SET slug = 'enclave-c5-playa-avellanas'           WHERE id = 'f785fcd1-a6e9-4191-97b4-5be64cbb4c57';
UPDATE properties SET slug = 'villa-calypso-tamarindo'              WHERE id = '47978e51-8443-46c7-9ed9-9c647c9a63ae';
UPDATE properties SET slug = 'casa-uchuva-playa-grande'             WHERE id = '29562190-c1b0-483c-974b-3014656d3df5';
UPDATE properties SET slug = 'casa-hanna-tamarindo'                 WHERE id = '7239fe66-32d5-4b90-a21f-44f3c749d39f';
UPDATE properties SET slug = 'multi-home-property-playa-avellanas'  WHERE id = '56bb618c-5571-4cce-ad83-04b82026e0f9';
UPDATE properties SET slug = 'diria-512-tamarindo'                  WHERE id = 'f46ee5c9-f438-44d6-a22b-c852eea40500';
UPDATE properties SET slug = 'mareas-iii-hacienda-pinilla'          WHERE id = '00ad65c3-5ec2-44a7-ac76-ee933af9b3ee';
UPDATE properties SET slug = 'villa-las-brisas-29-hacienda-pinilla' WHERE id = '12fcb6c9-4088-404b-9092-a061cf067e16';
UPDATE properties SET slug = 'mareas-i-hacienda-pinilla'            WHERE id = '37bf40df-3bbf-4aff-8566-76fbcbcf9303';
UPDATE properties SET slug = 'casa-golondrinas-hacienda-pinilla'    WHERE id = 'adef907b-5eff-4c56-814e-079adb714c36';
UPDATE properties SET slug = 'casa-hijau-marbella'                  WHERE id = 'e6552762-7495-459f-8bdb-7ccc0fbca9c0';
UPDATE properties SET slug = 'casa-nya-hacienda-pinilla'            WHERE id = '262abf92-5ce0-4514-89e1-1d49996c2288';

-- Verify: every row should show a slug.
SELECT name, slug FROM properties WHERE status IN ('active','sold') ORDER BY sort_order;
