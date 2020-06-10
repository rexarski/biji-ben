#lec02 notes

- **object** in a program is a structured collection of data, bundled together with some functions that can operate on this data.
- a **class** is a type of object, which allows us to create many objects with the same properties without redundant code.
- each piece of data associated with a class is an **attribute**.
	- a class can have many attributes
	- attributes can be different types
- the operations associated with classes are called the **methods** of the class.
- classes are used to *organize functions and data into logical blocks based on their purpose and relationships with each other.*
- When we create a new class, we need to use double underscore init double underscore, which is a special Python **constructor method** to create new objects of this class.
- the **self** parameter refers to the current object for which the method is being called.
- there is no concept of 'private' attributes; we can both access and change all attributes outside of the class at will.
	- *Principle of **information hiding***: when designing a class, we want to make a clear distinction between public interface (the features of the class that other code outside the class may use), and the *private implementation* (i.e., how we've written the methods and attributes of the class.)
- class method:
	- 