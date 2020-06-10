2015-09-15

DBMS: ...

Every DBMS is based on some data model: the structure, constraints on the content of data, operations on the data.
Some specific ones: network and hierarchical data models, relational data model, semistructured data model

Relational: based on the concept of relations of math.
Tables of rows and columns

example: a dataset scraped from twitter, called metadata, just a bunch of texts.

but say getting information from this with cutomized codes, it's gonna be nonstandardized since everyone shares his one idea. and for large dataset, it's inefficient. this is where DBMS kicks in.

defining a scheme that expresses its structure.
creating an instance that contains the data.
writing some queries on the data...

##What a DBMS provides
- ability to specify the logical structurr of the data
	- explicitly
	- and have it enforced
- ability to query or modify the data.
- good performance under heavy loads.
- durability of the data.
- concurrent access by multiple users/processes

##overall architecture of DBMS
- the dbms sits between the data and the users or between the data and an ...
- ...

##a semi-structured example
- an xml dataset scraped from imdb.com
- no schema required, no instance made
- we can immediately write queries on the data
- a much *looser* one

##what this course is about
- implementation of the DBMS itself
- using DBMSs:
	- defining schemas and instances
	- writing queries
	- connecting to code written in a general-purpose language (e.g. Java!)
	- rigorous underlying principles

##administrative info
Contact: website and piazza
**office hour**: Tuesday 3-5pm, BA3219
Email: nosayba@cs.toronto.edu

##marking scheme
- 3 assignments 30%
- Weekly lecture prep 7% due on Sundays 11pm
- Weekly in-class exercise 3% due in lectures
- midterm 15% October 27 first hour in class
- final 45% 

#relational model

Recap:
- relation or table

##relations in math
- a domain is a set of values
- suppose D_1, D_2, ... D_n are domains.
	- the **Cartesian product** D_1x...xD_n is the set of all tuples
	- a mathematical relation is s subset of Cartesian product
- our database tables are relations too

##relation schemas vs instances
- Schema: definition of the structure of the relation
- example: team have 3 attributes; no two teams can have the same coach.
- our database...
- notation for expressing a relation's schema: Team(Name, HomeField, Coach)
- instance: particular data in the relation
- instances change constantly; schemas rarely
- conventional databases store the current version or the data. ...

##terminology
- relation(table)
- attribute(column). Optionally we can specify that attributes have domains like types in a programming language.
- tuple(row)
- arity of a relation: number of attributes (columns)
- cardinality of a relation: number of tuples (rows)

##relations are sets
- a relation is a set of tuples, which means:
	- uniqueness of elements, no repitive elements
	- order of the tuples does not matter
- in another model, relations are bags -- a generalization of sets that allows duplicates
- commercial DBMS use this model
- but we will stick with the original one

##database schemas and instances
- database schemas: a set of relation schemas
- database instances: a set of relation instances

##superkeys
- superkey: a set of one or more attributes whose combined values are unique:
	- I.e., no two tuples can have the same values on all these attributes
	- exmaple: a relation called Course, with attributes: department code, course number, course name.
		- one tuple might be <"csc", "343", "introduction to databases">
		- what is superkey for this relation? For sure all attributes combined together is a superkey. Probably department code + course number is another one.
	- questions
		- does every relation have a superkey? Yes at least one
		- can a relation have more than one superkey? Yes, could be more.

##key
- key: a minimal superkey (a minimal set of attributes that make the combined value unique)
	- I.e., you may not remove an attribute from a key, and still have a set of attributes whose combined values are unique.
- what is a key for the Course relation?
	- Course(deptCode, cNumber, cName)
	- deptCode, cNumber
- can a relation have more than one key?
	- Student(student#, UTORid, surname, firstname,gpa) has either student# or UTORid as its key
- so for our previous example, Teams(Name, HomeField, Coach), Name and HomeField forms a key
- aside: called superkey because it is a superset of some key, but necessarily a proper superset

##coincidence vs key
If a set of attributes is a key for a relation
- it does not mean merely that "there are no duplicates" in a particular instance of the relation
- it means that **in principle** there cannot be any

Often we have to invent an artificial new attribute to ensure all tuples will be unique
- this predates databases, e.g., SIN, ISBN number

...

Example: movies schema

##foreign key
- the referring attribute is called a foreign key because it refers to an attribute that is a key in another table
- ...
- ...

##declaring foreign keys

