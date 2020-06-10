package university;

public class Main {

    public static void main(String[] args) {

        demoEquals();
        //demoCompareTo();
    }

    public static void demoEquals() {
        
        String s1 = new String("example");
        String s2 = new String("example");
        
        // Identity equality
        // Do s1 and s2 refer to the same object?
        // Like Python's operator: is
        System.out.println(s1 == s2);
        
        // Value equality
        // Do s1 and s2 refer to objects that have the same values?
        // Like Pythons operator: ==
        System.out.println(s1.equals(s2));
        
        // For A1, you are asked to write an equals method for Grid<T>.
        // It should return true iff each corresponding cell contains
        // the same Sprite object.
        
    }
    
    public static void demoCompareTo() {
        
        Double d1 = new Double(2.5);
        Double d2 = new Double(4.2);
        Double d3 = new Double(4.2);
        
        // Double's compareTo method:
        // Returns the value 0 if argument is numerically equal to this Double;
        // a value less than 0 if this Double is numerically less than argument;
        // and a value greater than 0 if this Double is numerically greater than the argument.
        
        System.out.println(d1.compareTo(d2)); // -1 
        System.out.println(d2.compareTo(d1)); // 1
        System.out.println(d2.compareTo(d3)); // 0
        
        // Now, Grade's compareTo method.
        NumericGrade n1 = new NumericGrade(55);
        NumericGrade n2 = new NumericGrade(75);
        LetterGrade l1 = new LetterGrade("A");
        LetterGrade l2 = new LetterGrade("B");
        
        // Can compare two NumericGrades.
        System.out.println(n1.compareTo(n2)); // -1
        
        // Can compare two LetterGrades.
        System.out.println(l1.compareTo(l2)); // 1
        
        // Can also compare a LetterGrade and a NumericGrade:
        System.out.println(l1.compareTo(n1)); // 1
        System.out.println(l2.compareTo(n2)); // 0
        
        // And a NumericGrade to a LetterGrade
        System.out.println(n1.compareTo(l2)); // -1
        System.out.println(n2.compareTo(l1)); // -1
        
        // In all cases, the subclass (LetterGrade or NumericGrade) is calling
        // on the compareTo method from Grade.  That method calls on gpa(),
        // which is overridden in LetterGrade and NumericGrade.
        
    }

}
