package csc207.example.universityregistry;

import university.Student;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

public class DisplayActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display);
        
         // Gets the Intent passed from MainActivity
         Intent intent = getIntent();
         
         // Uses key "studentKey" to get Student object.
         Student student = (Student) intent.getSerializableExtra("studentKey");

         // Sets TextView to the Student's toString.
         TextView newlyRegistered = (TextView) findViewById(R.id.newly_registered_field);
         newlyRegistered.setText("Registered: " + student.toString());
    }
}
