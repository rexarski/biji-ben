#lecture 6

2015-10-20

A prep question recap:

	country(code, name, continent, population)
	countrylanguage(countrycode, countrylanguage, isofficial, percentage)

Find all countries where 'English' is the most commonly spoken language based on percentage. Report the country names only (as attribute 'country'); do not include any duplicates.

Example:

code | clang | isoff | perct
---- | ----- | ----- | ------
1    | Eng   | t     | 80
1    | Fr    | f     | 20
2    | Eng   | t     | 10
2    | Sp    | f     | 90
3    | Fr    | t     | 50
3    | Sp    | f     | 50

Code:

	SELECT DISTINCT name AS country
	FROM countrylanguage c1, country
	WHERE countrylanguage = 'English' AND percentage >= ALL (
		SELECT percentage
		FROM countrylanguage c2)
		WHERE c2.countrycode = c1.code

------------

midterm next week

oct 27 6-7 pm @BR200

- up to embedded SQL
- practice writing:
	- RA queries
	- SQL queries + aggregates + subquereies
	- Views
- understand the rest of the material, of course

##database modifications
- queries return a relation
- a modification command does not; it changes the databse in some way
- 3 ways: insert, delete, update

## 2 ways to insert

	INSERT INTO <<relation>> VALUES <<list of tuples>>;

	INSERT INTO <<relation>> (<<subquery>>);

- insert into empty/non-empty table

- naming attributes in INSERT
	- insert tuples, don't have values for all attributes
	- NULL and default value

	CREATE TABLE Invite (
		name TEXT,
		campus TEXT DEFAULT 'StG',
		email TEXT,
		age INT);
	INSERT INTO Invite VALUES
	('Mark', 'StG', 'm@m.com', 18);
	INSERT INTO Invite(name, email)
	(	SELECT firstname, email
		FROM Student
		WHERE cgpa > 3.4);

here campus get default value, age gets NULL

## deletion

- delete tuples satisfying a condition

	DELETE FROM <<relation>>
	WHERE <<condition>>;

- delete all tuples

	DELETE FROM <<relation>>

example:

	DELETE FROM Course
	WHERE NOT EXISTS (
		SELECT *
		FROM Took JOIN Offering
					ON Took.oid = Offering.oID
		WHERE
			grade > 50 AND
			Offering.dept = Course.dept AND
			....
	)

## udpates

	UPDATE <<relation>>
	 SET <<list of attribute assignments>>
	 ...

	UPDATE Student
	SET campus = 'UTM'
	WHERE sid = 99999;

	UPDATE Took
	SET grade = 50
	WHERE grade < 47 AND grade > 53

## table attributes have types

- when creating, must define the type of each attribute
- analogous to declaring....

## basic types
- CHAR(n): fixed-length string of n characters. Padded with blanks if necessary.
- VARCHAR(n): variable-length string of up to n characters.
- TEXT: variable-length, unlimited. Not in the SQL standard, but psql and others support it.
- INT = INTEGER
- FLOAT = REAL
- BOOLEAN
- DATE
- TIME
- TIMESTAMP

	'Shakespeare''s Sonnets'

###more
- defined in the SQL standard...

##user-defined types
- defined in terms of a built-in type
- make more specific by defining constraints (default value, etc.)

	create domain Grade as int
		default null
		check (value >= 0 and value <= 100);

command `check` wants a specific constraint to be applied

## semantics of type constraints
- checked every time a 

- default value for a type is used when no value has been specified
- useful. run a query and insert the resulting tuples into a relation -- even if the query does not give values for all attributes
- table attributes can also have default values
- difference:
	- attribute default: for that one attribute in that one table
	- type default: for every attribute defined to be of that type

## key constraints
- declaring a set of one or more attri are the PRIMARY KEY for a relation means:
	- form a key (unique, no subset is)
	- their values never be null
- optimize for searches by this set of attri
- every tbl must have 0 or 1 primary key
	- a tbl have no primary key but in practice, every tbl should have one
	- cannot declare more than one primary key

## declaring primary keys
- for a single-attri key can be part of the attri def
	
	create table Blah (
	ID integer primary key,
	name varchar(25));

- can be at the end of the table def

	
		
## uniqueness constraints
- declaring a set of one or more attri are the PRIMARY KEY for a relation means:
	- form a key (unique, no subset is)
	- their values can be null

...

two ways to declare too

	create table Blah (
		ID integer,
		name varchar(25),
		unique (ID));

## foreign key constraints

- eg in table Took:
	
	foreign key (sID) references Student

- means that attr sID in this table is a foreign key that references the primary key of table Student
	- every value for sID in this table must actually occur in the Student table
- requirements
	- must be declared either as primary keys or foreign keys?

## declaring foreign keys
- declare with att or as a separate table element
- can reference attr that are not the primary key as long as they are unique; just name them

	create table People (
		SIN integer primary key,
		name text,
		OHIP text unique);

	create table Volunteers (
		email text primary key,
		OHIPnum text references People(OHIP));


## possible policies
- cascade: propagate the change to the referring table
	- e.g. if a Student leaves university, delete all their grades in Took
- set null: set the referring attr to null, primary cannot be. (not the most practical reaction)
- restrict

