# mid bulletpoint review

2015-10-23

## RA

- relation/table
- schema
	- definition of the structure of the relation
- instance
	- particular data in the relation
- attribute
- tuple
- arity (number of attributes)
- cardinality (number of tuples)
- a relation is a set of tuples
	- no duplicate tuples
	- order does not matter
- database schema
	- a set of relation schemas
- database instance
	- a set of relation instances
- superkey
	- a set of one or more attributes whose combined values are unique
- key
	- a minimal superkey
	- 'superkey' because it is a superset of some key
- integrity constraint
- foreign key
	- referring attribute -- an attribute is a key in another table
	- declaring foreign key with notation -- referential integrity constraints/inclusion dependencies
- RA basics
	- operands --  tables
	- operators
		- select: choose rows
			- sigma
		- project: choose columns
			- pi
			- eliminate duplicates
		- cartesian product
			- R1 x R2
		- natural join
			- R bowtie S
			- cartesian product + select + project
			- commutative
			- associative
			- problems: overmatch and undermatch
		- theta join
			- bowtie with condition as subscript
			- cartesian product + select
			- the result is cartesian product followed by select (not natural join!)
		- for dangling tuples
			- outer join: leaves those in, adds null values when no value exists
				- left, right, full
		- assignment operator
			- R:= expression
			- change name of attributes/relations
		- rename operation
			- rho
			- can rename within expression
	- set operation
		- intersection, union, difference
- specific types of query
	- max (min is analogous)
		- take a detour
		- pair tuples and find those that are not the max
		- subtract from all
	- k or more
		- make all combos of k different tuples that satisfy the condition
	- exactly k
		- [k or more - (k+1) or more]
	- every?
		- make all combos that should have occured
		- subtract those that did occur to find those that didn't always. These remaining are the failures
		- subtract the failures from all to get the answer
		- subtract

## SQL (DML)

- structured query language 
	- data manipulation language
	- data definition language
- PostgreSQL

- can select from 1 table, or more

		SELECT attributes
		FROM Table1, Table2
		WHERE <condition>;

- temporarily rename a table (like rho in RA)

		SELECT e.name, d.name
		FROM employee e, department d
		WHERE d.name = 'marketing' and e.name = 'Horton';

- `*` in SELECT: all attributes
- rename attribute using AS

		SELECT name AS title, dept
		FROM Course
		WHERE breadth;

- conditions in WHERE
	- comparison operators:  =, <>, <, >, <=, >=
	- boolean operators: AND, OR, NOT

- ORDER BY
	- ORDER BY <<attribute list>> [DESC]
	- ascending is default
	- ORDER BY  a+b

- case-sensitivity and whitespace
	- not case-sensitive!
	- string is!
	- whitespace is ignored

- string concatenation
	- dept || cnum, e.g. 'csc343'

- expression that is a constant

		SELECT name, 'satisfies' AS breathRequirement
		FROM Course
		WHERE breadth;

- pattern operators
	- <<attribute>> LIKE <<pattern>>
	- <<attribute>> NOT LIKE <<patern>>
	- pattern is quoted string
		- `%` means any string
		- `_` means single character

			SELECT *
			FROM Course
			WHERE name LIKE '%Comp%';

			WHERE phone LIKE '268______'

			WHERE entry NOT LIKE '%est'

- aggregation
	- compute across values in a column
		- SUM, AVG, COUNT, MIN, MAX (in SELECT)
		- COUNT(*) counts the number of tuples
	- DISTINCT
	- duplicates are not eliminated by default when using SELECT

- grouping
	- GROUP BY <attributes>
	- rows are grouped by values in attributes
	- any aggregation applied only within groups
	- SELECT can't include un-aggregated cols

			SELECT oID, avg(grade) as offavg, count(*) as numstudents
			FROM took
			GROUP BY oID;

	- restirction
		- if any aggregation is used, each element of the SELECT list must be either
			- aggregated, or
			- an attribute on the GROUP BY list
		- otherwise, it's meaningless to appear there

