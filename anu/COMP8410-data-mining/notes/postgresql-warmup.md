# [PostgreSQL warmup](https://www.pgexercises.com/)

2018-02-12

## Simple SQL Queries

### Retrieve everything from a table

```sql
select * from cd.facilities;
```

- The formula is `select [some set of columns] from [some table or group of tables]`. 
- `*` represents all columns.

### Retrieve specific columns from a table

```sql
select name, membercost from cd.facilities;
```

- Use comma to separate specified columns to select.
- Generally speaking, for non-throwaway queries it's considered desirable to specify the names of the columns you want in your queries rather than using `*`. This is because your application might not be able to cope if more columns get added into the table.

### Control which rows are retrieved

```sql
select * from cd.facilities where membercost > 0;
```

- The `FROM` clause is used to build up a set of candidate rows to read results from. In our examples so far, this set of rows has simply been the contents of a table. 

### Control which rows are retrieved - part 2

```sql
select facid, name, membercost, monthlymaintenance
		from cd.facilities
		where
				membercost > 0 and
				(membercost < monthlymaintenance/50.0);
```

- Two or more conditions, use `AND`/`OR` to combine them.

### Basic string searches

```sql
select *
		from cd.facilities
		where
				name like '%Tennis%';
```

- `LIKE` operators provides simple pattern matching on strings, with `%` character matching any string, `_` matching any single character.

### Matching against multiple possible values

```sql
select *
		from cd.facilities
		where facid in (1,5);
```

- Equivalently, use `where facid = 1 or facid = 5`. Alternatively, with large numbers of possible matches is the `IN` operator which takes a list of possible values and matches them against the `facid` in this case.
- `IN` in fact takes a table with a single column, for example

```sql
select * from cd.facilities where facid in (select facid from cd.facilities);
```

- The inner query is called *subquery*.

### Classify results into buckets

```sql
select name,
		case when (monthlymaintenance > 100) then
				'expensive'
		else
				'cheap'
		end as cost
		from cd.facilities;
```

- We do computation in the area of the query between `SELECT` and `FROM` (as a subquery).
- `CASE` statement is effectively like if/swithc statements.
- `AS` operator, is used to label columns or expressions and display them more nicely or easier referenced.

### Working with dates

```sql
select memid, surname, firstname, joindate
		from cd.members
		where joindate >= '2012-09-01';
```

- For SQL timestamps, they are formatted in descending order of magnitude: `YYYY-MM-DD HH:MM:SS.nnnnn`. If not specified, `YYYY-MM-DD` get automatically cast by postgres into the full timestamp `YYYY-MM-DD 00:00:00`.

### Removing duplicates, and ordering results

```sql
select distinct surname
		from cd.members
order by surname
limit 10;
```

- Specify `DISTINCT` after `SELECT`removes uplicate rows from the result set. This applies to _rows_: so if multiple columns, row B is only equalto row A if the values in all columns are the same (then we call it is distinct).
- Removing duplicates requires large cost, do it as needed only.
- Specify `ORDER BY` (after the `FROM` and `WHERE`), allow results to be ordered by a column or set of columns (comma separated).
- `LIMIT` keywords allows you to limit the number of results retrieved.

### Combining results from multiple queries

```sql
select surname
		from cd.members
union
select name
		from cd.facilities;
```

- `UNION` operator combines the results of two SQL queries into a single table.
- The caveat is that both results from the two queries must have the same number of columns and compatible data types.
- `UNION` removes duplicate rows, while `UNION ALL` does not.

### Simple aggregation

```sql
select max(joindate) as latest
		from cd.members;
```

- SQL's aggregate function, to extract information about whole groups of rows.
- `MAX` aggregate function...

### More aggregation

```sql
select firstname, surname, joindate
		from cd.members
		where joindate =
				(select max(joindate)
                		from cd.members)
```

- A subquery to find out what the most recent joindate is. This subquery returns a _scalar_ table - that is, a table with a single column and a single row.

```sql
select firstname, surname, joindate
		from cd.members
order by joindate desc
limit 1;
```

- This also could work!

## Joins and Subqueries

### Retrieve the start times of members' bookings

```sql
select bks.starttime
		from
				cd.bookings bks
				inner join cd.members mems
						on mem.memid = bks.memid
		where
				mems.firstname='David'
				and mems.surname='Farrell';
```

- `INNER JOIN` combines two tables based on a join expression - in this case, for each member id in the members table, we're looking for matching values in the bookings table.

- _Alias_!

- For each matching, it's then produced a row combining the row from the members table, and the row from the bookings table.

- Another syntax of inner joins:

  ```sql
  select bks.starttime
  		from
  				cd.bookings bks,
  				cd.members mems
  		where
  				mems.firstname='David'
  				and mems.surname='Farrell'
  				and mems.memid=bks.memid;
  ```

