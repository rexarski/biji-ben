# schema:

- Artist(**artist\_id**, name, birthdate, nationality)
	- when formed, where formed
	- 'Guns "n Roses'
- Role(**artist\_id, role**)
	- role is a tuple: musician, band, songwriter or multiple of those
- WasInBand(**artist\_id, band\_id, start\_year, end\_year**)
- Album(**album\_id**, title, artist\_id, genre\_id, year, sales)
	- one genre at a time
- Genre(**genre\_id**, genre)
- Song(**song\_id**, title, songwriter\_id)
	- songwritier\_id is artist\_id of the band
- BelongsToAlbum(**song\_id, album\_id**, track\_no)
- RecordLabel(**label\_id**, label\_name, country)
- ProducedBy(**album\_id, label\_id**)
- Collaboration(**song\_id, artist1, artist2**)
	- artist1 is the main
