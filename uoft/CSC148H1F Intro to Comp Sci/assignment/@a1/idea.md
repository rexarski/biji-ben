#student management console

##front end
- command line (text-based) interface
- enter commands or files

##back end
- class and methods -> execute the command-line inputs

##sms
- use split to turn str into a list of words
- student name and course name are single word
- case-sensitive

- create student (name)
- enrol (name) (course)
	- no name exists: ERROR: Student (name) does not exist.
	- already in that course: do nothing
	- full: 30 students enrolled. ERROR: Course (course) is full.
- drop (name) (course)
	- no such name in course: ERROR: Student (name) does not exist.
	- not in course at all. do nothing.
	
- list-courses (name)
	- list all the courses (name) is taking in the format of (name) is taking (course1), (course2), ... (course-n), where the courses are listed in alphabetical order.
	- if no (name), print ERROR: Student (name) does not exist.
	- if (name) isn't enrolled in any courses, print (name) is not taking any courses.
	
- common-courses (name1) (name2), print common courses of two students, in the format (course1), (course2), ...(course-n)
	- alphabetical order
	- one or two name does not exist, print ERROR: Student (name1/2) does not exist. if both, then separate lines.
	- if no common courses, print []

- class-list (course): print students enrolled in this course in alphabetical order.
	- if no one in this course, print "No one is taking (course)."
	
###other commands
- exit (given)
- undo
	- only undo (create, drop, enrol)
	- cannot undo an undo
	- no remaining command to undo, print Error: No commands to undo.
	- if create student (name) failed, already existed (name), then undo should do nothing. Don't delete student.
	- similarly for enrol/drop
	- stack
	
- undo (n)
	- n should be positive natural only, o.w. print ERROR: (n) is not a positive natural number.
	- undo (n) == undo n times
	- if no n steps available, then print ERROR: No commands to undo.
- any other unrecognized command: print Unrecognized command!

------
##DID NOT FOLLOW MARKDOWN SYNTAX BELOW:

input_string = 'Im saying      stuff
list_thing = input_string.split()
if list_thing[0] == 'create':
	if list_thing[1] == 'student':

Making sms.py -> Rui

create student -> Su Young
enrol student -> Rui
drop student -> Su Young
list-courses (of student) -> Rui
common-courses student1 student2 -> Su Young 
class-list -> Rui
exit

undo -> Su Young

xxx - name
yyy - course name

split -> [...]
check 
check len
- if 3
	- could be create, enrol, drop, common
	- if [0:1] == ["create", "student"]
		- call create function
	- elif [0] == "enrol"
		- call enrol function
	- elif [0] == "drop"
		- call drop function
	- elif [0] == "common-course"
		- call common function (note: if name valid, duplicated name)
	- else:
		unrecognized command 
		UofT.undo_stack.push(1)

- elif 2
	- could be list, class-list, undo n
	- if [0] == "list-courses"
		- call list-courses function
	- elif [0] == "class-list":
		- call class-list function
	- elif [0] == 'undo':
		- call undo n function
	- else:
		unrecognized command
		UofT.undo_stack.push(1)

- elif input == ['undo']
	- call undo
	
- else:
	print unrecognized command!
	UofT.undo_stack.push(1)


create student xxx
enrol xxx yyy
drop xxx yyy
list-courses xxx
common-courses xxx xxx #ask them
class-list yyy
undo
undo n

valid_inputs = {
	'create': 3
	'enrol': 3
	
	
if valid_inputs(command[0]) == len(command):
	it's a valid command
	
	


