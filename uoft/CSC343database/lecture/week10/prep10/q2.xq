<COMMERCIAL_UNITS>
{
let $pdoc := fn:doc("property.xml")//PROPERTY
for $p in $pdoc//COMMERCIAL/..
return if ($p//MULTI_UNIT) 
then <UNIT>{$p//UNIT, $p/ADDRESS}</UNIT>
else <UNIT>{($p//SINGLE_UNIT/INFO, $p/ADDRESS)}</UNIT>
}
</COMMERCIAL_UNITS>