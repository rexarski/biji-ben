SET search_path To artistdb;

CREATE VIEW Change_artist AS
SELECT DISTINCT Artist.name AS artist, Role.role AS capacity, COUNT(Album.genre_id) AS genres
FROM Artist, Album, Role
WHERE Role.artist_id = Artist.artist_id
      AND Artist.artist_id = Album.artist_id
      AND (Role.role = 'Musician' OR Role.role = 'Band')
GROUP BY Artist.artist_id, Role.role
HAVING COUNT(DISTINCT Album.genre_id) >= 3;

CREATE VIEW Change_songwriter AS
SELECT DISTINCT Artist.name AS artist, Role.role AS capacity, COUNT(Album.genre_id) AS genres
FROM Artist, Album, Role, Song, BelongsToAlbum bta
WHERE Role.artist_id = Artist.artist_id
      AND Role.role = 'Songwriter'
      ANd Song.songwriter_id = Artist.artist_id
      AND Song.song_id = bta.song_id
      AND Album.album_id = bta.album_id
GROUP BY Artist.artist_id, Role.role
HAVING COUNT(DISTINCT Album.genre_id) >= 3;

CREATE VIEW Comb AS
(SELECT * FROM Change_artist) UNION (SELECT * FROM Change_songwriter);


SELECT *
FROM Comb
ORDER BY
      CASE  capacity
      WHEN  'Musician' THEN 1
      WHEN  'Band' THEN 2
      WHEN  'Songwriter' THEN 3
      ELSE 4
      END,  genres DESC, artist ASC;

DROP VIEW Comb;
DROP VIEW Change_artist;
DROP VIEW Change_songwriter;
