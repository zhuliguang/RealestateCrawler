SELECT * FROM aus_sold_houses.victoria
WHERE postcode = 3149
ORDER BY time DESC;

SELECT * FROM aus_sold_houses.victoria
WHERE time > '2018-08-28 00:00:00'
ORDER BY time DESC;

SET SQL_SAFE_UPDATES = 0;
SELECT * FROM aus_sold_houses.victoria
WHERE postcode >= 4000 OR postcode <= 2000;
SET SQL_SAFE_UPDATES = 1;

SELECT suburb, COUNT(suburb) AS count FROM aus_sold_houses.victoria
GROUP BY suburb ORDER BY count DESC;

SELECT COUNT(*) FROM aus_sold_houses.victoria;

SELECT postcode, COUNT(postcode) AS count FROM aus_sold_houses.victoria
GROUP BY postcode ORDER BY count DESC;

ALTER TABLE aus_sold_houses.victoria ADD COLUMN land_size INTEGER NULL DEFAULT NULL AFTER parking;
ALTER TABLE aus_sold_houses.victoria ADD COLUMN floor_area INTEGER NULL DEFAULT NULL AFTER land_size;
ALTER TABLE aus_sold_houses.victoria ADD COLUMN year_built INTEGER NULL DEFAULT NULL AFTER floor_area;