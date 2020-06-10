package university;

import java.util.Arrays;

/** A representation of a letter grade: A, B, C, D, or F. */
public class LetterGrade extends Grade {

    /** The letter value. */
    private String grade;

    /**
     * Creates a new LetterGrade with value grade.
     * @param grade the letter grade value (must be one of Grade.VALID_GRADES)
     */
    public LetterGrade(String grade) throws InvalidGradeException {
        if (!Arrays.asList(Grade.VALID_GRADES).contains(grade)) {
            throw new InvalidGradeException();
        } else {
            this.grade = grade;
        }
    }

    /*
     * This method is required: it is abstract in Grade.
     */
    @Override
    public double gpa() {
        double gpa_value = 0.0;

        /* 
         * We can't use Java 1.7 with Android API 18, so
         * we can't use a switch statement on a String. 
         */
//        switch (grade) {
//        case "A": gpa_value = 4.0; break;
//        case "B": gpa_value = 3.0; break;
//        case "C": gpa_value = 2.0; break;
//        case "D": gpa_value = 1.0; break;
//        case "F": gpa_value = 0.0;
//        }
        
        if (grade == "A") {
            gpa_value = 4.0;
        } else if (grade == "B") {
            gpa_value = 3.0;
        } else if (grade == "C") {
            gpa_value = 2.0;
        } else if (grade == "D") {
            gpa_value = 1.0;
        } else if (grade == "F") {
            gpa_value = 0;
        }

        return gpa_value;
    }

    @Override
    public String toString() {
        return "Letter grade " + grade;
    }
    
      @Override
      public int hashCode() {
        final int prime = 31;
        int result = 1;
        
        // (Note: the statement below is a conditional statement.)
        result = prime * result + ((grade == null) ? 0 : grade.hashCode());
        
        return result;
      }

      @Override
      public boolean equals(Object obj) {
        if (this == obj)
          return true;
        if (obj == null)
          return false;
        if (getClass() != obj.getClass())
          return false;
        LetterGrade other = (LetterGrade) obj;
        if (grade == null) {
          if (other.grade != null)
            return false;
        } else if (!grade.equals(other.grade))
          return false;
        return true;
      }
}
