(: Tricky to get the ties to all come out as individual xml elements :)

<favourites>
{
   let $userdoc := doc("users.xml")
   for $user in $userdoc//user
   (: The highest playcount for $user, or -1 if they have no playlists :)
   let $highestplaycount :=
      if ($user//playlists) then 
         max($user//playlist/@playcount)
      else 
         -1
   (: The playlists with the highest playcount for $user, 
      or the empty sequence if they have no playlists. :)
   let $mostplayed :=
      if ($highestplaycount = -1) then
         ()
      else
         for $item in $user//playlist
         where $item/@playcount = $highestplaycount
         return $item
   return
      if ($mostplayed) then
         (: $user has playlists, so return their most popular one(s). :)
         for $x in $mostplayed
         return
            <user>
               {$user/@uid}
               {$x/@pid}
               {$x/@playcount}
            </user>
      else
         (: $user has no playlists, so just return their uid. :)
         <user>
            {$user/@uid}
         </user>
}
</favourites>
