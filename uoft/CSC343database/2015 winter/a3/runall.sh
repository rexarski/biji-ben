#! /bin/sh

echo "Checking Assignment 3 (Part 1) Solutions" > results.txt
echo "" >> results.txt

for query in q1 q2 q3 q4 q5 q6
do
   echo "============================== Query" $query " ==============================" >> results.txt
   echo "" >> results.txt
   # First run the query without any xmllinting.  
   # Even ill-formed xml work work here.
   echo "------ raw output ------" >> results.txt
   echo "" >> results.txt
   galax-run $query.xq >> results.txt 2>&1
   echo "" >> results.txt

   # Now run the queries and produce formatted output using xmllint.  
   # Only well-formed xml will work here.
   echo "------ formatted output (therefore well-formed) ------" >> results.txt
   echo "" >> results.txt
   echo "<?xml version='1.0' standalone='no' ?>" > TEMP.xml
   galax-run $query.xq >> TEMP.xml  2>&1
   xmllint --format TEMP.xml >> results.txt  2>&1
   echo "" >> results.txt

   # Now validate the output of the queries.
   echo "------ checking validity of output ------" >> results.txt
   echo "" >> results.txt
   echo "<?xml version='1.0' standalone='no' ?>" > TEMP.xml
   echo -n "<!DOCTYPE " >> TEMP.xml
   # Put the right doctype in, which depends on the query.
   if [ "$query" = "q1" ]; then
      echo -n "noplaylist" >> TEMP.xml
   fi
   if [ "$query" = "q2" ]; then
      echo -n "fewfollowers" >> TEMP.xml
   fi
   if [ "$query" = "q3" ]; then
      echo -n "favourites" >> TEMP.xml
   fi
   if [ "$query" = "q4" ]; then
      echo -n "pairs" >> TEMP.xml
   fi
   if [ "$query" = "q5" ]; then
      echo -n "popularity" >> TEMP.xml
   fi
   if [ "$query" = "q6" ]; then
      echo -n "songcounts" >> TEMP.xml
   fi
   echo " SYSTEM '"$query".dtd'>" >> TEMP.xml
   galax-run $query.xq >> TEMP.xml  2>&1
   echo "Results valid? (no news is good news)" >> results.txt
   xmllint --noout --valid TEMP.xml >> results.txt  2>&1
   echo "" >> results.txt
done
