/**
 * 
 */
package university;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

/**
 * @author campbell
 *
 */
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
        alice = new Person(aliceName, "01012001", "F");
    }

    /**
     * @throws java.lang.Exception
     */
    @After
    public void tearDown() throws Exception {
    }

    /**
     * Test method for {@link university.Person#Person(java.lang.String[], java.lang.String, java.lang.String)}.
     */
    @Test
    public void testCreateGetName() {
        assertArrayEquals("Constructor or getName failed.", 
                new String[] {"Alice", "A"}, alice.getName());
    }

    /**
     * Test method for {@link university.Person#getDob()}.
     */
    @Test
    public void testGetDob() {
        fail("Not yet implemented");
    }

    /**
     * Test method for {@link university.Person#setDob(java.lang.String)}.
     */
    @Test
    public void testSetDob() {
        fail("Not yet implemented");
    }

    /**
     * Test method for {@link university.Person#getName()}.
     */
    @Test
    public void testGetName() {
        fail("Not yet implemented");
    }

    /**
     * Test method for {@link university.Person#setName(java.lang.String[])}.
     */
    @Test
    public void testSetName() {
        fail("Not yet implemented");
    }

    /**
     * Test method for {@link university.Person#getGender()}.
     */
    @Test
    public void testGetGender() {
        fail("Not yet implemented");
    }

    /**
     * Test method for {@link university.Person#setGender(java.lang.String)}.
     */
    @Test
    public void testSetGender() {
        fail("Not yet implemented");
    }

    /**
     * Test method for {@link university.Person#toString()}.
     */
    @Test
    public void testToString() {
        fail("Not yet implemented");
    }

}
