SELECT * FROM aus_sold_houses.northern_territory
ORDER BY id DESC;

ALTER TABLE aus_sold_houses.northern_territory ADD COLUMN land_size INTEGER NULL DEFAULT NULL AFTER parking;
ALTER TABLE aus_sold_houses.northern_territory ADD COLUMN floor_area INTEGER NULL DEFAULT NULL AFTER land_size;
ALTER TABLE aus_sold_houses.northern_territory ADD COLUMN year_built INTEGER NULL DEFAULT NULL AFTER floor_area;