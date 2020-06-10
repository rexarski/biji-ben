SET search_path TO artistdb;

CREATE VIEW ACDC AS
SELECT wib.artist_id, wib.band_id, wib.start_year, wib.end_year
FROM WasInBand wib, Artist
WHERE wib.band_id = Artist.artist_id AND Artist.name = 'AC/DC';

INSERT INTO WasInBand (artist_id, band_id, start_year, end_year)
VALUES ((SELECT artist_id FROM ACDC), (SELECT band_id FROM ACDC),
'2014', '2015');

SELECT * FROM WasInBand ORDER BY artist_id;

DROP VIEW ACDC;