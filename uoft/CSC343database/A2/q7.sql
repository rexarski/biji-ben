SET search_path TO artistdb;

SELECT DISTINCT Song.title AS song_name, Album.year, Artist.name AS artist_name
FROM Artist, Album, Song, BelongsToAlbum bta
WHERE 
	Song.song_id = bta.song_id 
	AND Album.album_id = bta.album_id
	AND Artist.artist_id = Album.artist_id
	AND Song.song_id IN (
		SELECT song_id
		FROM BelongsToAlbum
		GROUP BY song_id
		HAVING COUNT(song_id) > 1)
ORDER BY Song.title ASC, Album.year ASC, Artist.name ASC;