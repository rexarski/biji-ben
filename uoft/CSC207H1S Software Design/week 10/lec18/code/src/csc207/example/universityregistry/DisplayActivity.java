package csc207.example.universityregistry;

import java.io.File;

import university.Student;
import managers.StudentManager;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

public class DisplayActivity extends Activity {

    // This will get initialized when we get it from the Intent that started
    // this Activity.
    private StudentManager manager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display);

        // Gets the Intent passed from MainActivity
        Intent intent = getIntent();

        // Uses key "studentKey" to get Student object.
        manager = (StudentManager) intent.getSerializableExtra(MainActivity.STUDENT_MANAGER_KEY);

        // Sets TextView to the Student's toString.
        TextView newlyRegistered = (TextView) findViewById(R.id.newly_registered_field);
        newlyRegistered.setText("Registered: \n" + manager.toString());
    }

    // This is an onClick method: must take a View and return void.
    public void saveToFile(View view) {
        manager.saveToFile();
    }
}
