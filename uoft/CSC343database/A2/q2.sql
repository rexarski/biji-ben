SET search_path TO artistdb;


CREATE VIEW Solo AS
SELECT Album.artist_id, Artist.name, album_id, sales
FROM Album, Artist
WHERE Album.artist_id = Artist.artist_id AND 
      album_id NOT IN (
		SELECT DISTINCT album_id
		FROM BelongsToAlbum bta, Collaboration c
		WHERE bta.song_id = c.song_id);

CREATE VIEW Co AS
(SELECT Album.artist_id, Artist.name, album_id, sales
	FROM Album, Artist
	WHERE Album.artist_id = Artist.artist_id)
EXCEPT
(SELECT *
	FROM Solo);

SELECT Co.name AS artists, AVG(Co.sales) AS avg_collab_sales
FROM Co, Solo 
WHERE Solo.artist_id = Co.artist_id 
GROUP BY Co.name, Solo.sales
HAVING AVG(Co.sales) > Solo.sales
ORDER BY Co.name ASC;


DROP VIEW Co;
DROP VIEW Solo;