<fewfollowers>
{
let $userdoc := doc("users.xml")
let $musicdoc := doc("music.xml")
(: Construct an XML structure to record the followers of each user.
   <f>
      <user uid="u20">
         <follower uid="u45"/>
         <follower uid="u9"/>
      </user>
   </f>
:)
let $followers :=
   <f> 
   {
      for $u1 in $userdoc//user
      let $u1followers :=
         (for $u2 in $userdoc//user
         where contains($u2//follows/@who, $u1/@uid)
         return <follower uid="{$u2/@uid}"/>)
      return <user uid="{$u1/@uid}">
               {$u1followers}
             </user>
   }
   </f>
for $userelement in $userdoc//user
where count($followers//user[@uid=$userelement/@uid]/follower) < 4
return
   <who>
      {$userelement/@uid}
      {$followers//user[@uid=$userelement/@uid]/follower}
   </who>
}
</fewfollowers>
