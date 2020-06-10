SET search_path TO artistdb;

SELECT DISTINCT ar.name AS artist_name, a.title AS album_name
FROM Artist ar, Album a
WHERE a.album_id NOT IN (SELECT DISTINCT Album.album_id
       FROM Album, Song, BelongsToAlbum bta
       WHERE Album.album_id = bta.album_id 
       	     AND bta.song_id = Song.song_id 
	     AND Song.songwriter_id <> Album.artist_id) 
       AND ar.artist_id = a.artist_id
ORDER BY ar.name ASC, a.title ASC;