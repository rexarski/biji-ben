SELECT DISTINCT name as country
FROM country CROSS JOIN countrylanguage
WHERE code = countrycode AND countrylanguage.countrylanguage = 'English' AND percentage >= ALL (
    SELECT percentage
    FROM countrylanguage
    WHERE code = countrycode AND countrylanguage <> 'English');