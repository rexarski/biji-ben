SET search_path TO artistdb;

UPDATE WasInBand wib
SET end_year = 2014
WHERE wib.artist_id = (
	SELECT artist_id
	FROM Artist
	WHERE name = 'Adam Levine');

UPDATE WasInband wib
SET end_year = 2014
WHERE wib.artist_id = (
	SELECT artist_id
	FROM Artist
	WHERE name = 'Mick Jagger');
	
INSERT INTO WasInBand(artist_id, band_id, start_year, end_year)
VALUES((SELECT artist_id FROM Artist WHERE name = 'Mick Jagger'),
		(SELECT artist_id FROM Artist WHERE name = 'Maroon 5'),
		2014, 2015);
		
SELECT * FROM WasInBand ORDER BY artist_id;
