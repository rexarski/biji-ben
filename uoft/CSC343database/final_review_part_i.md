# lecture recap after midterm

2015-10-30

# week 6

## SQL data definition language (DDL)

- database modifycation
	- queries return a relation
	- a **modification** command does not; it changes the database
	- 3 kinds
		- *insert* a tuple or tuples
		- *delete* a tuple or tuples
		- *update* the value(s) of an existing tuple or tuples
	- 2 ways to insert

			INSERT INTO <<relation>> VALUES <<list of tuples>>;
			INSERT INTO <<relation>> (<<subquery>>);

		- naming attributes
			- don't have all values for all attributes, use NULL or default values for the rest

					CREATE TABLE Invite (
						name TEXT,
						campus TEXT DEFAULT 'StG',
						email TEXT,
						age INT);
					INSERT INTO Invite VALUES
					('Mark', 'StG', 'm@m.com', 18);
					INSERT INTO Invite (name, email)
					(	SELECT firstname, email
						FROM Student
						WHERE cgpa > 3.4	);

			- name and email are values from the query, campus gets default value, age gets NULL

	- deletion
		- delete tuples satisfying a condition:

				DELETE FROM <<condition>>
				WHERE <<condition>>;

		- e.g.

				DELETE FROM Course
				WHERE NOT EXISTS (
					SELECT *
					FROM Took JOIN Offering
							  ON Took.oid = Offering.oid
					WHERE
						grade > 50 AND
						Offering.dept = Course.dept AND
						Offering.cnum = Course.cnum
				);

		- delete all tuples:

				DELETE FROM <<relation>>;

	- updates
		- change the value of certain attributes in certain tuples to given values:

				UPDATE <<relation>>
				SET <<list of attribute assignments>>
				WHERE <<condition on tuples>>;

		- e.g. update 1 tuple

				UPDATE Student
				SET campus = 'UTM'
				WHERE sid = 999999;

		- e.g. update several tuples

				UPDATE Took
				SET grade = 50
				WHERE grade >= 47 and grade < 50;

- types
	- built-in types and values
		- CHAR(n)
			- fixed-length string of n characters, padded with blanks if necessary
			- string must surround with single quotes `'Shakespeare''s Sonnets`
		- VARCHAR(n)
			- variable-length string of up to n characters
		- TEXT
			- variable-length, unlimited.
			- not supported in sql, but in psql and others
		- INT = INTEGER
			- 37
		- FLOAT = REAL
			- 1.49, 37.96e2
		- BOOLEAN
			- TRUE, FALSE
		- DATE, TIME, TIMESTAMP
			- '2011-09-22'
			- '15:00:02', '15:00:02.5'
			- 'Jan-12-2011 10:25'
	- user defined types
		- defining constraints

				create domain Grade as int
					default null
					check (value >= 0 and value <= 100);

				create domain Campus as varchar(4)
					default 'StG'
					check (value in ('StG', 'UTM', 'UTSC'));

		- constraints on a type are checked every time a value is assigned to an attribute of that type
		- *default* value for a type is used when no value has been specified
