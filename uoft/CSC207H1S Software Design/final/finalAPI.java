// Short Java APIs:

class Throwable:
	// the superclass of all Erros and Exceptions
	Throwable getCause()	// returns the Throwable that caused this Throwable to get thrown
	String getMessage()	// returns the detail message of this Throwable
	StackTraceElement[] getStackTrace()	// returns the stack trace info

class Excetpion extends Throwable:
	Excetpion()	// constructs a new Exception with detail message null
	Exception(String m)	// constructs a new Exception with detail message m
	Exception(String m, Throwable c)	// constructs a new Exception with detail message m caused by c

class RunTimeException extends Exception:
	// The superclass of exceptions that don't have to be declared to be thrown

class Error extends Throwable
	// something really bad

class Object:
	String toString()	// returns a String representation
	boolean equals(Object o)	// returns true iff "this is o"

interface Comparable<T>:
	int compareTo (T o)	// returns < 0 if this < o, = 0 if this is o, > 0 if this > o

interface Iterable<T>:
	// An iterator over a collection.
	boolean hasNext()	// returns true iff the iteration has more elements
	T next()	// returns the next element in the iteration
	void remove()	// remove from the underlying collection the last element returned or 
			// throws UnsupportedOperationException
interface Collection<E> extends Iterable<E>:
	boolean add(E e)	// adds e to the Collection
	void clear()	// removes all the items in this Collection
	boolean contains(Object o)	// returns true iff this Collection contains o
	boolean isEmpty()	// returns true iff this Collection is empty
	Iterator<E> iterator()	// returns an Iterator of the items in this Collection
	boolean remove(E e)	// removes e from this Collection
	int size()	// returns the number of items in this Collection
	Object[] to Array()	// returns an array containing all of the elements in this collection

interface List<E> extends Collection<E>, Iterable<E>:
	// An ordered Collection. Allows duplicate items.
	boolean add(E elem)	// appends elem to the end
	void add(int i, E elem)	//inserts elem at index i
	boolean contains(Object o)	// returns true iff this List contains o
	E get(int i)	// returns the item at index i
	int indexOf(Object o)	// returns the index of the first occurrence of o, or -1 if not in List
	boolean isEmpty()	// returns true iff this List contains no elements
	E remove(int i)	// removes the item at index i
	int size()	// returns the number of elements in this List

class ArrayList<E> implements List<E>

class Arrays
	static List<T> asList(T a, ...)	// returns a List containing the given arguments

interface Map<K, V>:
	// An object that maps keys to values.
	boolean containsKey(Object k)	// returns true iff this Map has k as a key
	boolean containsValue(Object v)	// returns true iff this Map has v as a value
	V get(Object k)	// returns the value associated with k, or null if k is not a key
	boolean isEmpty()	// returns true iff this Map is empty
	Set<K> keySet()	// returns the Set of keys of this Map
	V put(K k, V v)	//adds the mapping k -> v to this Map
	V remove(Object k)	// removes the key/value pair for key k from this Map
	int size()	// returns the number of key/value pairs in this Map
	Collection<V> values()	// returns a Collection of the values in this Map

class HashMap<K, V> implements Map<K, V>

class File:
	File(String pathname)	// constructs a new File for the given pathname

class Scanner:
	Scanner(File file)	// constructs a new Scanner that scans from file
	void close()	// closes this Scanner
	boolean hasNext()	// returns true iff this Scanner has another token in its input
	boolean hasNextInt()	// returns true iff the next token in the input can be interpreted as an int
	boolean hasNextLine()	// returns true iff this Scanner has another line in its input
	String next()	// returns the next complete token and advances the Scanner
	String nextLine()	// returns the next line and advances the Scanner
	int nextInt()	// returns the next int and advances the Scanner

class Integer implements Comparable<Integer>:
	static int parseInt(String a)	// returns the int contained in s
		throw a NumberFormatException if that isn't possible
	Integer(int v)	// constructs on Integer that wraps v
	Integer(String s)	// constructs an Integer that wraps s
	int compareTo(Object o)	// returns <0 if this < o, = 0 if this == o, > 0 otherwise
	int intValue()	// returns the int value

class String implements Comparable<String>:
	char charAt(int i)	// returns the char at index i.
	int compareTo(Object o)	// returns < 0 if this < o, = 0 if this == o, > 0 otherwise
	int compareToIgnoreCase(String s)	// returns the same as compareTo, but ignores case
	boolean endsWith(String s)	// returns true iff this String ends with s
	boolean startsWith(String s)	// returns true iff this String begins with s
	boolean equals(String s)	// returns true iff this String contains the same chars as s
	int indexOf(String s)	// returns the index of s in this String, or -1 if s is not a substring
	int indexOf(char c)	// returns the index of c in this String, or -1 if c does not occur
	String substring(int b)	// returns a substring of this String: s[b .. ]
	String substring(int b, int e)	// returns a substring of this String: s[b .. e)
	String toLowerCase()	// returns a lowercase version of this String
	String toUpperCase()	// returns an uppercase version of this String
	String trim()	// returns a version of this String with whitespace removed at the beginning and the end

class System:
	static PrintStream out	// standard output stream
	static PrintStream err	// error output stream
	static InputStream in 	// standard input stream

class PrintStream:
	print(Object o)	// prints o without a newline
	println(Object o)	// prints o followed by a newline

class Pattern:
	static boolean matches(String regex, CharSequence input)	// compiles regex and returns true iff input matches it
	static Pattern compile(String regex)	// compiles regex into a pattern
	Matcher matcher(CharSequence input)	// creates a matcher that will match input against this pattern

class Matcher:
	boolean find()	// returns true iff there is another subsequence of the input sequence that matches the pattern.
	String group()	// returns the input subsequence matched by the previous match
	String group(int group)	// returns the input subsequnce captured by the given group during the previous match operation
	boolean matches()	// attempts to match the entire region against the pattern.

class Observable:
	void addObserver(Observer o)	// adds o to the set of observers if it isn't already there
	void clearChanged()	// indicates that this object has no longer changed
	boolean hasChanged()	// returns true iff this object has changed
	void notifyObservers(Object arg)	// if this object has changed, as indicated by the hasChanged method, then notifies all of its obervers by calling update(arg) and then calls the clearChanged method to indicate that this object has no longer changed
	void setChanged()	// makes this object as having been changed

interface Observer:
	void update(Observable o, Object arg)	// called by Observable's notifyObservers;
		// o is the Observable and arg is any information that o wants to pass along


// Regular expressions:
// Here are some predefined character classes
	Any character
\d 	A digit: [0-9]
\D 	A non-digit: [^0-9]
\s 	A whitespace character: [ \t\n\x0B\f\r]
\S 	A non-whitespace character: [^\s]
\w 	A word character: [a-zA-Z_0-9]
\W 	A non-word character: [^\w]
\b 	A word boundary: any change from \w to \W or \W to \w

// Here are some quantifiers:
Quantifiers 	Meaning
X?		X, once or not at all
X*		X, zero or more times
X+		X, one or more times
X{n}		X, exactly n times
X{n,}		X, at least n times
X{n, m}		X, at least n; not more than m times
