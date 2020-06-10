#A closer look at the ‘Hello World!’ Application
January 18, 2015

`class HelloWorldApp {`
	`public static void main(String[] args) {`
		`System.out.println("Hello World!"); // Display the string.`
	`}`
`}`

consists of three primary components:

##Source Code Comments

`/**`
` * The HelloWorlApp class implements an application that`
` * simply prints "Hello World!" to standard output.`
` */`
`class HelloWorldApp {`
	`public static void main(String[] args) {`
		`System.out.println("Hello World!"); // Display the string.`
	`}`
`}`

comments are ignored by complier but useful to programmers

Java supports 3 kinds of comments:

`/* text */`
`/** documentation */`
`// text`


##The HelloWorldApp Class Definition
The most basic form of a class definition is:
`class name {`
	…
`}`

`class` is the beginning for a class named `name`

##The main Method
the code `public static void main(String[] args) {` begins the definition of the main method

every application must contain a `main` method whose signature is:
`public static void main(String[] args)`

- the modifiers `public` and `static` can be written in either order `public static` or `static public`
- you can name the argument anything, conventionally, it’s `args` or `argv`