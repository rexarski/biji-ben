# lecture 8

2015-11-03

# last time: query languages for xml

- xml is great recording data that software needs, exchange of info between softwares
- self-describing
	- schema-like info part of the data itself
	- structure and content at the same time
- well-formed and valid
	- well-formed is a subset of valid
	- well-formed:
		- single root element and proper nesting
	- valid:
		- well-formed + conforms to a DTD
		- DTD (document type definition) specifies what tags and attributes are permitted, where they can go, and how many there must be

# xml & dtd model

- xml document is a tree
- manipulating xml
	- extract parts of interest
	- transform document
	- relate (= join) different parts of a file (or different files)
	- need queries
	- xml query languages
		- XPATH
		- XQUERY

# XPath query language

- queries over hierarchical data
	- observe: all xml documents are trees
		- each element has one path to the document root
		- similar to a file system
	- slash '/' usage, similar to file systems
	- specify full or partial paths
		- `/Students/Student/Name`
		- returns the Name of each Student element under Students
	- with selection:
		- 
		- 
- write and run an XPath query
	- create a file containing: `fn:doc("<<xml file>>")<<path expression>>`
	- `fn:doc` is a function parses the document and evaluates to a document tree
	- `@` takes us to an attribute; otherwise we go to a subelement
	- each slash takes us down one level in the tree
	- run it on cdf: `galax-run query.xq`

- result of a path expression
	- a seq of ..
	- 

- homogeneous or heterogeneous results
	- often yields homo results
		- `doc("quiz.xml")//qeustions/mc-question`
		- `doc("quiz.xml")//tf-question/@solution`
	- but some don't
		- `doc("quiz.xml")/quiz/questions/*/*`
		- yields a mix of question elements and option elements


1. get the solution to every question (regardless of the question type)

		doc("quiz.xml")/quiz/questions//@solution

		or
		
		doc("quiz.xml")/quiz/questions/*/@solution

2. get the elements of the true-false questions only

		doc("quiz.xml")/quiz/questions/tf-question

3. get the text of the multiple-choice question which has the QID 'Q888'

		doc("quiz.xml")/quiz/questions/mc-question[@qid="Q888"]/question/text()

4. for the student with ID s555555555, list the second response answer recorded for them (need to extract some component with a certain order) hint: staring index is 1 not 0

		doc("quiz.xml")/quiz/class-responses/student[@sid="s555555555"]/response[2]/@answer

5. now return that answer to question 4, enclosed by a <secondAns></secondAns> tag (hint: use `{}` to make it dynamic)

		<secondAns>{doc("quiz.xml")/quiz/class-responses/student[@sid="s555555555"]/response[2]/@answer}</secondAns>
		
6. write an XQuery FLWOR expression that returns the text for each multiple-choice question in quiz.xml, along with the number of options available for that question. hint: use `count(option)`

		for $q in doc("quiz.xml")/quiz/question/mc-question
		return ($q/question/text(), $q/count(option))

# other axes

- axes
	- more modes of navigation, called axes
- syntax
	- notation: `/<<axis>>::`
	- where axis is one of
		- `child`
		- `parent`
		- `attribute`
	- if not specified as an axis, default is used: `child`
	- so path expression
		- `fn:doc("course.xml")/Students`
		- is shorthand for: `fn:doc("course.xml")/child::Students`
	- attribute ...
	- other shorthand for axes
		- `//` for the descendant-or-self axis
			- `fn:doc("courses.xml")//CrsTaken` is `fn:doc("courses.xml")/descendant-or-self::CrsTaken`
		- Dot(`.`) is for self axis
	- more
		- `parent`
		- `ancestor`
		- `ancestor-or-self`
		- `following-sibling`
		- `preceding-sibling`

# XQuery query language

- extends XPath (more powerful)
- same data model
	- a document is a tree
	- a query result is a sq of items from the doc
- an expression language
	- any XQuery expression can be an argument of any other XQuery expression
- item seq are flattened
	- xquery sometimes generates nested seq, always flattened
	- `(1 2 () 3 4) = (1 2 3 4)`
- `FLWOR` expressions

		let $d := fn:doc("bank.xml")
		for $tfq in $d//TFQuestion
		where $tfq/@answer="True"
		order by $qid
		return $tfq/question

	- return is mandatory
	- the semantics fo return is surprising:
		- not terminate the FLWOR expression
		- specifies values produced by the current iter
		- seq of these is the result of FLWOR expression
	- notes about syntax
		- keywords case-sensi
		- variable begins with `$`
		- rule : (for|let) + where? + order by? + **return**
	- `for` vs `let`
		- `for` is like `for x in [99, 42, 101, 5]`
		- `let` is like `let ...`