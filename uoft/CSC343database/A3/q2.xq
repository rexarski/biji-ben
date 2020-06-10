let $allmovies := fn:doc("movies.xml")
for $movie in $allmovies//Movie
let $numact := count($movie//Actor)
return ($movie/@MID, $numact)