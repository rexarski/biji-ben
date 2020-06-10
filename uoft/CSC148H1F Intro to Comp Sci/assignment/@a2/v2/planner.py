# Assignment 2 - Course Planning!
# Su Young Lee, leesu9

#
# CSC148 Fall 2014, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
# STUDENT INFORMATION
#
# List your group members below, one per line, in format
# Su Young Lee, leesu9
# Rui Qiu, qiurui2
# 
# ---------------------------------------------
"""Program for helping users plan schedules.

This module contains the main class that is used to interact with users
who are trying to plan their schedules. It requires the course module
to store prerequisite information.

TermPlanner: answers queries about schedules based on prerequisite tree.
"""
from course import *


# General helper function
def class_name_finder(target_name, target_list):
    """ (str, list) -> (Boolean, Course)
    Return (True, object) if target name in list,
    return (False, None) if not.
    """
    for course in target_list:
        if target_name == course.name:
            return (True, course)

    return (False, None)

def root_finder(course_list):
    ''' (lst of Course) -> Course

    Return the root in list of courses.
    '''
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
        """ (TermPlanner, Course) -> NoneType
        
        This will reset all taken courses to not taken.
        """
        target_tree.taken = False
        for prereq in target_tree.prereqs:
            self.course_reset(prereq)
    
    def is_course_valid(self, course_exists, course):
        """ (TermPlanner, Boolean, Course) -> Boolean
        
        Return whether a certain course is valid to take.
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
        """ (TermPlanner, list of lists) -> Boolean
        
        Return whether the schedule is empty.
        """
        if schedule == [[]]:
            return True
        else:
            return False
        
    def is_term_valid(self, term):
        """ (TermPlanner, list) -> Boolean
        
        Return whether a certain term is valid.
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

                takeable_course.take()
            except UntakeableError:
                print ("This shouldn't happen")
                pass

        return True

    def is_valid(self, schedule):
        """ (TermPlanner, list of (list of str)) -> bool

        Return True if schedule is a valid schedule.
        Note that you are *NOT* required to specify why a schedule is invalid,
        though this is an interesting exercise!
        """
        # [ [term1 courses] [term2 courses] .... [termN courses] ]

        # Currently this program assumes each term has max 5 courses already
        if self.course == []:
            return self.is_valid_empty(schedule)

        for term in schedule:
            if len(term) > 5:
                return False

            if not self.is_term_valid(term):
                return False

        self.course_reset(self.course)
        return True

    def generate_schedule(self, desired_courses):
        """ (TermPlanner, list of str) -> list of (list of str)

        Return a schedule containing the courses in selected_courses that
        satisfies the restrictions given in the assignment specification.
        """
        total_list = []

        # desired_courses = self.generate_schedule_helper(desired_courses)

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

            # This will repeat until all courses are taken of course!

        # Basically just take all leaves (courses with prereqs all taken / no prereqs at all)
        # And stuff them into a term.  Repeat.

        # Before total_list is returned, course tree needs to be reset.
        
        self.course_reset(self.course)

        return total_list

    def leaf_finder(self, target_course, specific_list):
        """ (TermPlanner, Course, list of str) -> list of Course
        Return a schedule containing the courses in selected_courses that
        satisfies the restrictions given in the assignment specification.
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
                #It's a leaf, but not a course we're looking for so.
                # It's taken so that the course is not checked later
                target_course.take()
                return leaf_list

        for prereq_course in target_course.prereqs:
            leaf_list += self.leaf_finder(prereq_course, specific_list)

        if len(leaf_list) > 5:
            leaf_list = leaf_list[:5]

        return leaf_list

    # if generate_schedule does not contain all needed courses, then just use this function
    # To make the original one work!
    
    def generate_schedule_helper(self, desired_list_name):
        """ (TermPlanner, list of str) -> list of str
        Return list of course names, with the addition of all of their needed pre-requisites
        """
        desired_list = self.course_name_converter(desired_list_name)
        new_list = []

        for course in desired_list:
            prereq_name_list = course.missing_prereqs()

            prereq_list = self.course_name_converter(prereq_name_list)

            for prereq_course in prereq_list:
                # This prevents redundancy
                prereq_course.taken = True
                if prereq_course.name not in desired_list:
                    new_list.append(prereq_course.name)

        new_list += desired_list_name

        # Make schedule back to normal as well
        self.course_reset(self.course)
        return (new_list)

    def course_name_converter(self, name_list):
        """ (TermPlanner, list of str) -> list of Course
        
        Return list of Courses with the names in name_list
        """
        course_list = []
        for course_name in name_list:
            exists, course = self.course_finder(course_name, self.course)
            if not exists:
                print ('Should always exist...')
                pass
            course_list.append(course)

        return course_list