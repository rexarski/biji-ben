let $allpeople := fn:doc("people.xml")
let $alldirectors := fn:doc("movies.xml")//Director/@PID
for $person in $allpeople//Person
where $person/@PID = $alldirectors and empty($person/@pob) 
return ($person/@PID, $person//Last)