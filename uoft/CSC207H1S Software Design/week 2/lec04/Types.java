package types;

public class Types {
    
    public static void main(String[] args) {
        
        // == Types ==
        // Every variable has a type.
        // There are two categories of types: primitive and class types.
    
        // == Primitive types ==
        // - primitive types are not objects
        // - int, boolean, char, double
        // - byte, short, long, float
        // - names begin with lowercase letters
        
        // Declare an int variable x; assign it value 4.
        int x = 4;
        
        // Can't redeclare a variable.
        //int x = 8; 
        
        // But we can reassign its value.
        x = 8;
        
        // Cannot assign a double to x.
        //x = 4.56;
        
        double y = 4.56;
        y = 8;
        
        boolean b = true;
        b = false;
        
        char c = 'a';
        
        // == Class types. ==
        
        // Declare variable named myInteger.
        // Create a new object of type Integer, which
        // contains among other things the int value 10;
        // assign the reference to the newly created
        // object to variable myInteger.
        Integer myInteger = new Integer(10);
        
        Integer xInteger = new Integer(x);
        System.out.println(myInteger);
        System.out.println(myInteger.toString());
        
        // == String ==
        // Strings are objects.
        // Strings are immutable.
        
        String s = new String("hello");
        String s2 = "bye";
        
        s2 = s + s2;
        System.out.println(s2);
        
        // Indexing
        char letter = s2.charAt(3); // Python: s2[3]
        System.out.println(letter);
        
        // Slicing
        String slice = s2.substring(4);  // Python: s2[4:]
        System.out.println(slice);
        slice = s2.substring(5, 7);     // Python: s2[5:7]
        System.out.println(slice);
        
        // Stripping (remove whitespace from beginning and end of String.)
        String s3 = "    hi   there   ";
        s3 = s3.trim();
        System.out.println(s3);
        
        // Splitting.
        s3 = "before    hi   there   after";
        String[] parts = s3.split("e");
        System.out.println(parts[0]);
        System.out.println(parts[1]);
        System.out.println(parts[2]);
        // Out of bounds:
        //System.out.println(parts[3]); 
        
        
        // == Arrays == 
        // Not like Python lists:
        // - fixed length, which is set when constructing the object
        // - all elements must have the same type
        
        int[] intArray = new int[4];
        System.out.println(intArray[0]);
        
        int myInt;
        myInt = 8;
        System.out.println(myInt);
        
        String[] stringArray = new String[20];
        System.out.println(stringArray[0]);
        stringArray[0] = "hello";
        System.out.println(stringArray[0]);
        
        intArray = new int[] {1, 2, 3};
        System.out.println(intArray[1]);
    }

}
