# Assignment 2 - Course Planning!
# Su Young Lee, leesu9
#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# Su Young, leesu9
# Rui Qiu, qiurui2
# ---------------------------------------------
"""Program for helping users plan schedules.

This module contains the main class that is used to interact with users
who are trying to plan their schedules. It requires the course module
to store prerequisite information.

TermPlanner: answers queries about schedules based on prerequisite tree.
"""
from course import *


# General helper function
# Return True/False if target name in list, and target object.
def class_name_finder(target_name, target_list):
    """ (str, list of Course) -> (bool, Course)
    Return (True, Course) if target_list has a course with target_name
    Return (False, None) if not.
    """
    for course in target_list:
        if target_name == course.name:
            return (True, course)

    return (False, None)

def root_finder(course_list):
    """ (lst of Course) -> Course

    Return the root in list of courses.
    """
    removal_list = []
    if len(course_list) == 1:
        return course_list[0]
    
    # Find every course that's a prerequisite, and add
    # to the list, to slate for removal.
    for course in course_list:
        for prereq_course in course.prereqs:
            removal_list.append(prereq_course)

    for course in removal_list:
        try:
            course_list.remove(course)
        except ValueError:
            pass

    return course_list

def parse_course_data(filename):
    """ (str) -> Course

    Read in prerequisite data from the file called filename,
    create the Course data structures for the data,
    and then return the root (top-most) course.

    See assignment handout for details.
    """
    clist = []

    with open(filename, 'r') as my_file:
        for line in my_file:
            split_name_list = line.split()
            prereq_name, newcourse_name = split_name_list[0], split_name_list[1]
            # Now add them together!
            course_adder(prereq_name, newcourse_name, clist)
    
    # If for some reason multiple roots, just pick the first one.
    root = root_finder(clist)[0]

    return root

def course_adder(prereq_name, newc_name, clist):
    """ (str, str, list of Course) -> None
    Add newc_name to course tree, with prereq_name as prerequisite.
    Create course if not pre-existing
    """
    prereq_exists, prereq_c = class_name_finder(prereq_name, clist)
    newc_exists, new_c = class_name_finder(newc_name, clist)

    # If course hasn't been made yet, make it.
    if not prereq_exists:
        prereq_c = Course(prereq_name)
        clist.append(prereq_c)

    if not newc_exists:
        new_c = Course(newc_name)
        clist.append(new_c)

    # Try to add the course then!
    try:
        new_c.add_prereq(prereq_c)
    except PrerequisiteError:
        pass

