SET search_path TO artistdb;

CREATE VIEW CA_album AS
SELECT album_id, year, Artist.artist_id, name
FROM Album, Artist
WHERE Album.artist_id = Artist.artist_id 
	AND Artist.nationality = 'Canada';

CREATE VIEW CA_first AS
SELECT ca.album_id, ca.artist_id, ca.name
FROM CA_album ca
WHERE year = (
	SELECT MIN(year)
	FROM CA_album
	WHERE CA_album.artist_id = ca.artist_id )
GROUP BY ca.artist_id, ca.album_id, ca.name;

CREATE VIEW CA_first_indie AS
SELECT *
FROM CA_first
WHERE album_id NOT IN (
	SELECT album_id
	FROM ProducedBy);

SELECT DISTINCT cfi.name AS artist_name
FROM CA_first_indie cfi, ProducedBy pb, 
	RecordLabel rl, Album al
WHERE al.artist_id = cfi.artist_id
	AND al.album_id = pb.album_id 
	AND pb.label_id = rl.label_id
	AND rl.country = 'America'
ORDER BY cfi.name ASC;

DROP VIEW CA_first_indie;
DROP VIEW CA_first;
DROP VIEW CA_album;

