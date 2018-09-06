SELECT * FROM aus_sold_houses.western_australia
ORDER BY id DESC;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM aus_sold_houses.western_australia
WHERE postcode >= 7000 OR postcode < 6000;
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE aus_sold_houses.western_australia ADD COLUMN REA_id INTEGER NULL DEFAULT NULL AFTER house_id;
ALTER TABLE aus_sold_houses.western_australia ADD UNIQUE (REA_id);