class TermPlanner:
    """Tool for planning course enrolment over multiple terms.

    Attributes:a
    - course (Course): tree containing all available courses
    """

    def __init__(self, filename):
        """ (TermPlanner, str) -> NoneType

        Create a new term planning tool based on the data in the file
        named filename.

        You may not change this method in any way!
        """
        self.course = parse_course_data(filename)

    # Will find the course.
    def course_finder(self, course_name, target_tree):
        """ (TermPlanner, str, Course) -> (Boolean, Course)
        
        Return (True, Course) if target course tree has a course with that name
        Return (False, None) if no courses have course_name
        """

        # If there isn't even a tree to begin with...
        if target_tree == []:
            return (False, None)

        if target_tree.name == course_name:
            return (True, target_tree)

        for prereq_course in target_tree.prereqs:
            if self.course_finder(course_name, prereq_course)[0]:
                return self.course_finder(course_name, prereq_course)

        return (False, None)

    def course_reset(self, target_tree):
        """ (TermPlanner, Course) -> None

        Reset all course.taken to False
        """
        # This will reset all taken courses to not taken.
        target_tree.taken = False
        for prereq in target_tree.prereqs:
            self.course_reset(prereq)

    def is_course_valid(self, course_exists, course):
        """ (TermPlanner, bool, Course) -> bool

        Return True if course can be taken
        """
        if not course_exists:
            self.course_reset(self.course)
            return False

        # If course was already taken, then this is a duplicate! So False.
        if course.taken:
            self.course_reset(self.course)
            return False

        # Assumes the "co-requisites" aren't allowed.
        if not course.is_takeable():
            self.course_reset(self.course)
            return False

        # If course exists, isn't taken, and is_takeable, return True
        return True

    def is_valid_empty(self, schedule):
        """ (TermPlanner, list of list) -> bool

        Return True if schedule is empty.
        (Only run this function if self.course is also empty)
        """
        for term in schedule:
            if len(term) >= 1: # If there's anything in a term.
                return False

        return True

    def is_term_valid(self, term):
        """ (TermPlanner, list of str) -> bool

        Return True if term is valid
        """
        valid_course_list = []
        for course_name in term:
            course_exists, course = self.course_finder(course_name, self.course)         
            if not self.is_course_valid(course_exists, course):
                return False

            valid_course_list.append(course)

        for takeable_course in valid_course_list:
            try:
                # This catches duplicates in the same term
                if takeable_course.taken:
                    return False
                
                else:
                    takeable_course.take()
            except UntakeableError:
                # print ("This shouldn't happen")
                pass

        return True

    def is_valid(self, schedule):
        """ (TermPlanner, list of (list of str)) -> bool

        Return True if schedule is a valid schedule.
        Note that you are *NOT* required to specify why a schedule is invalid,
        though this is an interesting exercise!
        """
        # [ [term1 courses] [term2 courses] .... [termN courses] ] (is the input)
        if self.course == []:
            return self.is_valid_empty(schedule)

        for term in schedule:
            #if len(term) > 5:
                #return False

            if not self.is_term_valid(term):
                return False
            
        # Only reaches this point if every term was valid (therefore schedule is valid)
        self.course_reset(self.course)
        return True

    def generate_schedule(self, desired_courses):
        """ (TermPlanner, list of str) -> list of (list of str)

        Return a schedule containing the courses in selected_courses that
        satisfies the restrictions given in the assignment specification.
        """
        total_list = []

        # Aka. until the root course is being taken, continue to take courses.
        while not self.course.taken:
            term_courses = []
            leaves = self.leaf_finder(self.course, desired_courses)

            # Aka. there are no more courses to be taken as well!
            if leaves == []:
                break

            for leaf_course in leaves:
                leaf_course.take()
                term_courses.append(leaf_course.name)

            total_list.append(term_courses)

            # This will repeat until all possible courses are taken.

        self.course_reset(self.course)

        # If not all desired courses were not able to be taken, then len(total_list) will be
        # less than len(desired_courses).  So return [] if this happened
        temp_len = 0
        for term in total_list:
            for course in term:
                temp_len += 1

        if temp_len < len(desired_courses):
            return []

        return total_list

    def leaf_finder(self, target_course, specific_list):
        """ (TermPlanner, Course, list of str) -> list of Course
        Return at most five "leaf" courses, i.e courses that can be taken.
        """        

        leaf_list = []

        # If target_course is already taken, no need to check other.
        if target_course.taken:
            return leaf_list

        # If it's a leaf..
        if target_course.is_takeable():
            if target_course.name in specific_list:
                return [target_course]

            else:
                #It's a leaf, but not a course we're looking for so it's ignored
                return leaf_list

        for prereq_course in target_course.prereqs:
            leaf_list += self.leaf_finder(prereq_course, specific_list)

        if len(leaf_list) > 5:
            leaf_list = leaf_list[:5]

        return leaf_list

    def course_name_converter(self, name_list):
        """ (TermPlanner, list of str) -> list of Course

        Return list of Courses with the names in name_list
        """
        course_list = []
        for course_name in name_list:
            exists, course = self.course_finder(course_name, self.course)
            if not exists:
                # print ('Should always exist...')
                pass
            course_list.append(course)

        return course_list