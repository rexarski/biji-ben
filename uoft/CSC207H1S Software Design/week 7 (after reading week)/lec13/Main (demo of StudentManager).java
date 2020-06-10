package university;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
import java.util.regex.Pattern;

import managers.StudentManager;

public class Main {

    public static void main(String[] args) throws InvalidGradeException, IOException {
        demoStudentManager();
    }

    public static void demoStudentManager() throws IOException {

        String csvPath ="/Users/campbell/courses/207/course-20715s/stg/lectures/managers/students.csv";
        StudentManager sm = new StudentManager();    
        System.out.println(sm);

        // loads data from CSV for first launch of the program
        sm.readFromCSVFile(csvPath);
        System.out.println(sm);
        
        // adds a new student to StudentManager sm's records
        sm.add(new Student(new String[] {"New", "Student"},
                "10102000", "F", "1122334455"));
        System.out.println(sm);
        
        // ser isn't a standard extension, just one that I chose to use.    
        String path ="/Users/campbell/courses/207/course-20715s/stg/lectures/managers/students.ser";
        
        // Writes the existing Student objects to file.
        // This data is serialized and written to file as a sequence of bytes.
        sm.saveToFile(path);
    }
}
