package university;

import java.io.Serializable;

/*
 * An abstract class:
 * - cannot be instantiated, but can be subclassed
 * - it can, but is not required to, contain abstract methods
 * 
 * An abstract method is one that is declared without an implementation.
 * 
 * If a class contains an abstract method, then the class must be abstract.
 */

/**
 * A representation of a grade.
 */
public abstract class Grade implements Comparable<Grade>, Serializable{
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1616992908949548331L;
	/*
	 * VALID_GRADES is a constant.  Because VALID_GRADES is "final", 
	 * it cannot be reinitialized.
	 */
	/** Valid letter grades. */
	public static final String[] VALID_GRADES = {"A", "B", "C", "D", "F"};

	/*
	 * This method is abstract. It is a requirement for all subclasses of
	 * Grade to implement a method called gpa that takes no parameters and
	 * returns a double.
	 * Try removing gpa() from one of the subclasses and see what happens.
	 */
	/**
	 * Return the GPA that corresponds to this Grade.
	 * @return the GPA that corresponds to this Grade.
	 */
	public abstract double gpa();

	/*
	 * Another example of a static method.  
	 */
	/**
	 * Return a letter corresponding to the integer grade.
	 * @param grade an integer value of the grade, must be in [0, 100]
	 * @return the letter that corresponds to grade
	 */
	public static String toLetter(int grade) {
	    if (grade < 50) { return "F"; }
	    if (grade < 60) { return "D"; }
	    if (grade < 70) { return "C"; }
	    if (grade < 80) { return "B"; }
	    return "A";
	}
	
	/*
	 *  compareTo returns a negative integer, zero, or a positive integer
	 *  as this object is less than, equal to, or greater than the specified object.
	 *  For Grades, the gpa() return values will be compared.
	 * 
	 * Think carefully about how the code below works!
	 * 
	 * We now have a way to compare ANY Grade to ANY other Grade: 
	 * LetterGrades to LetterGrades, LetterGrades to NumericGrades, 
	 * NumericGrades to whatever new type of Grade we decide to define next!
	 *  
	 * The method compareTo is not abstract. It gets inherited in the 
	 * subclasses of Grade. So if we have, for example (see also main), 
	 * LetterGrade letterGrade = ...
	 * NumericGrade numericGrade = ...
	 * ...letterGrade.compareTo(numericGrade)...
	 * then this.gpa() calls the method gpa() that is defined in LetterGrade, and
	 * other.gpa() calls the method gpa() that is defined in NumericGrade.
	 * 
	 * This is overriding!
	 */
	@Override
	public int compareTo(Grade other) {
		return (new Double(this.gpa()).compareTo(new Double(other.gpa())));
	}
}
