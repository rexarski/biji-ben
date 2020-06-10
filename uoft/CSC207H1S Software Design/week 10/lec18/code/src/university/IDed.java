package university;

/*
 * Interfaces cannot be instantiated.
 * All methods in an interface are abstract.
 * An interface cannot have instance variables (can only
 * have public static final variables).
 * A class may implement multiple interfaces.
 */

/*
 * This was our first version of IDed.
 * The getID() method returned a String.
 * Class Student implements IDed.
 * But then we wanted Instructor to implement IDed too,
 * and we wanted its getID() method to return an Integer.
 * See our revised version below.
 */
//public interface IDed {
//	
//	public String getID();
//
//}

/*
 * Now IDed is a generic interface.
 * We say that IDed is a parameterized type and
 * T is the type variable (or type parameter). 
 * Typically we use T (stands for type). 
 * For collections, we use E (stands for element), as in the Java API.
 */
public interface IDed<T> {
	
	public T getID();

}