<pairs>
{
let $userdoc := doc("users.xml")
for $u1 in $userdoc//user
for $u2 in $userdoc//user
where $u1 < $u2 and
   every $x in $u1//playlist/@pid satisfies $x = $u2//playlist/@pid and
   every $y in $u2//playlist/@pid satisfies $x = $u1//playlist/@pid and
   count($u1//playlist) >= 5
return 
   <pair uid1="{$u1/@uid}" uid2="{$u2/@uid}"/>
}
</pairs>