### Work out the start times of bookings for tennis courts

```sql
select bks.starttime as start, facs.name as name
		from
				cd.facilities facs
				inner join cd.bookings bks
						on facs.facid = bks.facid
		where
				facs.facid in (0,1) and
				bks.starttime >= '2012-09-21' and
				bks.starttime < '2012-09-22'
order by bks.starttime
```

- Another `INNER JOIN` query.

### Produce a list of all members who have recommended another member

```sql
select distinct recs.firstname as firstname, recs.surname as surname
		from
				cd.members mems
				inner join cd.members recs
						on recs.memid = mems.recommendedby
order by surname, firstname
```

- Can join a table to itself. Our join takes each row in members that has a recommendedby value and looks in members again for the row which has a matching member id. Then generate an output row combining the two members entires.

### Produce a list of all members, along with their recommender

```sql
select mems.firstname as memfname, mems.surname as memsname, recs.firstname as recfname, recs.surname as recsname
		from
				cd.members mems
				left outer join cd.members recs
						on recs.memid = mems.recommendedby
orderby memsname, memfname;
```

- `LEFT OUTER JOIN`. As `INNER JOINT` takes a left and a right tables, and look for matching rows based on a join condition (`ON`). A `LEFT OUTER JOIN` operates similarly, except that if a given row on the left hand table doesn't match anything, it still produces an output row but consists of the left hand table row and a bunch of `NULLS` in place of the right hand table row.
- Useful in situations where we want to produce output with optional data.
- Also has `RIGHT OUTER JOIN` and `FULL OUTER JOIN` (rarely used)

### Produce a list of all members who have used a tennis court

```sql
select distinct mems.firstname || ' ' || mems.surname as member, facs.name as facility
		from
				cd.members mems
				inner join cd.bookings bks
						on mems.memid = bks.memid
				inner join cd.facilities facs
						on bks.facid = facs.facid
		where
				bks.facid in (0,1)
order by member
```

- Multiple joins! The relational model is all about tables, the output of any join is another table. The output of a query is a table. Sinlge columned lists are tables.
- `||` operator is used to concatenate strings.

### Produce a list of costly bookings

```sql
select mems.firstname || ' ' || mems.surname as member,
		facs.name as facility,
		case
				when mems.memid = 0 then
						bks.slots*facs.guestcost
				else
						bks.slots*facs.membercost
		end as cost
		from
				cd.members mems
				inner join cd.bookings bks
						on mems.memid = bks.memid
				inner join cd.facilities facs
						on bks.facid = facs.facid
		where
				bks.starttime >= '2012-09-14' and
				bks.starttime < '2012-09-15' and (
						(mems.memid = 0 and bks.slots*facs.guestcost > 30) or
						(mems.memid = !=0 and bks.slots*facs.membercost > 30)
				)
order by cost desc;
```

### Produce a list of all members, along with their recommender, using no joins

```sql
select distinct mems.firstname || ' ' || mems.surname as member,
		(select recs.firstname || ' ' || recs.surname as recommender
        		from cd.members recs
        		where recs.memid = mems.recommendedby
        )
        from
        		cd.members mems
order by member;
```

- Using the subquery to emulate an outer join. For each value of member, the subquery is run once to find the name of the individual who recommended them (if any).
- A subquery that uses information from the outer query in this way (and thus has to be run for each row in the result query) is known as a _correlated subquery_.

### Produce a list of costly bookings, using a subquery

```sql
select member, facility, cost from (
	select 
		mems.firstname || ' ' || mems.surname as member,
		facs.name as facility,
		case
			when mems.memid = 0 then
				bks.slots*facs.guestcost
			else
				bks.slots*facs.membercost
		end as cost
		from
			cd.members mems
			inner join cd.bookings bks
				on mems.memid = bks.memid
			inner join cd.facilities facs
				on bks.facid = facs.facid
		where
			bks.starttime >= '2012-09-14' and
			bks.starttime < '2012-09-15'
	) as bookings
	where cost > 30
order by cost desc;          
```

- This answer provides a mild simplification to the previous iteration: in the no-subquery version, we had to calculate the member or guest's cost in both the WHERE clause and the CASE statement. In our new version, we produce an inline query that calculates the total booking cost for us, allowing the outer query to simply select the bookings it's looking for. For reference, you may also see subqueries in the FROM clause referred to as *inline views*.

## Modifying data

### Insert some data into a table

```sql
insert into cd.facilities
    (facid, name, membercost, guestcost, initialoutlay, monthlymaintenance)
    values (9, 'Spa', 20, 30, 100000, 800);
```

