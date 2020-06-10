package university;

/**
 * A representation of an instructor.
 * @author campbell
 */
public class Instructor extends Person implements IDed<Integer> {
    
    /** This Instructor's employee number. */
    private Integer employeeNum;

    /**
     * Creates a new Instructor with the given name, date of birth,
     * gender and employee number.
     * @param name the name of the new Instructor
     * @param dob the date of birth of the new Instructor (DDMMYYYY)
     * @param gender the gender of the enw Instructor (M or F)
     * @param employeeNum the employee number of the new Instructor
     */
    public Instructor(String[] name, String dob, String gender,
            Integer employeeNum) {
        super(name, dob, gender);
        this.employeeNum = employeeNum;
    }

    @Override
    public Integer getID() {
        return null;
    }
    
    @Override
    public String toString() {
        return super.toString() + employeeNum;
    }

}
