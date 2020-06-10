package university;

public class Main {

    public static void main(String[] args) {

        //demoAliasing();
        demoInheritance();
    }

    /** Demonstrates some aspects of aliasing. */
    public static void demoAliasing() {
        
        // See the memory model diagram PDF file.

        // We begin BEFORE adding the ".clone()" to the constructor
        // and setter of Person.
        String[] jenName = {"Jen", "C"};
        Person jen = new Person(jenName, "21012000", "F");
        System.out.println(jen);

        // So far so good. Let's change the value of the first element
        // in the Array jenName.
        jenName[0] = "Bob";       // Exercise 1.
        System.out.println(jen);

        // Why did the change in jenName have an effect on the Person
        // object jen? Aliasing!
        
        // Now we fix the problem by using a copy of the Person's
        // name instead of a reference to it (in constructor/setter).
        // Exercise 2

        // The output changes -- we no longer see the change in jen! 
        // But did we fix the problem?  Let's try this:
        String [] someName = jen.getName();
        someName[1] = "Bob";      // Exercise 3
        System.out.println(jen);
        
        // OK, now what happened? Look at the second Java memory diagram.
        // Now we add ".clone()" to the getter name.

        // Finally fixed!  Exercise 4
    }

    public static void demoInheritance() {

        // ==== Method overriding. ====
        
        String [] jenName = {"Jen", "C"};
        Person jen = new Person(jenName, "21012000", "F");

        // Runs toString() from class Person.
        System.out.println(jen);

        String [] bobsName = {"Bob", "B", "Bobson"};
        Student bob = new Student(bobsName, "12121992", "M", "1234567890");

        // OK, so which toString() is executed here?
        // Before we defined toString() in class Student, this ran
        // the toString() defined in class Person. Once we implemented
        // toString() in Student, this runs the toString() defined in
        // Student. There is now no way to run Person's toString() on
        // an object of type Student. We say that toString() in Student
        // "overrides" toString() in Person.
        System.out.println(bob);
        
        // ========  Shadowing, casting, and  overriding ========
        
        // We added a String instance variable named example to 
        // the Person class and to the Student class.
        
        //  Two instance variables with the same type and name:
        System.out.println(jen.example); // example from Person
        System.out.println(bob.example); // example from Student
        
        // This prints the example variable from class Person.
        System.out.println(((Person) bob).example); // example from Person

        // But the following calls toString() from Student!
        // This is what method overriding is all about!
        System.out.println(((Person) bob).toString());
        
        // We'll do more on this next time.
    }
}
