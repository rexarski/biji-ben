class EmptyStackError(Exception):    pass
class Stack:    def __init__(self):        self.command_stack = []
    def push(self, item):        self.command_stack.append(item) 
    def pop(self):
        try:
            self.comand_stack.pop()
        except IndexError:
            raise EmptyStackError			
    def is_empty(self):
        return len(self.command_stack) == 0		
class School:
    def __init__(self):
        self.name = 'UofT'
        self.student_list = []
        self.course_list = []
        self.undo_stack = Stack()			def student_create(self, name):		if object_caller(name, self.student_list)[0]:			print ("ERROR: Student", name, "already exists.")			self.undo_stack.push(1)						else:			self.undo_stack.push(('create', name))			x = Student(name)			self.undo_stack.push(x)	def course_drop(self, name, course):		if not (object_caller(name, self.student_list)[0]):			print ("ERROR: Student", name, "does not exist")			self.undo_stack.push(1)					else:			target_student = object_caller(name, self.student_list)[1]			if not (course in target_student.course_list):				self.undo_stack.push(1)			else:				target_course = object_caller(course, self.course_list)[1]								# NO IDEA IF THIS WORKS.  CHECK LATER.  Not sure if the self parameter is needed (unlikely)				target_student.course_drop(course)				target_course.student_removal(name)								self.undo_stack.push(('drop', name, course))							def common_check(self, name1, name2):				# This is done first, simply because it will happen no matter what anyway.		self.undo_stack.push(1)				if not (object_caller(name1, self.student_list)[0]):			print ("ERROR: Student", name1, "does not exist")				if not (object_caller(name2, self.student_list)[0]):			print ("ERROR: Student", name2, "does not exist")					# A bit confusing, but this elif statement verifies that both students exist.		elif (object_caller(name1, self.student_list)[0]):					student1 = object_caller(name1, self.student_list)[1]			student2 = object_caller(name2, self.student_list)[1]						student1.common_check(student2)				def undo_check(self):		undo_variable = self.undo_stack.pop()				if type(undo_variable) == tuple:			self.undo_it(undo_variable)				def undo_it(self, undo_tuple):				if undo_tuple[0] == 'create':			name = undo_tuple[1]			poor_student = object_caller(name, self.student_list)[1]			self.student_list.remove(poor_student)					elif undo_tuple[0] == 'enrol':				name, course = undo_tuple[1], undo_tuple[2]						target_student = object_caller(name, self.student_list)[1]			target_course = object_caller(course, self.course_list)[1]						target_student.course_drop(course)			target_course.student_removal(name)					elif undo_tuple[0] == 'drop':			pass
class Student:
    def __init__(self, name):
        self.name = name
        self.course_list = []	def course_drop(self, course):		self.course_list.remove(course)			def common_check(self, other_student):		common_list = []		# common_list = [x for x in student1.course_list if x in student2.course_list]		# Use this list comprehension, after verifying every thing else works (aka. not priority)		for course in student1.course_list:			if course in student2.course_list:				common_list.append(course)						if len(common_list) >= 1:			common_list.sort()			print (', '.join(common_list))		else:			print ()	
class Course:
    def __init__(self, name, student):
        self.name = name
        self.student_list = [student]			def student_removal(self, student_name):		self.student_list.remove(student_name)### HELPER FUNCTIONS ###
def object_caller(name, target_list):
    for object in target_list:
        if object.name == name:
            return True, object
    return False, object			