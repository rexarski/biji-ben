let $oscars := fn:doc("oscars.xml")
let $movies := fn:doc("movies.xml")//Movie
let $later := 
	for $o1 in $oscars//Oscar
	for $o2 in $oscars//Oscar
	where ($o1/@year > $o2/@year) and ($o1/Type = $o2/Type)
	return $o1
let $first := $oscars//Oscar except $later
let $moid := $movies//@OID
for $award in $first[./@OID = $moid]
return ($award/Type, $award/@year, $movies[./Oscar[@OID = $award/@OID]]/Title)

