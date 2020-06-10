let $personpid := fn:doc("people.xml")//Person[.//First="James" and .//Last="Cameron"]/@PID
let $movieinfo := fn:doc("movies.xml")//Movie[@year > 2001]
for $movie in $movieinfo
where $movie/Director/@PID = $personpid
return  ($movie/Title, $movie/@year)