let $allpeople := fn:doc("people.xml")
let $numpeople := count($allpeople//Person)
let $numoscars := count($allpeople//Oscar)
return $numoscars div $numpeople