- `INSERT INTO ... VALUES` to insert data into a table.

- `VALUES` here construct a row of data, which the `INSERT` statement inserts into the table.

- The first section in parentheses specifies the columns that we're providing data for. The second is part of `VALUES` specifies the actual data we want to insert into each column.

- If we insert data into every column of the table, explicitly specifying the column names is optional.

  ```sql
  insert into cd.facilities values (9, 'Spa', 20, 30, 100000, 800);
  ```

  - better to be specific though.

### Insert multiple rows of data into a table

```sql
insert into cd.facilities
		(facid, name, membercost, guestcost, initialoutlay, monthlymaintenance)
		values
				(9, 'Spa', 20, 30, 100000, 800),
				(10, 'Squash Court 2', 3.5, 17.5, 5000, 80);
```

- `VALUES` can generate more than one row to insert into a table.
- Postgres allows you to use `VALUES` wherever you might use a `SELECT`:

```sql
insert into cd.facilities
		(facid, name, membercost, guestcost, initialoutlay, monthlymaintenance)
		SELECT 9, 'Spa', 20, 30, 100000, 800
		UNION ALL
			SELECT 10, 'Squash Court 2', 3.5, 17.5, 5000, 80;
```

### Insert calculated data into a table

```sql
insert into cd.facilities
    (facid, name, membercost, guestcost, initialoutlay, monthlymaintenance)
    select (select max(facid) from cd.facilities)+1, 'Spa', 20, 30, 100000, 800; 
```

- a dynamically generated ID, current ID unknown. `VALUES` only supplies constant data.

### Update some existing data

```sql
update cd.facilities
    set initialoutlay = 10000
    where facid = 1;       
```

- `UPDATE` alters existing data, the `WHERE` is in exactly the same fashion. `SET` modifies data. `WHERE` is important, if ignored, the whole table will be updated.

### Update multiple rows and columns at the same time

```sql
update cd.facilities
	set
		membercost = 6,
		guestcost = 30
	where facid in (0,1);
```

- The `SET` clause accepts a comma separated list of values that you want to update.

### Update a row based on the contents of another row

```sql
update cd.facilities facs
    set
        membercost = (select membercost * 1.1 from cd.facilities where facid = 0),
        guestcost = (select guestcost * 1.1 from cd.facilities where facid = 0)
    where facs.facid = 1;   
```

- Postgres provides a nonstandard extension to SQL called `UPDATE…FROM` that addresses this: it allows you to supply a `FROM` clause to generate values for use in the `SET` clause. Example below:

```sql
update cd.facilities facs
    set
        membercost = facs2.membercost * 1.1,
        guestcost = facs2.guestcost * 1.1
    from (select * from cd.facilities where facid = 0) facs2
    where facs.facid = 1;
```

### Delete all bookings

```sql
delete from cd.bookings;
```

- delete rows from the table, with no qualifiers, deletes everything from the table.

```sql
truncate cd.bookings;
```

- TRUNCATE also deletes everything in the table, but does so using a quicker underlying mechanism. It's not [perfectly safe in all circumstances](https://www.postgresql.org/docs/9.6/static/mvcc-caveats.html), though, so use judiciously. When in doubt, use DELETE.

### Delete a member from the cd.members table

```sql
delete from cd.members where memid = 37;          
```

- parallel with `SELECT` and `UPDATE`.

### Delete based on a subquery

```sql
delete from cd.members where memid not in (select from cd.bookings);
```

- Use subqueries to determine whether a row should be deleted or not.
- Alternativley, use a _correlated subquerry_, instead it specifies a smaller subquery to run against every row.

```sql
delete from cd.members mems where not exists (select 1 from cd.bookings where memid = mems.memid);
```

## Aggregates

### Count the number of facilities

```sql
select count(*) from cd.facilities;
```

- `COUNT(*)` returns the number of rows
- `COUNT(address)` counts the number of non-null addresses in the result set.
- `COUNT(DISTINCT address)`...
- basic idea: takes a column of data, performs some function upon it, and outputs a _scalar_ (single) value.
- other aggregation functions like `MAX, MIN, SUM, AVG`.

```sql
select facid,
		(select count(*) from cd.facilities)
		from cd.facilities;
```

- `select facid, count(*) from cd.facilities` would not work because `count(*)` wants to collapse the facilities table into a single value, but it does not know which acid to pair the count with.

### Count the number of expensive facilities

```sql
select count(*) from cd.facilities where guestcost >= 10;          
```

### Count the number of recommendataions each member makes 

```sql
select recommendedby, count(*) 
	from cd.members
	where recommendedby is not null
	group by recommendedby
order by recommendedby;          
```

