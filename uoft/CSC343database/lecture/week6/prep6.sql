INSERT INTO country(code, name, continent, population)
VALUES ('BOR','Borduria','Pangaea','1000'),
('CAG','Cagliostro','Pangaea','250'),
('MAR','Qumar','Pangaea','3380');

INSERT INTO countrylanguage(countrycode, countrylanguage)
VALUES ('BOR','English'), ('BOR','Italian'), ('BOR','Klingon');

DELETE FROM country
WHERE population < 300;
 
UPDATE country
SET continent = 'Luna'
WHERE code = 'BOR';
 

Result:

 select * from country;
 code |   name   | continent | population 
------+----------+-----------+------------
 MAR  | Qumar    | Pangaea   |       3380
 BOR  | Borduria | Luna      |       1000
(2 rows)

select * from countrylanguage;
 countrycode | countrylanguage | isofficial | percentage 
-------------+-----------------+------------+------------
 BOR         | English         |            |           
 BOR         | Italian         |            |           
 BOR         | Klingon         |            |           
(3 rows)