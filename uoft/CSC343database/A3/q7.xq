<Stats>
{
let $movies := fn:doc("movies.xml")//Movie
let $types := distinct-values($movies//Category/text())
for $m in $types
return 
<Bar category = "{$m}" count = "{count($movies[.//Category=$m])}" />
}
</Stats>
