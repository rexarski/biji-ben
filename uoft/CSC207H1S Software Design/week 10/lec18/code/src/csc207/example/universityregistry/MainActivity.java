package csc207.example.universityregistry;

import java.io.File;
import java.io.IOException;

import university.Student;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import managers.StudentManager;

public class MainActivity extends Activity {

    // Why use constants here?
    // If "userdata" or "students.ser" are used in several places in the code
    // then if we need to change one later on, then we need to make sure to 
    // consistently change all of them. This way I only need to change it in
    // one place.
    public static final String FILENAME = "students.ser";
    public static final String USERDATADIR = "userdata";
    public static final String STUDENT_MANAGER_KEY = "studentManagerKey";

    private StudentManager manager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);    

        File userdata = this.getApplicationContext().getDir(USERDATADIR, MODE_PRIVATE);
        File studentsFile = new File(userdata, FILENAME);

        // initialize the StudentManager
        try {
            manager = new StudentManager(studentsFile);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    // Note: an onClick method must return void and have one View parameter.  
    public void registerStudent(View view) {

        // Specifies the next Activity to move to: DisplayActivity.
        Intent intent = new Intent(this, DisplayActivity.class);

        // Gets the first name from the 1st EditText field.
        EditText firstNameField = (EditText) findViewById(R.id.first_name_field);
        String firstName = firstNameField.getText().toString();

        // Gets the last name from the 2nd EditText field.
        EditText lastNameField = (EditText) findViewById(R.id.last_name_field);
        String lastName = lastNameField.getText().toString();
        String[] name = {firstName, lastName};

        // Gets the gender from the selected radio button.
        RadioGroup genderField = (RadioGroup) findViewById(R.id.gender_field);
        int genderChoice = genderField.getCheckedRadioButtonId();
        RadioButton genderButton = (RadioButton) findViewById(genderChoice);
        String gender = (String) genderButton.getText();

        // Gets the DOB from the 3nd EditText field.
        EditText dobField = (EditText) findViewById(R.id.dob_field);
        String dob = dobField.getText().toString();

        // Gets the student number from the last EditText field.
        EditText studNumField = (EditText) findViewById(R.id.student_num_field);
        String studentNum = studNumField.getText().toString();

        // Constructs a Student object.
        Student student = new Student(name, dob, gender, studentNum);

        // Adds the Student to the Student manager
        manager.add(student);
        
        // Puts the StudentManager into the Intent to pass to the next Activity
        intent.putExtra(STUDENT_MANAGER_KEY, manager);
        
        // Starts DisplayActivity.
        startActivity(intent);       
    }
}
