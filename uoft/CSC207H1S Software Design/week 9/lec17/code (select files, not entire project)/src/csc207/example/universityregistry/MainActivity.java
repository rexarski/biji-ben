package csc207.example.universityregistry;

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

public class MainActivity extends Activity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);    
    }
    
    // Note: an onClick method must return void and have one View parameter.  
    public void registerStudent(View view) {
         
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
        
        // Specifies the next Activity to move to: DisplayActivity.
        Intent intent = new Intent(this, DisplayActivity.class);
   
        // Passes the Student object to DisplayActivity.
        intent.putExtra("studentKey", student);
        startActivity(intent);       // Starts DisplayActivity.
    }
}
