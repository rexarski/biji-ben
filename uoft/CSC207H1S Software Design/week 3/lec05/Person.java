package university;

public class Person {

    /** This person's name. */
    private String[] name;
    
    /** This person's date of birth in format DDMMYYYY.     */
    private String dob;
    
    /** This person's gender. */
    private String gender;

    /**
     * Creates a Person named name with date of birth dob
     * and gender gender.
     * 
     * @param name the name of this person
     * @param dob the date of birth (DDMMYYYY)
     * @param gender the gender (either M or F)
     */
    public Person(String[] name, String dob, String gender) {
        this.setName(name);
        this.dob = dob;
        this.setGender(gender);
    }
    
    /**
     * Gets the date of birth of this person.
     * @return the date of birth (format DDMMYYYY)
     */
    public String getDob() {
        return this.dob;
    }
    
    /**
     * Sets the date of birth of this person to dob.
     * @param dob the new date of birth (format DDMMYYYY)
     */
    public void setDob(String dob) {
        this.dob = dob;
    }

    /**
     * Gets the name of this person.
     * @return the name of this person
     */
    public String[] getName() {
        return name;
    }

    /**
     * Sets the name of this person to name.
     * @param name the new name of this person
     */
    public void setName(String[] name) {
        this.name = name;
    }

    /**
     * Gets the gender of this person.
     * @return the gender of this person (M or F)
     */
    public String getGender() {
        return gender;
    }

    /**
     * Sets the gender of this person to gender.
     * @param gender the gender of this person (M or F)
     */
    public void setGender(String gender) {
        this.gender = gender;
    }

    /** 
     * Returns a string representation of this person.
     */
    @Override
    public String toString() {
        String result = "";
        
        for (String n : this.name) {
            result = result + n + " ";
        }
        
        result += this.dob;
        
        if (this.gender.equals("M")) {
            result += ", male";
        } else {
            result += ", female";
        }
        
        return result;
    }
}
