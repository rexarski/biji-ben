
package university;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

/**
 * @author campbell
 */
public class StudentTest extends PersonTest {

    private Student bob; 

    /* (non-Javadoc)
     * @see university.PersonTest#setUp()
     */
    @Before
    public void setUp() throws Exception {
        super.setUp();
        alice = new Student(aliceName, "01012000", "F", "9999999999");
        bob = new Student(new String[] {"Bob", "B", "Bobson"},
                "12121992", "M", "1234567890");
    }

    /* (non-Javadoc)
     * @see university.PersonTest#tearDown()
     */
    @After
    public void tearDown() throws Exception {
        super.tearDown();
    }

    /**
     * Test method for {@link university.Student#Student(java.lang.String[], java.lang.String, java.lang.String, java.lang.String)}.
     */
    @Test
    public void testCreateGetStNum() {
        assertEquals("Constructor or getStNum failed",
                "1234567890", bob.getStudentNum());
    }

    /**
     * Test method for {@link university.Student#getGrade(java.lang.String)},
     * {@link university.Student#addGrade(String, int).
     */
    @Test
    public void testAddGetGradeNumeric() {
        try {
            bob.addGrade("csc148", 77);
            assertEquals("addGrade or getGrade failed (added grade 77)",
                    new NumericGrade(77), bob.getGrade("csc148"));
        } catch (InvalidGradeException e) {
            fail("Unexpected InvalidGradeException" + e);
        }
    }

    /**
     * Test method for {@link university.Student#getGrade(java.lang.String)},
     * {@link university.Student#addGrade(String, String).
     */
    @Test
    public void testAddGetGradeLetter() {
        try {
            bob.addGrade("cscb07", "B");
            assertEquals("addGrade or getGrade failed (added grade B)",
                    new LetterGrade("B"), bob.getGrade("cscb07"));
        } catch (InvalidGradeException e) {
            fail("Unexpected InvalidGradeException" + e);
        }
    }

    /**
     * Test method for {@link university.Student#getGrade(java.lang.String)},
     * {@link university.Student#addGrade(String, int),
     * {@link university.Student#addGrade(String, String).
     */

    @Test
    public void testAddGetGradeMultiple() {
        try {
            for (int i = 0; i < 10; i++) {
                bob.addGrade("cscxx" + i, 10 * i);
                bob.addGrade("cscyy" + i, 
                        Grade.VALID_GRADES[i % Grade.VALID_GRADES.length]);
            }
            for (int i=0; i<10; i++) {
                String grade = 
                        Grade.VALID_GRADES[i % Grade.VALID_GRADES.length];
                assertEquals(
                        "addGrade or getGrade failed -- added grade " + i * 10,
                        new NumericGrade(10 * i), bob.getGrade("cscxx" + i));
                assertEquals(
                        "addGrade or getGrade failed (added grade " + i * 10,
                        new LetterGrade(grade), bob.getGrade("cscyy" + i));
            }
        } catch (InvalidGradeException e) {
            fail("Unexpected InvalidGradeException" + e);
        } 
    }

    /** 
     * Test method for  {@link university.Student#addGrade(String, int),
     * @throws InvalidGradeException    */
    @Test(expected=InvalidGradeException.class)
    public void testAddGradeNumericException() throws InvalidGradeException {
        bob.addGrade("csczzz", 120);
    }

    /** 
     * Test method for  {@link university.Student#addGrade(String, String),
     * @throws InvalidGradeException    */
    @Test(expected=InvalidGradeException.class)
    public void testAddGradeLetterException() throws InvalidGradeException {
        bob.addGrade("csczzz", "Q");
    }

    /**
     * Test method for {@link university.Student#getID()}.
     */
    @Test
    public void testGetID() {
        assertEquals("getID failed", "1234567890", bob.getID());
    }
}

