<DEALS>
{
for $q in fn:doc('property.xml')//RENT_AMOUNT[.<=800]
return
<DEAL>
{
$q
}
</DEAL>
}
</DEALS>
