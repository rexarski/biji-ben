SET search_path TO artistdb;

CREATE VIEW FirstAlbumYear(fyear) AS
       SELECT min(al.year)
       FROM  Album al, Artist ar
       WHERE  al.artist_id = ar.artist_id  
       	      AND ar.name = 'Steppenwolf';


SELECT DISTINCT art.name, art.nationality
FROM Artist art, Role,  FirstAlbumYear fay
WHERE fay.fyear =  EXTRACT(year FROM art.birthdate)
      AND art.artist_id = Role.artist_id
      AND Role.role = 'Musician'
ORDER BY art.name ASC;

DROP VIEW FirstAlbumYear;

