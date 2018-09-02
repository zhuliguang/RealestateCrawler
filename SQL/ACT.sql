SELECT * FROM aus_sold_houses.australian_capital_territory
ORDER BY id DESC;

SELECT COUNT(*) FROM aus_sold_houses.australian_capital_territory;

ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN land_size INTEGER NULL DEFAULT NULL AFTER parking;
ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN floor_area INTEGER NULL DEFAULT NULL AFTER land_size;
ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN year_built INTEGER NULL DEFAULT NULL AFTER floor_area;