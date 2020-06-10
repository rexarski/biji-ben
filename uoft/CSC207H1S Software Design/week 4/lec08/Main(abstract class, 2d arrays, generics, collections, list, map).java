package university;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Main {

    public static void main(String[] args) {
        //demo2DArray();
        //demoAbstract();
        demoCollections();
    }    
    
    /** Demonstrates declaration and initialization of 2D arrays. */
    public static void demo2DArray() {

        // A 3 x 4 array.
        int[][] table = new int[3][4];
        System.out.println(table[1][2]);

        // An array with 3 rows and columns of length 4, 2, and 3, 
        // respectively.
        // When column length varies, sometimes called "jagged" or
        // "ragged" array.
        int[][] jagged = new int[3][];
        jagged[0] = new int[4];
        jagged[1] = new int[2];
        jagged[2] = new int[3];        

        for (int r = 0; r < jagged.length; r++) {
            System.out.println(jagged[r].length);
        }
    }
    
    /** Demonstrates more overriding and polymorphism. */    
    public static void demoAbstract() {

        // Cannot instantiate an abstract class:
        //Grade g = new Grade();             // compile error

        LetterGrade lgA = new LetterGrade("A");
        LetterGrade lgB = new LetterGrade("B");
        NumericGrade ng100 = new NumericGrade(100);
        NumericGrade ng42 = new NumericGrade(42);

        // Grade declared an abstract method: double gpa()
        // Subclasses of grade must implement the gpa() method.
        System.out.println(lgA.gpa());
        System.out.println(lgB.gpa());
        System.out.println(ng100.gpa());
        System.out.println(ng42.gpa());

        // More polymorphism.
        Grade myGrade = lgA;
        System.out.println(myGrade);
        
        Grade[] grades = {lgA, lgB, ng100, ng42};

        for (Grade g : grades) {
            System.out.println(g);    // more overriding of toString()
        }
    }
    public static void demoCollections() {

        // Java Collections: Map, List, Set, Queue, etc
        // These are all interfaces.

        // == List ==
        // Java's List is very similar to Python's lists.
        // Declare and initialize an ArrayList of Strings.
        // Lists are generic, so we provide the type of the
        // elements.
        List<String> csc207team = new ArrayList<String>();

        // Add elements to the list.
        csc207team.add("jen");
        csc207team.add("alex");
        csc207team.add("daniyal");
        csc207team.add("gary");
        System.out.println(csc207team);
        
        // This isn't permitted, because we specified type String.
        //csc207team.add(new Integer(45));
        
        // The compiler know that get() will return a String in this
        // case, so we don't need to type cast.
        csc207team.get(0).charAt(0);   // calling String method charAt
        
        // A couple more List methods:
        System.out.println(csc207team.size());    
        System.out.println(csc207team.contains("alex"));
        
        // List has many more methods: check the documentation!
                
        // == Generics must use object types ==
        
        // Can have an ArrayList of any valid (built-in or user-
        // defined) Java object type (i.e. no primitives!)
        // List<int> primitiveIntList = new ArrayList<int>(); // compile error
        List<Integer> intList = new ArrayList<Integer>();
        
        // But we can make use of autoboxing of primitive types:
        intList.add(12); // creates an Integer object, adds it to ArrayList
        System.out.println(intList);
        
        // Automatically unboxes as well:
        int x = intList.get(0);
        System.out.println(x);
        
        // == Map ==

        // Map interface (similar to Python's dictionary type)
        // Collection of unordeded (key, value) pairs.
        Map<String, Integer> myMap = new HashMap<String, Integer>();

        myMap.put("csc", new Integer(207));  // Python: my_map["csc"] = 207;
        System.out.println(myMap.get("csc")); // Python: my_map["csc"]

        // "mat" is not a key, so this returns null.
        System.out.println(myMap.get("mat")); 
    }
}
