SELECT * FROM aus_sold_houses.queensland
ORDER BY id DESC;

SELECT * FROM aus_sold_houses.queensland
WHERE house_id = 127017118;

SELECT COUNT(*) FROM aus_sold_houses.queensland;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM aus_sold_houses.queensland
WHERE postcode >= 5000 OR postcode < 4000;
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE aus_sold_houses.queensland ADD COLUMN land_size INTEGER NULL DEFAULT NULL AFTER parking;
ALTER TABLE aus_sold_houses.queensland ADD COLUMN floor_area INTEGER NULL DEFAULT NULL AFTER land_size;
ALTER TABLE aus_sold_houses.queensland ADD COLUMN year_built INTEGER NULL DEFAULT NULL AFTER floor_area;