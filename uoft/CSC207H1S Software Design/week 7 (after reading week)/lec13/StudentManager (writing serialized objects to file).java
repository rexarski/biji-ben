package managers;

import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutput;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

import university.Student;

/**
 * Manages the saving and loading of Students.
 */
public class StudentManager {

    /** A mapping of student ids to Students. */
    private Map<String, Student> students;
    
    /**
     * Creates a new empty StudentManager.
     */
    public StudentManager() {
        students = new HashMap<>();
    }
    
    /**
     * Populates the records map from the file at path filePath.
     * @param filePath the path of the data file  
     * @throws FileNotFoundException if filePath is not a valid path
     */
    public void readFromCSVFile(String filePath) 
            throws FileNotFoundException {
        
        // FileInputStream can be used for reading raw bytes, like an image. 
        Scanner scanner = new Scanner(new FileInputStream(filePath));
        String[] record;
        Student student;

        while(scanner.hasNextLine()) {
            record = scanner.nextLine().split(",");
            student = new Student(record[0].split(" "), record[1], record[2], record[3]);
            students.put(student.getID(), student);
        }
        scanner.close();
    }
    
    /**
     * Adds record to this StudentManager.
     * @param record a record to be added.
     */
    public void add(Student record) {
        students.put(record.getID(), record);
    }
    
    /**
     * Writes the students to file at filePath.
     * @param filePath the file to write the records to
     * @throws IOException 
     */
    public void saveToFile(String filePath) throws IOException {

        OutputStream file = new FileOutputStream(filePath);
        OutputStream buffer = new BufferedOutputStream(file);
        ObjectOutput output = new ObjectOutputStream(buffer);

        // serialize the Map
        output.writeObject(students);
        output.close();
    }
    
    @Override
    public String toString() {
        String result = "";
        for (Student r : students.values()) {
            result += r.toString() + "\n";
        }
        return result;
    }
}