- keys and foreign keys
	- key constraints
		- declaring a set of one or more attributes are the PRIMARY KEY for a relation means:
			- they form a **key** (unique, no subset is)
			- their values will **never be null**
		- every table must have 0 or 1 primary key
			- in practice, must be 1
	- declaring primary keys
		- single-attribute key, as part of the attribute definition

				create table Blah (
					ID integer primary key,
					name varchar(25));

		- multi-attribute, the only way is at the end of table definition

				create table Blah (
					ID integer,
					name varchar(25),
					primary key (ID));

	- uniqueness constraints
		- declaring that a set of one or more attributes is UNIQUE for a relation means:
			- they form a **key**
			- their value *can* be **null**
		- can declare more than one set of attributes to be UNIQUE
	- declaring UNIQUE
		- if only one attribute is involved, can be part of the attribute definition

				create table Blah (
					ID integer unique,
					name varchar(25));

		- or at the end (only way for multi-attribute)

				create table Blah (
					ID integer,
					name varchar(25),
					unique (ID));

	- nulls affect unique, as for uniqueness constraints, no two nulls are considered equal.
		- two insertions of `('Stephen', 'Cook')` are not allowed, but two insertions of `(null, 'Rackoff')` are allowed.

	- foreign key constraints

			foreign key (sID) references Students

		- attributes sID in this table is a foreign key that references the primary key of table Student
			- every value for sID in this table actually occur in the Student table
			- must be declared either primary key or unique in the 'home' table
				- i.e., foreign key must be unique or primary key somewhere else!
	- declaring foreign keys
		- similarly, declare with the attribute (only single attribute) or as a separate table element
		- can reference attribute(s) that are not the primary key as long as unique; name them

				create table People (
					SIN integer primary key,
					name text,
					OHIP text unique);

				create table Volunteers (
					email text primary key,
					OHIPnum text references People(OHIP));

	- enforcing foreign-key constraints
		- '**reaction policy**'
			- what's the DBMS *default*
			- can we change it? how?
		- possible policies
			- `cascade`: propagate the change to the referring table
			- `set null`: set the referring attribute(s) to null
			- if nothing said, *defaults* is to forbid the change in the referred-to table
		- syntax for specifying a reaction policy
			- add where specifies the foreign key constraint

					create table Took (
						...
						foreign key (sID) references Student
								on delete cascade
						...
					);

		- reaction policy can specify what to do either
			- `on delete`: when a deletion creates a dangling reference
			- `on update`: when an update creates a dangling reference
			- both, like `on delete restrict on update cascade`
		- reaction can be
			- `restrict`: don't allow the deletion/update
			- `cascade`: make the same deletion/update in the referring tuple
			- `set null`: set the corresponding value in the referring tuple to null
- other constraints and assertions
	- 'check' constraints
		- on an attribute
		- on the tuples of a relation
		- across relations
		- attribute-based 'check' constraints
			- defined with a single attribute and constrain its value
			- can only refer to that attribute
			- can include a subquery
			- e.g.

					create table Student (
						sID integer,
						program varchar(5) check
							(program in (select post from P)),
						firstName varchar(15) not null, ...);

			- condition can be anything could go in a WHERE clause
		- when checked
			- only when a tuple is **inserted** into that relation
			- or its value for that attribute is **updated**
			- if a change **somewhere** else **violates** the constraint, dbms will not notice
	- 'not null' constraints
		- can declare that an attribute of a table is NOT NULL

				create table Course (
					cNum integer,
					name varchar(40) not null,
					dept Department,
					wr boolean,
					primary key (cNum, dept));

		- in practice, many attrs should be **not null**
		- very specific
	- tuple-based 'check' constraints
		- defined as a separate element of the table schema, can refer to any attributes of the table
		- condition can be anything could go in a WHERE clause
		- can conclude a subquery
		- e.g.

				create table Student (
					sID integer,
					age integer,
					year integer,
					college varchar(4),
					check (year = age - 18),
					check college in
							(select name from Colleges));

		- when checked
			- only when a tuple is **inserted** into that relation, or **updated**
			- if a change somewhere else violates the constraint, the DBMS will not notice
	- null affects 'check' constraint
		- a check constraint only fails if it evaluates to **false**, i.e. check will pass a null
		- e.g.

				create table Tester (
					num integer,
					word varchar(10),
					check (num>5));
		- it would allow you to insert (null, 'hello')
		- if you want to prevent this

				create table Tester (
					num integer not null,
					word varchar(10),
					check (num>5));
	- nameing constraints
		- add `constraint <<name>>` before the `check (<<condition>>)`
		- e.g.

				create domain Grade as smallint
					default null
					constraint gradeInRange
						check (value >= 0 and value <= 100);

				create domain Campus as varchar(4)
					not null
					constraint validCampus
						check (value in ('StG', 'UTM', 'UTSC'));

				create table Offering(...
					constraint validCourseReference
					foreign key (cNum, dept) references Course);
		- create table Student, sID is primary key, firstName and surName cannot be null, campus can only be StG, UTM or UTSC.

				CREATE TABLE Student (
					sID INTEGER,
					surName VARCHAR(25) NOT NULL,
					firstName VARCHAR(25) NOT NULL,
					campus VARCHAR(5)
					check (campus in ('StG', 'UTM', 'UTSC')),
					email VARCAR(30),
					cgpa FLOAT,
					PRIMARY KEY (sID)
				);

		- order of constraints doesn't matter, doesn't dictate the order in which they are checked
	- assertions
		- **check** constraints apply to an attribute or table, they can't express constraints *across* tables
		- **assertions** are schema elements at the top level, so *can* express cross-table constraints
		- `create assertion (<name>) check (<predicate>);`
		- assertions are costly because they have to be checked upon every databse update
		- testing and maintenance are also difficult
		- used with great care!
	- triggers
		- assertions are powerful but costly
		- check constraints are less costly but less powerful
		- **triggers** are a compromise between these extremes
			- cross-table constraints as powerful as assertions
			- control the cost by having control over **when they are applied**
			- idea: specify three things
				- event: some types of database action, e.g. `after delete on Courses` or `before update of grade on Took`
				- condition: a boolean-valued expression, e.g., `when grade > 95`
				- action: any SQL statements, e.g., `insert into Winners values (sID, course)`
