SELECT * FROM aus_sold_houses.south_australia
ORDER BY id DESC;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM aus_sold_houses.south_australia
WHERE postcode >= 6000 OR postcode < 5000;
SET SQL_SAFE_UPDATES = 1;