- `GROUP BY` batches the data together into groups and run the aggregation function separately for each group. In this case, we're saying 'for each distinct value of recommendedby, get me the number of times that value appears'.

### List the total slots booked per facility

```sql
select facid, sum(slots) as "Total Slots"
		from cd.bookings
		group by facid
order by facid;
```

### List the total slots booked per facility in a given month

```sql
select facid, sum(slots) as "Total Slots"
		from cd.bookings
		where
				startime >= '2012-09-01'
				and starttime < '2012-10-01'
		group by facid
order by sum(slots);
```

- Note: aggregation happens after the `WHERE` clause is evaluated, use `WHERE` to restrict the data we aggregate over.

### List the total slots booked per facility per month

```sql
select facid, extract(month from starttime) as month, sum(slots) as "Total Slots"
	from cd.bookings
	where
		starttime >= '2012-01-01'
		and starttime < '2013-01-01'
	group by facid, month
order by facid, month;
```

- `EXTRACT` allows you to get individual components of a timestamp, like day, month, year, etc.

### Find the count of members who have made at least one booking

```sql
select count(distinct memid) from cd.bookings
```

- equivalently, use subquery like

```sql
select count(*) from
		(select distinct memid from cd.bookings) as mems
```

- `COUNT DISTINCT`...

### List facilities with more than 1000 slots booked

```sql
select facid, sum(slots) as "Total Slots"
        from cd.bookings
        group by facid
        having sum(slots) > 1000
        order by facid  
```

- `HAVING` is used to filter the output from aggregate functions.
- The behaviour of `HAVING` is easily confused with that of `WHERE`. The best way to think about this is that **in the context of a query with an aggregate function, `WHERE` is used to filter what data gets input into the aggregate function, while `HAVING` is used to filter the data once it is output from the function.**

### Find the total revenue of each facility

```sql
select facs.name, sum(slots * case
			when memid = 0 then facs.guestcost
			else facs.membercost
		end) as revenue
	from cd.bookings bks
	inner join cd.facilities facs
		on bks.facid = facs.facid
	group by facs.name
order by revenue;          
```

### Find facilities with a total revenue less than 1000

```sql
select facs.name, sum(case 
		when memid = 0 then slots * facs.guestcost
		else slots * membercost
	end) as revenue
	from cd.bookings bks
	inner join cd.facilities facs
		on bks.facid = facs.facid
	group by facs.name
	having sum(case 
		when memid = 0 then slots * facs.guestcost
		else slots * membercost
	end) < 1000
order by revenue;
```

- Note: Postgres, unlike some other RDBMSs like SQL Server and MySQL, doesn't support putting column names in the `HAVING` clause. 

### Output the facility id that has the highest number of slots booked

```sql
select facid, sum(slots) as "Total Slots"
	from cd.bookings
	group by facid
order by sum(slots) desc
LIMIT 1;          
```

- this method has a significant weakness. In the event of a tie, we will still only get one result! To get all the relevant results, we might try using the `MAX` aggregate function

```sql
select facid, max(totalslots) from (
	select facid, sum(slots) as totalslots    
		from cd.bookings    
		group by facid
	) as sub group by facid
```

- Common Table Expressions (CTEs), allowing you to define a database view inline in your query. `WITH CTEName as (SQL-Expression)`.

```sql
with sum as (select facid, sum(slots) as totalslots
	from cd.bookings
	group by facid
)
select facid, totalslots 
	from sum
	where totalslots = (select max(totalslots) from sum);
```

### List the total slots booked per facility per month, part 2

### List the total hours booked per named facility

### List each member's first booking after September 1st 2012

### Produce a list of member names, with each row containing the total member count

### Produce a numbered list of members

### Output the facility id that has the highest number of slots booked, again

### Rank members by (rounded) hours used

### Find the top three revenue generating facilities

### Classify facilities by value

### Calculate the payback time for each facility

### Calculate a rolling average of total revenue

## Date

### Produce a timestamp for 1 a.m. on the 31st of August 2012

### Subtract timestamps from each other

### Generate a list of all the dates in October 2012

### Get the day of the month from a timestamp

### Work out the number of seconds between timestamps

### Work out the number of days in each month of 2012

### Work out the number of days remaining in the month

### Work out the end time of bookings

### Return a count of bookings for each month

### Work out the utilisation percentage for each facility by month

## String

### Format the names of members

### Find facilities by a name prefix

### Perform a case-insensitive search

### Find telephone numbers with parentheses

### Pad zip codes with leading zeroes

### Count the number of members whose surname starts with each letter of the alphabet

### Clean up telephone numbers

## Recursive

### Find the upward recommendation chain for member ID 27

### Find the downward recommendation chain for member ID 1

### Produce a CTE that can return the upward recommendation chain for any member

