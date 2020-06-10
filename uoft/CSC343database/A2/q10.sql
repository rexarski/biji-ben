SET search_path TO artistdb;

CREATE VIEW T AS
SELECT Song.song_id, Album.album_id
FROM Song, Album, BelongsToAlbum bta
WHERE
	Song.song_id = bta.song_id
	AND Album.album_id = bta.album_id
	AND Album.title = 'Thriller';
	
SELECT * INTO Temp From T;

DROP VIEW T;

DELETE FROM ProducedBy
WHERE ProducedBy.album_id IN (select album_id FROM Temp);

DELETE FROM Collaboration
WHERE song_id IN (select song_id FROM Temp);

DELETE FROM BelongsToAlbum bta
WHERE 
	bta.song_id IN (select song_id FROM Temp)
	OR bta.album_id IN (select album_id FROM Temp);

DELETE FROM Song
WHERE song_id IN (select song_id FROM Temp);

DELETE FROM Album
WHERE Album.title = 'Thriller';

DROP TABLE Temp;



