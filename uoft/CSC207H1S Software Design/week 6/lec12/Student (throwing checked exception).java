package university;

import java.util.HashMap;
import java.util.Map;

public class Student extends Person implements IDed<String> {
    
    /** This Student's student number. */
    private String studentNum;

    /** A mapping of Course to Grades for this Student. */
    private Map<String, Grade> courseToGrade;
    
    /** The total number of Students. */
    private static int studentCount = 0;
    
    /* 
     * This instance variable does not belong in this class.
     * We used it to demonstrate what happens when a parent class
     * and a child class declare variables with the same name.
     */
    public String example;   

    /**
     * Creates a new Student with named name with date of birth dob,
     * gender gender, and student number studentNum.
     * 
     * @param name the name of this Student
     * @param dob the date of birth (DDMMYYYY) of this Student
     * @param gender the gender of this Student (either M or F)
     * @param studentNum the student number of this Student
     */
    public Student(String[] name, String dob,
            String gender, String studentNum) {
        
        super(name, dob, gender);
        this.studentNum = studentNum;
        
        // Added to show what happens when child and parent have a
        // variable with the same name.
        this.example = "Student's example";
        
        studentCount++; 
        this.courseToGrade = new HashMap<>();
    }
    
    /**
     * Records that this Student obtained the given grade in the
     * given course.
     * @param course the course for which to record the given grade
     * @param grade the grade to record for the given course; must be
     * in [0, 100].
     * @throws InvalidGradeException if grade is not in [0, 100]
     */
    public void addGrade(String course, int grade) throws InvalidGradeException {
        this.courseToGrade.put(course, new NumericGrade(grade));
    }

    /**
     * Records that this Student obtained the given grade in the
     * given course.
     * @param course the course for which to record the given grade
     * @param grade the grade to record for the given course; must be
     * in Grade.VALID_GRADES.
     */
    public void addGrade(String course, String grade) {
        this.courseToGrade.put(course, new LetterGrade(grade));
    }    
    
    // Updated Week 6 Friday
    /**
     * Returns the Grade of this Student for the given course.
     * @param course the course for which the grade is returned.
     * @return the Grade of this Student for the given course
     */
    public Grade getGrade(String course) {
        return this.courseToGrade.get(course);
    }
    
    /**
     * Returns the student number of this Student.
     * @return the student number of this Student
     */
    public String getStudentNum() {
        return this.studentNum;
    }

    /**
     * Returns a string representation of this Student.
     */
    @Override
    public String toString() {
        return super.toString() + ", " + this.studentNum;
    }

    /**
     * Returns the total number of Students.
     * @return the total number of Students
     */
    public static int getStudentCount() {
        return studentCount;
    }

    @Override
    public String getID() {
        return this.studentNum;
    }
}
