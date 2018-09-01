SELECT * FROM aus_sold_houses.new_south_wales
ORDER BY id DESC;

SELECT COUNT(*) FROM aus_sold_houses.new_south_wales;

SELECT COUNT(*) FROM aus_sold_houses.new_south_wales
WHERE time > '2018-08-29 00:00:00'
ORDER BY time DESC;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM aus_sold_houses.new_south_wales
WHERE postcode >= 3000 OR postcode < 2000;
SET SQL_SAFE_UPDATES = 1;