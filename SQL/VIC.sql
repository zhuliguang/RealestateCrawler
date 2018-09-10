SELECT * FROM aus_sold_houses.victoria
ORDER BY id;

SELECT COUNT(*) FROM aus_sold_houses.victoria
WHERE land_size is not Null or floor_area is not Null or year_built is not Null
ORDER BY id DESC;

SELECT * FROM aus_sold_houses.victoria
WHERE land_size is Null AND floor_area is Null AND year_built is Null
ORDER BY postcode;


SELECT * FROM aus_sold_houses.victoria
WHERE land_size is not Null or floor_area is not Null or year_built is not Null
ORDER BY id DESC;

SELECT * FROM aus_sold_houses.victoria
WHERE time > '2018-08-28 00:00:00'
ORDER BY time DESC;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM aus_sold_houses.victoria
WHERE postcode >= 4000 OR postcode < 3000;
SET SQL_SAFE_UPDATES = 1;

SELECT suburb, COUNT(suburb) AS count FROM aus_sold_houses.victoria
GROUP BY suburb ORDER BY count DESC;


SELECT postcode, COUNT(postcode) AS count FROM aus_sold_houses.victoria
GROUP BY postcode ORDER BY count DESC;

UPDATE aus_sold_houses.victoria SET land_size = Null WHERE house_id = 127598510;


ALTER TABLE aus_sold_houses.victoria ADD COLUMN land_size INTEGER NULL DEFAULT NULL AFTER parking;
ALTER TABLE aus_sold_houses.victoria ADD COLUMN floor_area INTEGER NULL DEFAULT NULL AFTER land_size;
ALTER TABLE aus_sold_houses.victoria ADD COLUMN year_built INTEGER NULL DEFAULT NULL AFTER floor_area;

ALTER TABLE aus_sold_houses.victoria ADD COLUMN REA_id INTEGER NULL DEFAULT NULL AFTER house_id;
ALTER TABLE aus_sold_houses.victoria ADD UNIQUE (REA_id);