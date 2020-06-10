#Lecture 3 

September 15, 2014

#Week 2 - Exceptions

**Exceptions** are a way to separate error handling from the regular program control flow: if an exceptional situation occurs during a function call, an exception is **raised**, control immediately transfers away from the function call, and no value is returned.

In Python, exceptions are just regular objects that represent an exceptional situation (not necessarily a problem). The runtime errors you explored last week are built-in exceptions, but you can easily define your own depending on the design of your program.

For example, consider the situation of creating a Person class specifying a name and age. We could do this pretty simply as follows:

(see the lec03.py)