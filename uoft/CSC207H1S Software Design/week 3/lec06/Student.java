	package university;

public class Student extends Person {
    
    /** This Student's student number. */
    private String studentNum;
    
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
        
        // Calling on Person's constructor.
        super(name, dob, gender);
        
        // Calling the parent's constructor instead of this:
//        this.name = name;
//        this.dob = dob;
//        this.gender = gender;
        
        this.studentNum = studentNum;
        
        // Added to show what happens when child and parent have a
        // variable with the same name.
        this.example = "Student's example";
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
}
