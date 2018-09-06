SELECT * FROM aus_sold_houses.australian_capital_territory
WHERE REA_id is not null
ORDER BY id DESC;

SELECT * FROM aus_sold_houses.australian_capital_territory
WHERE id = 93
ORDER BY id DESC;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM aus_sold_houses.australian_capital_territory
WHERE postcode >= 3000 OR postcode < 2600
OR (postcode >= 2700 AND postcode < 2900);
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN land_size INTEGER NULL DEFAULT NULL AFTER parking;
ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN floor_area INTEGER NULL DEFAULT NULL AFTER land_size;
ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN year_built INTEGER NULL DEFAULT NULL AFTER floor_area;

ALTER TABLE aus_sold_houses.australian_capital_territory ADD COLUMN REA_id INTEGER NULL DEFAULT NULL AFTER house_id;
ALTER TABLE aus_sold_houses.australian_capital_territory ADD UNIQUE (REA_id);