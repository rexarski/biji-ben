# Part 1: Math Functions

## Contents:

*   [Python is Interpreted](#python-is-interpreted)
*   [Whitespace](#whitespace)
*   [Modules](#modules)
*   [The print function](#the-print-function)
*   [Comments](#comments)
*   [Expressions, Values, Types, and Assignment](#expressions-values-types-and-assignment)
*   [Functions](#functions)
*   [**Exercise 1: Math Functions — 10 Marks**](#exercise-1-math-functions-10-marks)

## Python is Interpreted

A Python interpreter reads and executes Python scripts. Python interpreters can be operated in two ways:

1.  As an interactive interpreter — In Linux start the interpreter with the command:

    ```
    python3
    ```

2.  By reading Python scripts — In Linux, the Python script (file) `hello_world.py`, which is included with this assignment, can be executed with the command:

    ```
    python3 hello_world.py
    ```

Throughout this exercise it is recommended that you use the interactive interpreter to try out new concepts.

In the interactive interpreter information about any type can be obtained with the `help` function. For example, `help(int)` will return information about the type `int`, which stores integer numbers.

You can exit the interactive interpreter with `ctrl-d`. **Windows**: In Windows systems you will need to key in the combination `ctrl-z` _and then_ press Return.

Write your script files the editor of your choice. We recommend using [Atom](https://atom.io/), a modern, cross-platform editor with good Python support. Make sure you set auto-indentation to use spaces.

## Whitespace is Important

Before you get into anything too complicated it is important to realise that in Python, **whitespace matters**.

White space — in contrast with `C++` or `Java` that use brackets — is used to delineate blocks of code inside classes, functions, conditionals, loops, exceptions, and a number of other constructs.

For instance here are implementations of this function in both C and Python.

`foo` function in [C](http://en.wikipedia.org/wiki/C_(programming_language) "C (programming language)") with [K&R indent style](http://en.wikipedia.org/wiki/1_true_brace_style "1 true brace style"):

```c
void foo(int x)
{
    if (x == 0) {
        bar();
        baz();
    } else {
        qux(x);
        foo(x - 1);
    }
}
```

`foo` function in Python 3.x:

```python
def foo(x):
    if x == 0:
        bar()
        baz()
    else:
        qux(x)
        foo(x - 1)
```

As a general rule, all code within a block must be at the same indentation level. Python is picky about this, so expect to get a syntax errors complaining about indentation as you do this tutorial.

To avoid issues, do not use tabs as whitespace.

**NEW on Python 3:** Python 3 introduces stronger type-checking via the `typing` module. Though, if your project requires stronger typing mechanisms, it is perhaps better to use a different programming language.

If a line runs too long it can be broken by terminating it with a backslash. For readability, the trailing code should be indented further than the base line:

```python
if name in list_of_names[index] and \
    age < 50:
        print(...)
```

## Modules

Python comes with a lot of useful built in modules (the Pythonic way of saying "library"). You can find a list of these [here](http://docs.python.org/3/library/).

Modules can be imported with the `import` statement.

For example, we can import the `math` module with the following statement:

```python
import math
```

To see what functions and attributes it contains use the `help` function after you import `math`.

```python
help(math)
```

To access the functions and attributes of a module, use a full stop.

```python
>>> math.sqrt(64)
8.0
```

We can import attributes and functions from modules directly by using the `from` keyword.

```python
>>> from math import sqrt, factorial
>>> factorial(sqrt(64))
40320
```

We can rename things when we import them.

```python
>>> from math import sqrt as sq
>>> sq(64)
8.0
```

It is possible, though generally ill-advised, to import everything in a module.

```python
from math import *
```

The import statement will be scoped according to where it is used. If it is used at the top of a file, then everything in the file will have access to whatever is imported. If it is used within a function (or any kind of block), then only subsequent lines in that function (block) can use the module.

There is a module called `this`. For a bit of fun and some advice about Python, try importing it.

## The print function

In Python 3, the easiest way to write to the screen is the `print` _built-in function_.

```python
>>> print("Hello World!")
Hello World!
```

The `print` function can take as an argument a string object or an expression whose result is a string object

```python
>>> print("The circumference of a unit circle is: " + str(2 * 3.14159))
The circumference of a unit circle is: 6.28318
```

By using the built-in function `str()` we are explicitly converting the result of the multiplication into a string object, which can be concatenated with another string via the operator `+`.

The method above is not very convenient when we need to generate strings dynamically. The `format()` method of string objects allows us to achieve the same we did with the previous command

```python
>>> print("The circumference of a unit circle is: {}".format(2 * 3.14159))
The circumference of a unit circle is: 6.28318
```

where the empty curly braces `{}` are substituted by the first argument of the `format` method. When we have several pieces of data to be inserted in a string, the i-th pair of curly braces in the string will be substituted by the i-th argument of `format()`

```python
>>> print("My birthday is: {}/{}/{}".format(13, 6, 1970))
My birthday is: 13/6/1970
```

this can be overridden by specifying the index of the argument of `format()` we want each pair of curly brackets to be substituted by

```python
>>> print("In the United States, my birthday is: {1}/{0}/{2} ".format(13, 6, 1970))
In the United States, my birthday is: 6/13/1970
```

## Comments

As a general rule — and as a requirement for this assignment — you should comment your code.

In Python, single line comments start with a hash.

```python
# This line is a comment, it will not be executed
```

Multiple line comments are contained between triple quotes. They are treated like a statement that does nothing and must be indented to the level of the block they occur in.

```python
""" This is a multiple line comment.
    Python will read it, but ignore it.
"""
```

## Expressions, Values, Types, and Assignment

In Python, expressions return values.

Values — like just about everything else — are objects.

They have a type which can be determined with the `type` function.

```
>>> type(5)
<class 'int'>
>>> type(1.0/2.0)
<class 'float'>
>>> type("Hello")
<class 'str'>
```

Check the types of some other expressions to familiarise yourself with this.

As we saw while discussing the `print()` function, objects have methods and attributes which can be accessed with a period. For example, we can make a new lower case version of a string as follows:

```python
>>> "HELLO".lower()
'hello'
```

You can use the `help` function or documentation to find out more useful methods of the built in types.

We can build expressions using all of the operators you might expect. A list of operators in Python can be found [here](http://www.tutorialspoint.com/python/python_basic_operators.htm).

In Python `=` is the assignment operator. It stores a value in memory and points a variable name at it.

Because Python is dynamically typed, we do not have to specify the type of a variable. A variable can store any value at any time, regardless of type.

```
>>> name = "Ludwig"
>>> type(name)
<class 'str'>
>>> name = 3/2
>>> type(name)
<class 'float'>
```

The names of types - `int`, `float`, `str`, etc. can be used as functions to convert values between types. We saw an example of this converting floating point numbers into strings, and you should experiment with this to see if it behaves as expected when converting strings into numbers.

`None` is a special value which is usually used to denote no value. We will explore this more later.

A Python script can be made interactive by getting input from the user with the `input` function. Try the following in a script file:

```python
print("Enter your name:")
name = input()
print("Hello {}".format(name))
```

## Functions

Like all respectable programming languages, in Python it is possible to define new functions.

```python
def square(val):
    return val * val
```

The code inside a function occupies a single indented block. Of course, this block can contain its own sub-blocks in conditionals, or loops, or even other functions.

Notice that we do not specify the types of our arguments or the type of our return value. These are determined at run time. A function which returns no value returns `None` by default.

Here is an even better function:

```python
def square(val):
    """ Return the square of the input val.

        (number) -> number
    """
    return val * val
```

The comment at the top of the function is called a docstring. Classes, functions, methods, and modules all should have docstrings. They are what is displayed when the `help` function is used.

Docstrings for functions should include a typestring to indicate the intended types of the arguments and the return value. In a typestring, use types that are the most general your function will accept. If the function `square` only accepted integer numbers, then the typestring would be `(int) -> int`.

Many Python objects are immutable, which means we cannot change them. This includes `int`, `float`, and `str`. We will explore this more in a future section of this tutorial, but for now assume that when you pass a value into a function and change this variable within the function, the original value will remain unchanged.

```python
>>> def square(val):
        val *= val
>>> x = 2
>>> square(x)
>>> x
2
```

Remember that in Python, everything is an object. Mutable objects passed as arguments to a function are _passed by reference_, while immutable objects are _passed by value_.

Functions are considered _immutable_ objects.

Since we can point variables at any object, including functions, it is possible to pass functions as arguments to other functions. If we have the following functions defined:

```python
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def apply(func, x, y):
    return func(x, y)
```

Then we can do the following:

```python
>>> apply(add, 5, 6)
11
>>> apply(sub, 5, 6)
-1
```

Familiarise yourself with this concept. We will use it later for Exercise 2.

When deciding the scope of variables in functions, Python always prefers local variables, if they exist.

When assigning to a variable in a function, Python always creates a local variable, even if there is an existing global variable with the same name.

**TIP**: When you eventually write your own modules to put together functions and classes, and import them in the interactive interpreter, you will need to restart the interpreter and re-import the module if it changes. This means that it is probably easier to write script files to test your own modules, rather than using the interactive interpreter.

## Exercise 1: Math Functions — 10 Marks

For this exercise we want you to experiment with assignment statements and expressions using the built in `math` module.

Try importing the `math` module and use the help function to see what it contains.

Edit the file `math_functions.py` so that it does the following when run:

*   Create a module variable called `ln_e`, whose value is the _natural_ logarithm of `e` (Don't hard code any numbers. Instead use the values and functions from the `math` module.);
*   Create a module variable called `twenty_radians` and assign it whatever value a 20 degree angle would be in radians;
*   Create two functions called `quotient_ceil` and `quotient_floor`, each of which takes two arguments, a numerator and a denominator, in that order. The first of these functions returns the ceiling of the result of the division (numerator divided by the denominator), and the second returns the floor. Note that here we are expecting floating point division to be performed, regardless of the types of the input arguments. We also expect an integer to be returned.
*   Create a function called `manhattan`, which takes four arguments, `x1`, `y1`, `x2`, and `y2` and returns the Manhattan distance between the two points specified by these arguments.

**Remember** to submit the file `math_functions.py`.

Our automarking programs will import `math_functions.py`, and check that these variables variables exist and have the correct values. **Your file should not print anything when imported.**

Don't forget to edit the comment header at the top of the file and to add docstrings for all functions.

Now you can either go back to the [index](README.md) or move to the
[next exercise](2_truth_tables.md).