- Using SQL 'schemas'
	- schema is kind of namespace
	- everything defined (tables, types, etc.) goes into one big pot
	- create different namespaces
	- useful for logical organization, and for avoiding name clashes
	- create a schema
		- already have 'public'
		- `create schema University`
		- dot notation, `University.Student`...
		- when don't use dot notation, referring to a name without specifying what schema it is within, it's in public schema
	- the search path
		- `show search_path`: see the search path
		- `set search_path to University, public;`: set the search path yourself
		- default search path is `"$user", public`
			- schema `"$user"` is not created for you, but if you create it, it's at the front of the search path
			- schema `public` is created for you
	- remove a schema
		- `drop schema University cascade;`
		- `cascade` means everything inside it is dropped too
		- to avoid getting errors if the schema does not exist, add `iff exists`
	- usage pattern
		- use this at the top of every DDL file

				drop schema if exists University cascade;
				create schema University;
				set search_path to University;

	- update schema itself
		- alter: alter a domain or table

				alter table Course
					add column numSections integer;
				alter table Course
					add column breadth;

		- drop: remove a domain, table, or whole schema

				drop table course;

		- different from `delete from course;`; if you drop a table that is referenced by another table, must specify "cascade"
		- this removes all referring rows

## embedded sql

- sql + a conventional language
	- sql is based on **relations**, but conventional languages have no such type
	- solved by
		- feeding tuples from sql to the other language one at a time, and
		- feeding each attribute value into a particular *variable*
- approaches
	- 3 for combining sql and a general purpose language
		- stored procedures (skip)
		- statement-level inferface (skip)
		- **call-level interface**
- call-level interface (CLI)
	- instead of using a pre-processor to replace embedded sql with **calls** to library functions, write those calls yourself
	- eliminates need to preprocess
	- each language has its own set of library functions for this
		- C, SQL/CLI
		- **Java, JDBC**
		- PHP, PEAR DB
- JDBC



# week 7

2015-10-31

## XML & DTDs

