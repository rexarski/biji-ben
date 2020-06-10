#exceptions

- **exceptions** are raised towards **runtime error**
- so what we look forwarding doing here are:
	- how to create and raise exceptions;
	- how to deal with exceptions gracefully.
- the usual strategy, which is *to return special values indicating an error*, has drawbacks since it might result in a variable silently getting assigned a null value because of an error, only to cause other problems.
- the other strategy, is called *'Look Before You Leap'(LBYL)*: if you know that a function does not work correctly for certain inputs, then before calling the function, check whether the inputs are valid.
	- common in Java, but not in Python.
	- 3 reasons...

> Instead of LBYL, Pythons takes **'It's Easier to Ask Forgiveness Than Permission'(EAFP)**

- simple flip of LBYL (like leap first then you look)

- step1: raising errors to signify a problem
	- definition: **exceptions** are just regular objects that represent an exceptional situation (not necessarily a problem).
	- The runtime errors are built-in exceptions.
	- the creation of our exceptions is actually the creation of another class, which looks differently. with a 'pass' as an ending.
	- and any exception class we define must have the (Exception) 
- step2: dealing with errors so that the program does not crash
	- try-except block:
	- can add **else** and **finally**
	- a more sophisticated form of class
	
	