<noplaylist>
{
let $userdoc := doc("users.xml")
let $musicdoc := doc("music.xml")
let $songsonplaylists := $musicdoc//playlist/track/@sid
for $song in $musicdoc//song
where not($song/@sid = $songsonplaylists)
return 
   <song> {$song/@sid} </song>
}
</noplaylist>
