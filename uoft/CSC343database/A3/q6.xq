let $movies := fn:doc("movies.xml")//Movie
let $person := fn:doc("people.xml")//Person
for $movie in $movies
where ($movie/Director/@PID = $movie/Actor/@PID)
and ($movie/Director/@PID = $person/@PID)
return ($person/@PID, $person/Last)

