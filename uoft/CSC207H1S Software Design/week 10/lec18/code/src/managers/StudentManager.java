package managers;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInput;
import java.io.ObjectInputStream;
import java.io.ObjectOutput;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.ConsoleHandler;
import java.util.logging.Level;
import java.util.logging.Logger;

import university.Student;


/**
 * Manages the saving and loading of Students.
 */
public class StudentManager implements Serializable {

    private static final long serialVersionUID = 8641290543921831486L;

    /** A mapping of student ids to Students. */
    private Map<String, Student> students;

    /** The path of the serialized data file. */
    private String filePath;

    private static final Logger logger = 
            Logger.getLogger(StudentManager.class.getPackage().getName());

    private static final ConsoleHandler consoleHandler = new ConsoleHandler();

    /**
     * Creates a new empty StudentManager.
     * @throws IOException 
     * @throws ClassNotFoundException 
     */
    public StudentManager(File file) throws ClassNotFoundException, IOException {
        students = new HashMap<String, Student>();

        // Associate the handler with the logger.
        logger.setLevel(Level.ALL);
        consoleHandler.setLevel(Level.ALL);
        logger.addHandler(consoleHandler);

        // Reads serializable objects from file.
        // Populates the record list using stored data, if it exists.
        if (file.exists()) {
            readFromFile(file.getPath());
        } else {
            file.createNewFile();
        }

        // sets the path of the serialized data file
        this.filePath = file.getPath();
    }

    /**
     * Adds record to this StudentManager.
     * @param record a record to be added.
     */
    public void add(Student record) {
        students.put(record.getID(), record);

        // Log the addition of a student.
        logger.log(Level.FINE, "Added a new student " + record.toString());
    }

    /**
     * Writes the students to serialized data file.
     */
    public void saveToFile() {

        try {
            OutputStream file = new FileOutputStream(filePath);
            OutputStream buffer = new BufferedOutputStream(file);
            ObjectOutput output = new ObjectOutputStream(buffer);

            // serialize the Map
            output.writeObject(students);
            output.close();
        } catch(IOException ex) {
            logger.log(Level.SEVERE, 
                    "Cannot perform output. File I/O failed.", ex);
        }
    }

    /**
     * Reads serialized student data from file at path and populates
     * this StudentManager's map with that data.
     * @param path
     */
    private void readFromFile(String path) {

        try {
            InputStream file = new FileInputStream(path);
            InputStream buffer = new BufferedInputStream(file);
            ObjectInput input = new ObjectInputStream(buffer);

            //deserialize the Map
            students = (Map<String,Student>) input.readObject();
            input.close();
        } catch (IOException ex) {
            logger.log(Level.SEVERE, "Cannot read from input.", ex);
        }  catch (ClassNotFoundException ex) {
            logger.log(Level.SEVERE, "Cannot find class.", ex);
        }
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