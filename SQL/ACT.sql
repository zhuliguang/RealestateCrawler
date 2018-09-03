SELECT * FROM aus_sold_houses.australian_capital_territory
#WHERE postcode > 2700
ORDER BY id DESC;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM aus_sold_houses.australian_capital_territory
WHERE postcode >= 3000 OR postcode < 2600
OR (postcode >= 2700 AND postcode < 2900);
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN land_size INTEGER NULL DEFAULT NULL AFTER parking;
ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN floor_area INTEGER NULL DEFAULT NULL AFTER land_size;
ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN year_built INTEGER NULL DEFAULT NULL AFTER floor_area;