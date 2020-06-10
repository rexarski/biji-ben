# Part 2: Truth Tables

## Contents:

*   [Boolean Expressions and Conditionals](#boolean-expressions-conditionals)
*   [While Loops](#while-loops)
*   [Immutability, Strings, and Tuples](#immutability-strings-and-tuples)
*   [**Exercise 2: Generating Truth Tables — 20 Marks**](#exercise-2-generating-truth-tables-20-marks)

## Boolean Expressions and Conditionals

Python has two special values `True` and `False` which represent truth and falsehood, respectively.

These are returned by expressions involving Boolean operators.

The following are the most important Boolean operators: `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `is not`, `in`, `not in`, `not`, `and`, `or`.

The meanings of most of these operators should be fairly clear. However, it is worth noting the difference between `==` and `is` (and between `!=` and `is not`).

The equality operator `==` checks if two objects have the same value.

```python
>>> 5 == 5.0
True
>>> 4 != 4
False
```

The `is` operator checks if two objects **are** the same. That is, if they are the same object then they have the same memory location, which can be found using the `id` function if you are interested.

```python
>>> x = [3, 2, 1]
>>> y = x
>>> z = [3, 2, 1]
>>> x == y
True
>>> x is y
True
>>> z == y
True
>>> z is y
False
```

When comparing a value to `None`, you should use `is` and `is not`.

When evaluating Boolean operators, or conditional statements, Python treats certain non-Boolean values as `True` and others as `False`. You can use the `bool` function to test this, but here are some useful ones:

*   `False` — `None`, `0`, an empty string/tuple/list/set/dictionary;
*   `True` — Pretty much everything else.

In Python, we can make conditionals with the keywords `if`, `elif`, and `else`.

To make conditional statements we must make use of indentation. Python does not allow blocks of code to be delineated with brackets and it is considered bad style to wrap conditions in parentheses.

```python
print("Enter your name:")
name = input()
if len(name) > 10:
    print("That is a very long name!")
elif len(name) > 7:
    print("That is a somewhat long name.")
else:
    print("That name is not long at all.")
    if len(name) > 5:
        print("In fact, it is very efficient.")
```

You can have any number of lines in an indented block except zero. Use the `pass` keyword or a `""" Triple quote comment like this """`, as a placeholder for an empty block, if required.

## While Loops

In Python, while loops behave much like while loops in other procedural languages.

```python
x = 0
while x < 5:
    print(x)
    x += 1
```

Like blocks of code inside conditional statements, all code inside a while loop must be at the same indentation level.

`break` and `continue` statements behave as you might expect.

## Immutability, Strings, and Tuples

In Python, variables point to objects. Some of these objects are mutable (can be modified) and other are immutable (cannot be modified).

Immutable object types include `int`, `float`, `str`, and `tuple`.

Mutable object types, which we will cover in the next section, include `list`, `set`, `dict`, and instances of classes.

The assignment operator in Python operates differently than one might expect coming from C++ or Java. Try the following and note the memory addresses returned by the `id` functions.

```python
>>> x = 5
>>> id(x)
10105952
>>> x += 1
>>> id(x)
10105984
```

This immutability extends to some more complex types, which may surprise the uninitiated programmer.

First, lets look at strings, which have the type `str`.

We have already seen some basic string behaviour and we will cover iterating over strings and other sequences in a later section.

In the following example, the method `lower` returns a new `str` `"hello"`. The variable `greeting` still points to the value `"Hello"`.

```python
>>> greeting = "Hello"
>>> greeting.lower()
"hello"
>>> greeting
"Hello"
```

Python uses square brackets to index into sequences. Continuing the previous example:

```python
>>> greeting[0]
"H"
>>> greeting[-1]
"o"
>>> greeting[-2]
"l"
>>> greeting[-10]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: string index out of range
```

Square brackets are also used to 'slice' a string, that is, to extract a specified sub-string. By using a negative number as an index, we can count back from the end of a string.

```python
>>> greeting[0:2]
"He"
>>> greeting[1:-1]
"ell"
```

Either the start or end index can be omitted. When omitted, they default to the start and end of the string, respectively.

```python
>>> greeting[:]
"Hello"
```

Note that none of these operations are modifying the original string (because it is immutable), they are returning new strings.

When slicing, an optional second colon can be supplied to give a third argument which specifies the step.

```python
>>> greeting[::2]
"Hlo"
```

The step can even be negative:

```python
>>> greeting[::-1]
"olleH"
```

When slicing, indices that extend beyond the ends of a string will not cause an error, they simply result in an empty slice being returned.

We can check for the presence of a sub-string in a string using the Boolean `in` and `not in` operators.

```python
>>> "He" in greeting
True
>>> "l" not in greeting
False
```

The `in` and `not in` operators will also work for tuples, lists, sets, and dictionaries.

For strings, tuples, and lists, it has linear time complexity. It is constant time for sets and dictionaries.

`tuple` is another very important immutable type, which allows us to store sequences of arbitrary values.

An empty `tuple` is made as follows:

```python
>>> tup = ()
>>> type(tup)
tuple
```

A `tuple` with one element is made as follows. The trailing comma is not a typo:

```python
tup = ("One",)
```

And multiple elements:

```python
>>> coords = ("Home", -3, 6)
>>> print(coords)
("Home", -3, 6)
```

We can access the elements of tuples just like we can with strings.

```python
>>> print(coords[1])
-3
```

Slicing also works the same.

Because tuples are immutable (and therefore hashable) they are particularly important for storing sequences in sets and as keys in dictionaries.

There are two very useful string methods which transform between any iterable type, such as `str`, `tuple`, `list`, `set`, and `dict`.

First, `split`, which takes a string and given a specified delimiter, will return a `list` of tokens separated by this delimiter. We will cover lists after the next exercise.

```python
>>> "Hello world. What a lovely day.".split(" ")
["Hello", "world.", "What", "a", "lovely" "day."]
```

If no separator string is specified, any white-space character will be used.

Next, we can take a sequence of strings, or just a string, and join its elements with the specified separator.

```python
>>> ", ".join("Hello")
"H, e, l, l, o"
>>> " : ".join(("One", "Two", "Three"))
"One : Two : Three"
```

You will need to convert each element of a sequence to a `str` before joining. The `map` function is one way to do this. List comprehensions, covered at the end of this tutorial, are another way.

```python
>>> x = (1, 2, 3)
>>> tuple(map(str, x))
("1", "2", "3")
```

## Exercise 2: Generating Truth Tables — 20 Marks

Later in this course you will cover Boolean Satisfiability and use it to encode and solve decision problems.

By now you should all be familiar with Boolean expressions and how to evaluate and manipulate them.

In this exercise you will use your knowledge of conditional expressions, while loops, and strings to generate the truth tables for some Boolean expressions.

Say we have a Boolean expression: `(a ∨ b) ∧ (-b ∨ c) ∧ (-c ∨ -a)` over the variables `a`, `b`, and `c`.

We have a truth table which describes how the expression evaluates for given values of `a`, `b`, and `c`:

```
a     b     c     res
-----------------------
False False False False
False False True  False
False True  False False
False True  True  True
True  False False True
True  False True  False
True  True  False False
True  True  True  False
```

Edit the supplied file `truth_tables.py`, and include the following functions.

First, some functions to implement a set of Boolean formulae:

1.  `boolean_fn1(a, b, c)` - which returns the truth value of `(a ∨ b) → (-a ∧ -b)`
2.  `boolean_fn2(a, b, c)` - which returns the truth value of `(a ∧ b) ∨ (-a ∧ -b)`
3.  `boolean_fn3(a, b, c)` - which returns the truth value of `((c → a) ∧ (a ∧ -b)) ∨ (-a ∧ b)`

You will need to simplify these formulae into formulae using only `not`, `and`, and `or`.

Remember `a → b` is equivalent to `-a ∨ b`, which can be written in Python as `not a or b`.

Next, implement the following function in the same file:

```python
def draw_truth_table(boolean_fn):
    """ This function prints a truth table for the given boolean function.
        It is assumed that the supplied function has three arguments.

        ((bool, bool, bool) -> bool) -> None
    """
```

You can then test this function by running `draw_truth_table(boolean_fn1)`, for example. Note that `draw_truth_table` doesn't return the result but only prints it to the screen.

Each function should display the truth table according to the formula using the same format of the example above.

We will import your file `truth_tables.py` and test the functions you have implemented. The file should not produce any output when imported. Our auto-marking code will expect the output to be exactly as specified.

Please avoid the use of the itertools module which is described at the end of this tutorial. We want you to demonstrate your ability to use the basic constructs of Python (and you will appreciate this module so much more when you have done this exercise manually).

As a final hint, remember that when evaluating conditional expressions, Python considers `0` to be `False` and all other integer values to be `True`.

Now you can either go back to the [index](README.md) or move to the
[next exercise](3_automata.md).
