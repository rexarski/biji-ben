package university;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class PersonTest {

    protected String[] aliceName, bobName;
    protected Person alice;

    /**
     * @throws java.lang.Exception
     */
    @Before
    public void setUp() throws Exception {
        aliceName = new String[] {"Alice", "A"};
        bobName = new String[] {"Bob", "B"};
        alice = new Person(aliceName, "01012000", "F");
    }

    /**
     * @throws java.lang.Exception
     */
    @After
    public void tearDown() throws Exception {
    }

    /**
     * Test method for {@link basicoo.Person#Person(java.lang.String[], java.lang.String, java.lang.String)}
     * and {@link basicoo.Person#getName()}.
     */
    @Test
    public void testCreateGetName() {
        assertArrayEquals("Constructor or getName failed",
                new String[] {"Alice", "A"}, alice.getName());
    }

    /**
     * Test method for {@link basicoo.Person#Person(java.lang.String[], java.lang.String, java.lang.String)}
     * and {@link basicoo.Person#getDob()}.
     */
    @Test
    public void testCreateGetDob() {
        assertEquals("Constructor or getDob failed",
                "01012000", alice.getDob());
    }

    /**
     * Test method for {@link basicoo.Person#Person(java.lang.String[], java.lang.String, java.lang.String)}
     * and {@link basicoo.Person#getDob()}.
     */
    @Test
    public void testCreateGetGender() {
        assertEquals("Constructor or getGender failed",
                "F", alice.getGender());
    }


    /**
     * Test method for {@link basicoo.Person#setName(java.lang.String[])}.
     */
    @Test
    public void testSetName() {
        alice.setName(bobName);
        assertArrayEquals("setName or getName failed", 
                bobName, alice.getName());
    }

    /**
     * Test method for {@link basicoo.Person#setDob(java.lang.String)}.
     */
    @Test
    public void testSetDob() {
        alice.setDob("12341234");
        assertEquals("setDob or getDob failed", 
                "12341234", alice.getDob());
    }

    /**
     * Test method for {@link basicoo.Person#setGender(java.lang.String)}.
     */
    @Test
    public void testSetGender() {
        alice.setGender("M");
        assertEquals("setGender or getGender failed", 
                "M", alice.getGender());
    }

    /**
     * Test method for {@link basicoo.Person#Person(java.lang.String[], java.lang.String, java.lang.String)} for aliasing problems.
     */
    @Test
    public void testPersonAliasing() {
        aliceName[0] = "Surprise!";
        assertArrayEquals("Aliasing problem in the constructor",
                new String[] {"Alice", "A"}, alice.getName());  
    }

    /**
     * Test method for {@link basicoo.Person#getName()} for aliasing problems.
     */
    @Test
    public void testGetNameAliasing() {
        String [] name = alice.getName();
        name[0] = "Surprise!";
        assertArrayEquals("Aliasing problem in getName",
                aliceName, alice.getName());
    }

    /**
     * Test method for {@link basicoo.Person#setName(java.lang.String)} for aliasing problems.
     */
    @Test
    public void testSetNameAliasing() {
        alice.setName(bobName);
        bobName[0] = "Surprise!";
        assertArrayEquals("Aliasing problem in setName",
                new String[] {"Bob", "B"}, alice.getName());
    }
}
