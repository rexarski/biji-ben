package university;

import java.io.Serializable;

public class Person implements Serializable {
    
    /**
     * 
     */
    private static final long serialVersionUID = 1113659063027473468L;

    /** This Person's name. */
    protected String[] name;   
    
    /** This Person's date of birth in format DDMMYYYY.     */
    protected String dob;       
    
    /** This Person's gender. */
    protected String gender;    
    
    /* 
     * This instance variable does not belong in this class.
     * We used it to demonstrate what happens when a parent class
     * and a child class declare variables with the same name.
     */
    public String example;   // Added week 3 Friday.

    /**
     * Creates a Person named name with date of birth dob
     * and gender gender.
     * 
     * @param name the name of this Person
     * @param dob the date of birth (DDMMYYYY) of this Person
     * @param gender the gender of this Person (either M or F)
     */
    public Person(String[] name, String dob, String gender) {
        
        // Updated week 3 Friday; clone() returns a shallow copy of the array
        this.name = name.clone();  
        this.dob = dob;
        this.gender = gender;
        
        // Added to show what happens when child and parent have a
        // variable with the same name.
        this.example = "Person's example"; // Added week 3 Friday.
    }
    
    /**
     * Returns the date of birth of this Person.
     * @return the date of birth (format DDMMYYYY)
     */
    public String getDob() {
        return this.dob;
    }
    
    /**
     * Sets the date of birth of this Person to dob.
     * @param dob the new date of birth (format DDMMYYYY)
     */
    public void setDob(String dob) {
        this.dob = dob;
    }

    /**
     * Returns the name of this Person.
     * @return the name of this Person
     */
    public String[] getName() {
        
        // Updated week 3 Friday; clone() returns a shallow copy of the array
        return name.clone();
    }

    /**
     * Sets the name of this Person to name.
     * @param name the new name of this Person
     */
    public void setName(String[] name) {
        
        // Updated week 3 Friday; clone() returns a shallow copy of the array
        this.name = name.clone();
    }

    /**
     * Returns the gender of this person.
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
