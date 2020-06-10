package week3lab;

public class Author {
	
	/** This Author's first name. */
	private String firstname;
	
	/** This Author's last name. */
	private String lastname;

	/**
	 * Creates a new Author with first name firstname 
	 * and last name lastname.
	 * 
	 * @param firstname
	 * @param lastname
	 */
	public Author(String firstname, String lastname) {
		
		this.firstname = firstname;
		this.lastname = lastname;
	}

	/**
	 * Returns the first name of this Author.
	 * @return the firstname
	 */
	public String getFirstname() {
		return firstname;
	}

	/**
	 * Sets the first name of this Author to firstname.
	 * @param firstname the firstname to set
	 */
	public void setFirstname(String firstname) {
		this.firstname = firstname;
	}

	/**
	 * Returns the last name of this Author.
	 * @return the lastname
	 */
	public String getLastname() {
		return lastname;
	}

	/**
	 * Sets the last name of this Author to lastname.
	 * @param lastname the lastname to set
	 */
	public void setLastname(String lastname) {
		this.lastname = lastname;
	}

	/**
	 * @see java.lang.Object#toString()
	 */
	public String toString() {
				
		return this.lastname + ", " + this.firstname;
	}
}
