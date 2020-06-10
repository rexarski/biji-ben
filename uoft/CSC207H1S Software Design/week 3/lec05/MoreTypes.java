 package types;

public class MoreTypes {

    public static void main(String[] args) {

        // Recap: type array

        Double[] numbers = new Double[6];
        numbers[0] = new Double(10);

        int[] integers = new int[] {10, 20, 30};

        // Basic for loop.
        
        // Three parts (similar to while loop):
        // - initialization: int i = 0;
        // - loop condition; i < integers.length
        // - increment: i++
        for (int i = 0; i < integers.length; i++) {
            System.out.println(integers[i]);
        }

        for (int i = 0; i < numbers.length; i++) {
            System.out.println(numbers[i]);
        }

        // Enhanced for loop.
        for (int item : integers) {
            System.out.println(item);
        }
        
        demoAutoboxingBehaviour();
    }

    public static void demoAutoboxing() {

        // The usual way to create an Integer.
        Integer x = new Integer(1);

        // The shortcut:
        Integer y = 2;

        // Equivalent to: Integer y = new Integer(2);
        // This is called autoboxing: automatically
        // putting a primitive type 2 into a "box" --
        // an object of type Integer.

        // This can be done with any primitive type and its wrapper class,
        // not just int/Integer.
        Double dbl = 3.14;
        Boolean b = true;

        Double d1 = new Double(3.14);
        double d2 = d1; // unboxing: automatically "un-boxes" the double

        // Aliasing.
        Double d3 = d1; // d3 and d1 refer to the same Integer object
    }
    
    public static void demoAutoboxingBehaviour() {
        
        // Autoboxing/unboxing can sometimes result in interesting situations.
        Integer i1 = new Integer(7);
        Integer i2 = new Integer(7);
        int i3 = 7;
        
        // This prints false, since i1 and i2 are references for two different
        // Integer objects.
        System.out.println(i1 == i2);
        
        // For these two expressions, Java automatically unboxes the Integers,
        // gets the value 7 in both cases and so the comparison is 42 == 42.
        // These are both true!
        System.out.println(i1 == i3);
        System.out.println(i2 == i3);
        
        // This is suprising!  Generally, if i1 == i3 and i2 == i3, then we
        // would expect i1 == i2.  But that isn't the case here!
        
        // Rather than comparing the memory address, we can compare the int values
        // that the Integer objects are boxing (i.e., compare 7 == 7).
        System.out.println(i1.equals(i2));
    }
}
