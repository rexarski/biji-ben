import java.util.ArrayList;      // This is the main data structure.
import java.util.Collections;    // This import is for sorting ArrayLists

import java.util.Set;            // You may find these classes helpful,
import java.util.LinkedHashSet;  // but you aren't required to use them.

import java.sql.*;

public class Assignment2 {

  // A connection to the database
  private Connection connection;

  // Empty constructor. There is no need to modify this.
  public Assignment2() {}

  /**
   * Establishes a connection to be used for this session, assigning it to
   * the instance variable 'connection'.
   *
   * @param  url       the url to the database
   * @param  username  the username to connect to the database
   * @param  password  the password to connect to the database
   * @return           true if the connection is successful, false otherwise
   */
  public boolean connectDB(String url, String username, String password) {
    // Implement this method!
    return false;
  }

  /**
   * Closes the database connection.
   *
   * @return true if the closing was successful, false otherwise
   */
  public boolean disconnectDB() {
    // Implement this method!
    return false;
  }

  /**
   * Returns a sorted list of the names of people who have acted in
   * at least one movie with the input person.
   *
   * Returns an empty list if the input person is not found.
   *
   * NOTES:
   * 1. The names should be taken directly from the database,
   *    without any formatting. (So the form is 'Pitt, Brad')
   * 2. Use Collections.sort() to sort the names in ascending
   *    alphabetical order.
   *
   * @param  person  the name of the person to find the co-stars for
   * @return         a sorted list of names of actors who worked with person
   */
  public ArrayList<String> findCoStars(String person) {
    // Implement this method!
    return new ArrayList<String>();
  }

  /**
   * Computes and returns the connectivity between two actors.
   *
   * Returns 0 if the two arguments are equal, regardless of whether they are
   * in the database or not.
   * Returns -1 if at least one of the input actors are not found.
   *
   * WARNING:
   * Do not assume the actors are connected; return -1 if they are not.
   * It's easy to write this method naively and get into an infinite loop
   * when the actors are not connected. Make sure you handle this!
   *
   * @param person1  the name of an actor
   * @param person2  the name of an actor
   * @return         the connectivity between the actors, or -1 if they
   *                 are not connected
   */
  public int computeConnectivity(String person1, String person2) {
    // Implement this method!
    return -1000;
  }
}
