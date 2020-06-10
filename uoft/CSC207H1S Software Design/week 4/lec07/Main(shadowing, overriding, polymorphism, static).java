package university;


public class Main {

    public static void main(String[] args) {
        //demoInheritance2();
        demoStatic();
    }    

    public static void demoInheritance2(){    

        // ========  Overriding, shadowing, and casting  ========

        String [] jenName = {"Jen", "C"};
        Person jen = new Person(jenName, "21012000", "F");
        String [] bobsName = {"Bob", "B", "Bobson"};
        Student bob = new Student(bobsName, "12121992", "M", "1234567890");

        // Person "is a" Student. Person "is a" Object too.
        if (bob instanceof Student) {
            System.out.println("bob is a Student.");
        }
        if (bob instanceof Person) {
            System.out.println("bob is a Person.");
        }
        if (bob instanceof Object) {
            System.out.println("bob is a Object.");
        }

        // Person jen is not a Student.
        if (jen instanceof Student) {  // this is false, so nothing is printed
            System.out.println("jen is a Student.");
        }
        if (jen instanceof Person) {  
            System.out.println("jen is a Person.");
        }
        if (jen instanceof Object) {
            System.out.println("jen is a Object.");
        }

        // Shadowing: avoid doing this!
        // Child and parent classes have two instance variables with the same type and name:
        System.out.println(bob.example); // example from Student
        System.out.println(((Person) bob).example); // example from Person


        // When treating bob as a Person, can only call methods Person knows about.
        System.out.println(((Person) bob).getName());

        // The following can't be done; no getStudentNum() method in Person
        //System.out.println(((Person) bob).getStudentNum());  // compile error

        // But the following calls toString() from Student!
        // This is what method overriding is all about!
        System.out.println(((Person) bob).toString());


        // Polymorphism: one object having multiple forms.
        
        String [] charliesName = {"Charlie", "C"};
        Student charlie = new Student(charliesName, "31311331", "M", "9876");

        Person [] people = new Person [3];
        people[0] = jen;
        people[1] = bob;
        people[2] = charlie;

        System.out.println("The people are: ");
        for (Person person: people) {
            System.out.println(person); // polymorphism!
        }
    }

    /** Demonstrates the use of "static" modifier in Java. */
    public static void demoStatic() {
        
        // Can access the static variable before any Student instances exist.
        System.out.println("Count is " + Student.getStudentCount());
        
        String [] bobsName = {"Bob", "B", "Bobson"};
        Student bob = new Student(bobsName, "12121992", "M", "1234567890");

        // We need to use a static method to access the static variable.
        System.out.println("Count is " + Student.getStudentCount());

        String [] charliesName = {"Charlie", "C", "Charleson"};
        Student charlie = new Student(charliesName, "31311331", "M", "0987654321");

        System.out.println("Count is " + Student.getStudentCount());
    }
}