- HAVING
	- WHERE decides which tuples to keep
	- HAVING decides which groups to keep
	- HAVING may refer to attributes only if they are either
		- aggregated, or
		- an attribute on the GROUP BY list
		- same as requirement as for SELECT with aggregation

				SELECT oID, avg(grade) as offavg
				FROM took
				GROUP BY oID
				HAVING avg(grade)>80

				SELECT oID, avg(grade) as offavg
				FROM took
				GROUP BY oID
				HAVING oID <= 5
				ORDER By oID

- set operations
	- tables can have duplicates in SQL
	- SELECT-FROM-WHERE removes duplicates
	- (<<subquery>>) UNION (<<subquery>>)
	- (<<subquery>>) INTERSECT (<<subquery>>)
	- (<<subquery>>) EXCEPT (<<subquery>>)
	- brackets mandatory
	- operands are queries, cannot use relation names

			(SELECT sid
			 FROM Took
			 WHERE grade > 95)
			 	UNION
			(SELECT sid
			 FROM Took
			 WHERE grade < 50)

	- SELECT-FROM-WHERE uses bag semantics by default
	- set(INTERSECT/UNION/EXCEPT) uses set semantics by default
	- controlling
		- keep duplicates with SFW
			- SELECT DISTINCT
		- remove duplicates with set operation
			- UNION/INTERSECT/EXCEPT ALL

- views
	- a view is a relation defined in terms of stored tables (called basd tables) and possibly also other views
	- CREATE VIEW topresults as

- SQL joins
	- dangling tuples
	- outer join preserves dangling tuples by padding them with NULL
	- inner join doesn't pad with NULL
	- don't use natural join! dangerous
	- there are keywords INNER OUTER, but never used

- null value
	- missing value
	- inapplicable attribute
	- checking null
		- IS NULL
		- IS NOT NULL

				SELECT *
				FROM Course
				WHERE breadth IS NULL;

	- arithmetic expression
		- always NULL
	- comparison operator
		- UNKNOWN
			- UNKNOWN OR FALSE -> UNKNOWN
			- UNKNOWN OR TRUE -> TRUE
			- UNKNOWN AND TRUE -> UNKNOWN
			- UNKNOWN AND FALSE -> FALSE
			- NOT UNKNOWN -> UNKNOWN
				- ternary logic tricks
					- TRUE = 1
					- FALSE = 0
					- UNKNOWN = 1/2
					- AND = min(...)
					- OR = max(...)
					- NOT = 1 - x
	- aggregation
		- aggregation ignores NULL
		- if ALL values are NULL in a col, the result of aggregation is NULL
		- only `count(*)` counts all tuples including NULL

- subqueires
	- subqueires in FROM clause
		- must be parenthesized
		- must name the result, can be referred in outer query

				SELECT sid, dept || cnum as course, grade
				FROM Took,
					(SELECT *
					 FROM Offering
					 WHERE instructor='Horton') Hoffering
				WHERE Took.oid = Hoffering.oid;

	- subqueries as a value in WHERE
		- if guaranteed to produce one tuple, then can be used as a value

				SELECT sid, surname
				FROM Student
				WHERE cgpa > 
					(SELECT cpga
					 FROM Student
					 WHERE sid = 99999);

	- if subquery returns NULL
		- evaluates to UNKNOWN, no tuples returned
	- subquery can return multiple values, can make comparison
	- ANY
		- x <<comparison>> ANY (<<subquery>>)
		- or x <<comparison>> SOME (<<subquery>>)
		- ture iff the comparison holds for at least one tuple in the subquery result
		- x can be a list of attributes, but this feature is not supported by psql
	- ALL
		- x <<comparison>> ALL (<<subquery>>)
		- true iff the comparison holds for every tuple in the subquery result
		- can be a list of attributes, but this feature is not supported by psql
	- IN
		- x IN (<<subquery>>)
		- true iff x equals at least one of the tuples in the subquery result
		- can be a list of attributes, but this feature is not supported by psql

- summary: where subqueries can go
	- as a relation in a FROM clause
	- as a value in a WHERE clause
	- with ANY, ALL, IN or EXISTS in a WHERE clause
	- as operands to UNION, INTERSECT or EXCEPT
	- reference: textbook section 6.3