- XML
	- HTML to XML
		- similar
			- tags and attributes
			- tree-structured format
		- important differences
			- XML data must be **well-formed**
			- define your own **tags** and **attributes**
			- these describe the *meaning* of the data, imply nothing about its presentation
			- XML was designed to *carry* data, HTML was designed to *display* data
	- what's XML for?
		- record data that **software** needs
		- exchange of information between pieces of software
		- **"self-describing"**
			- schema-like information is part of the data itself
			- e.g.

					<student stnum = "1234" name = "Cindylou Who">
						<address>
							<street>99 Alfalfa Way</street>
							<city>Whoville</city>
						</addrees>
					</student>
	- well-formed vs valid
		- **well-formed XML**
			- just need a single *root* element and proper *nesting* (with closing tag)
			- any tag or attribute can go anywhere
		- **valid XML**
			- a valid XML must be **well-formed** + conforms a **DTD**
			- a "DTD" (**document type definition**) specifies
				- what tags and attributes are permitted, 
				- where they can go and 
				- how many there must be
			- a valid XML file is one that has a DTD and follows the rules specified in its DTD
	- well-formed XML
		- begin document with a **declaration**
			- `<?xml ... ?>`
		- declaration for a document that is merely well-formed (no DTD!)
			- `<?xml version="1.0" standalone="yes" ?>`
		- the rest is a single **root tag** with tags nested inside it
	- tags
		- *matched* pairs
		- text or nested tags in between
		- e.g.

				<tf-question qid="Q637" solution="False">
					<question>
						The Prime Minister, Justin Trudeau, is Canada's Head of State.
					</question>
				</tf-question>

		- or unmatched, with a slash placed inside
			- `<response qid="Q637" answer="False" />`
		- tag names case-sensitive
	- attributes
		- an opening **tag** can have **attribute** name-value pairs within it
		- pairs are separated by blanks
		- extreme cases
			- if all the info is in the attributes, the tag becomes empty, i.e. you don't need to use attributes

					<tf-question>
						<qid>Q637</qid>
						<solution>False</solution>
						<question>
							The Prime Minister...
						</question>
					</tf-question>

			- or all data via attributes

					<tf-question qid="Q637" solution="False" question="The Prime Minister ..."/>

			- it's just a design decision
				- in most cases, something in between makes more sense
				- matched **tags** make sense when you need structure within
				- **attributes** make sense when you want something like keys and foreign keys
	- check well-formedness
		- `xmllint` command on cdf, default is to check merely for well-formedness
		- `xmllint -- debug`, outputs an annotated tree of the parsed document, useful for diagnosis of problems
