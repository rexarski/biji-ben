<popularity>
{
let $userdoc := doc("users.xml")
let $musicdoc := doc("music.xml")
for $p in $musicdoc//playlist
let $lowcount := count($userdoc//playlist[@pid = $p/@pid][@playcount < 5])
let $medcount := count($userdoc//playlist[@pid = $p/@pid]
			[@playcount >= 5 and @playcount < 50])
let $highcount := count($userdoc//playlist[@pid = $p/@pid][@playcount >= 50])
return 
   <histogram>
      {$p/@pid}
      <low count="{$lowcount}"/>
      <medium count="{$medcount}"/>
      <high count="{$highcount}"/>
   </histogram>
}
</popularity>
