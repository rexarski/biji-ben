<songcounts>
{
let $userdoc := doc("users.xml")
let $musicdoc := doc("music.xml")
for $song in $musicdoc//song
(: Make a sequence of elements like this: <count n="71">
   Each one is a playcount for some user of some playlist that
   includes this song. :)
let $counts :=
      (: The playlists that this song is on. :)
      let $playlistsOn := 
	      for $p in $musicdoc//playlist
	      where $p/track/@sid = $song/@sid
	      return $p
      for $p in $playlistsOn 
      (: The user playlists with that pid. :)
      let $userplaylists :=
	      for $up in $userdoc//playlist
	      where $up/@pid = $p/@pid
	      return $up
      for $userplaylist in $userplaylists
      return
	      <count n="{$userplaylist/@playcount}"/>
(: Total playcount for that song. :)
let $total := sum($counts/@n)
let $title := normalize-space($song/title)
return 	
	<song sid="{$song/@sid}" title="{$title}" playcount="{$total}">
	</song>
}
</songcounts>
