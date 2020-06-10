package university;

public class Main {

    public static void main(String[] args) {
        
        // Before we added our own constructor, Java provided a default
        // constructor that takes no arguments.  Once we declared our
        // own constructor, the default one is no longer available.
        //Person jen = new Person();
        
        String[] name = new String[] {"Jen", "C"};
        Person jen = new Person(name, "21012000", "F");

        // Person's dob instance varialbe is private, so it cannot be
        // accessed outside of the Person class.
        //System.out.println(jen.dob);

        // Instead, we create a public "getter" method to get the dob
        // instance variable's value.
        System.out.println(jen.getDob());

        // This involves calling jen.toString().
        // Person originally inherited that method from Object (its parent) 
        // and this printed the memory address.
        // We then defined toString in the Person class (overriding the 
        // toString method from Object) and the method
        // from Person is nowcalled instead.
        System.out.println(jen); 
    }
}
