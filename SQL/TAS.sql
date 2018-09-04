SELECT * FROM aus_sold_houses.tasmania
ORDER BY id DESC;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM aus_sold_houses.tasmania
WHERE postcode >= 8000 OR postcode < 7000;
SET SQL_SAFE_UPDATES = 1;