- valid XML with DTDs
	- content of a DTD
		- a series of rules
		- an `ELEMENT` rule defines an element that may occur, and what can be within its opening and closing tags
		- an `ATTLIST` rule defines an attribute of an element
		- order of the rules doesn't matter
	- ELEMENT rules
		- form `<!ELEMENT <<name>> (<<subcomponents>>)>`
		- `name`: the element's tag
		- `subcomponents` can be
			- a comma-separated list of elements
				- the elements must occur inside, and in the order given
			- `#PCDATA`
				- the element contains simply text (no subelements)
			- `EMPTY`
				- "empty" element, may have attributes, but not matching opening & closing tags
		- e.g.

				<!ELEMENT INGREDIENT (NAME, QUANTITY)>
				<!ELEMENT NAME (#PCDATA)>
				<!ELEMENT QUANTITY EMPTY>

		- more expressiveness for subcomponents
			- pipe symbol `|` to indicate alternatives, `(something | something2)`
			- specify multiplicity as follows
				- `*` means zero or more
				- `+` means one or more
				- `?` means zero or one
			- can use brackets for grouping
	- ATTLIST rules
		- form `<!ATTLIST <<elName>> <<attName>> <<type>> <<optionality>> >`
		- `elname`: the element whose attribute this is
		- `attName`: the name of this attribute
		- `type`: either `CDATA` or a list of possible values, e.g., `True | False`
		- `optionality`: either `#REQUIRED` or `#IMPLIED` (which means optional)
		- can define multiple attributes at once

				<!ATTLIST person SIN CDATA #REQUIRED
								 age CDATA #IMPLIED>

	- using a DTD
		- XML declaration must say the document is not standalone
			- `<?xml version="1.0" standalone="no" ?>`
		- 3 possible places for the DTD
			- in the same file, between the declaration and the XML content
			- in a separate file on the same computer, specify the filename or give the full or relative path
			- at a URL
		- you must specify what the root element will be
	- DTD in the same file

			<?xml version="1.0" standalone="no" ?>
			<!DOCTYPE People [
				<!ELEMENT People (Person*)>
				<!ELEMENT Person (#PCDATA)>
			]>
			<People>
				<Person>Tommy Douglas</Person>
				<Person>Terry Fox</Person>
				<Person>Louise Arbour</Person>
				<Person>Chris Hadfield</Person>
			</People>

	- DTD in another file

			<?xml version="1.0" standalone="no" ?>
			<!DOCTYPE People SYSTEM "people.dtd">
			<People>
				<Person>Tommy Douglas</Person>
				<Person>Terry Fox</Person>
				<Person>Louise Arbour</Person>
				<Person>Chris Hadfield</Person>
			</People>

	- DTD at a URL

			<?xml version="1.0" standalone="no" ?>
			<!DOCTYPE People SYSTEM "http://www.cs.utoronto.ca/xyyz/people.dtd">
			<People>
				<Person>Tommy Douglas</Person>
				<Person>Terry Fox</Person>
				<Person>Louise Arbour</Person>
				<Person>Chris Hadfield</Person>
			</People>		

- "keys" and "foreign keys"
	- motivation
		- like relational model, want **unique** identifiers, and **refer** in one place to some data in another place
		- like the DTD to express these rules and our tools to enforce them
		- but DTDs don't have full capability, although having some features in this direction
	- using ID to enforce uniqueness
		- to specify that values must be unique
			- make an attribute of type `ID` rather than `CDATA`
			- `<!ATTLIST mc-question qid ID #REQUIRED>`
		- values of `ID` attr are restricted
			- must not begin with a digit
			- must not have blanks
	- limitations of ID
		- uniqueness is enforced across **all** IDs in the file
		- e.g.
			- Quiz.xml

					<?xml version="1.0" standalone="no"?>
					<!DOCTYPE Quiz SYSTEM "quiz.dtd">
					<Quiz quizID="csc343" title="Homework Set 1">
						<Question QID="N-15" weight="2"/>
						<Question QID="MC-08" weight="2"/>
					</Quiz>

			- Quiz.dtd

					<!ELEMENT Quiz (Question+)>
					<!ATTLIST Quiz quizID CDATA #REQUIRED>
					<!ATTLIST Quiz title CDATA #REQUIRED>
					<!ATTLIST Quiz hints (yes|no) #REQUIRED>
					<!ELEMENT Question EMPTY>
					<!ATTLIST Question QID ID #REQUIRED>
					<!ATTLIST Question weight CDATA #REQUIRED>

	- using IDREF to enforce referential integrity
		- to specify that a value must refer to some ID:
			- make an attribute of type `IDREF`
			- `<!ATTLIST response qid IDREF #REQUIRED>`
			- can allow an attribute to have a *list* of values, each of which references some ID: 
			- `<!ATTLIST response qid IDREFS #REQUIRED>`
	- limitations of IDREF
		- needs only to refer to **any ID** in the file, not specifially to one of a particular type
	- checking for validity
		- `xmllint --valid` command on cdf
	- limitations of DTDs
		- ID and IDREF are a pale imitation of keys and foreign keys
			- all ID values are treated as a single set
		- ID and IDREF only work within a single file
			- references to an ID in another file are flagged as errors
			- duplicate ID value across files cannot be detected
		- no other types of constraints
		- the only data type is string
		- hard to specify contents but allow them in any order
	- XML schema
		- greater expressive power
			- rich set of built-in types, + user-defined types
			- finer control over sequences of sub-elements
			- more effective keys and foreign keys
		- more complex
		- XML schema definitions (XSDs) are XML documents themselves
			- describe "elements" and
			- the things doing the describing are themselves "elements"