package university;

import java.util.ArrayList;
import java.util.List;

/**
 * A representation of a university course.
 * @author campbell
 */
public class Course implements IDed<String> {
    
    /** The id of this Course. */
    private String courseNum; 
    
    /** The Instructor of this Course. */
    private Instructor instructor;
    
    /** The maximum number of students that can be enrolled. */
    private int capacity; 
    
    /** The students enrolled in this Course. */
    private List<Student> roster; 
    
    /** The waiting list of students for this Course. */
    private WaitList<Student> waiting; 
    
    /**
     * Creates a new Course with the given course number and capacity,
     *  an empty student roster and an empty waiting list.
     * @param courseNum
     */
    public Course(String courseNum, int capacity) {
      this.roster = new ArrayList<>();
      this.waiting = new WaitList<>();
      this.courseNum = courseNum;
      this.capacity = capacity;
    }
    
    /**
     * Returns the course number of this Course.
     * @return the course number of this Course
     */
    public String getCourseNum() {
        return this.getID();
    }

    /**
     * Returns the Instructor of this Course.
     * @return the Instructor of this Course.
     */
    public Instructor getInstructor() {
        return this.instructor;
    }

    /**
     * Sets the Instructor of this Course to the given Instructor.
     * @param instructor the Instructor to set
     */
    public void setInstructor(Instructor instructor) {
        this.instructor = instructor;
    }

    /**
     * Returns capacity of this Course.
     * @return the maximum number of students that can be registered in
     * this Course.
     */
    public int getCapacity() {
        return this.capacity;
    }

    /**
     * Sets the capacity of this course (the maximum number of students
     * that can be enrlled) to the given capacity.
     * @param capacity the capacity to set
     */
    public void setCapacity(int capacity) {
        this.capacity = capacity;
    }

    /**
     * Returns the student roster of this Course -- the List of Students
     * registered in it.
     * @return the student roster of this Course -- the List of Students
     * registered in it.
     */
    public List<Student> getRoster() {
        return this.roster;
    }

    /**
     * Returns the waitlist of this Course -- the List of Students
     * on the waiting list for it.
     * @return the waitlist of this Course -- the List of Students
     * on the waiting list for it.
     */
    public WaitList<Student> getWaiting() {
        return this.waiting;
    }
    
    /**
     * Returns the course number of this Course.
     */
    @Override
    public String getID() {
        return this.courseNum; 
    }
    
    /**
     * Enrolls the given Student if this Course, if capacity permits and
     * if the student is not yet enrolled. 
     * @param student the student to enroll
     * @return whether the student was enrolled successfully
     */
    public boolean enroll(Student student) {
        if (this.roster.size() == this.capacity ||
            this.roster.contains(student)) {
            return false;
        }
        this.roster.add(student);
        return true;
    }
    
    /**
     * Drops the given student from the Course.
     * @param student the student to remove from the Course.
     * @return whether the student was removed successfully
     */
    public boolean drop(Student student) {
        return this.roster.remove(student);
    }
    
    /**
     * Puts the given student on the waiting list for this Course,
     * if the student is not yet in it.
     * @param student the student to put on the waiting list
     * @return whether the student was successfully put on the 
     * waiting list
     */
    public boolean waitlist(Student student) {
        if (this.waiting.contains(student)) {
            return false;
        }
        this.waiting.add(student);
        return true;
    }
    
    /**
     * Moves one student from the waiting list (the next in line)
     * into the course roster if capacity permits and the waitlist
     * is not empty.
     * @return whether a student was successfully moved 
     */
    public boolean move() {
        if (this.roster.size() == this.capacity ||
            this.waiting.isEmpty()) {
            return false;
        }
        return this.roster.add(this.waiting.remove());
    }

    @Override
    public String toString() {
        return "Course{" + "courseNum=" + this.courseNum + 
                ", instructor=" + this.instructor + 
                ", capacity=" + this.capacity + 
                ", roster=" + this.roster + 
                ", waiting=" + this.waiting + '}';
    }
}