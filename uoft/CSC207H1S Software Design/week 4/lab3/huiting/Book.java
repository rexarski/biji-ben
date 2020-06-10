package week3lab;

public class Book {
	
	/** This Book's title. */
	private String title;
	
	/** This Book's authors. */
	private Author[] authors;
	
	/** This Book's ISBN. */
	private String iSBN;
	
	/** This Book's price. */
	private double price;
		
	/**
	 * Creates a new Book with title title, authors authors, 
	 * ISBN iSBN, and price price.
	 * 
	 * @param title
	 * @param authors
	 * @param iSBN
	 * @param price
	 */
	public Book(String title, Author[] authors, String iSBN, double price) {
		
		this.title = title;
		this.authors = authors.clone();
		this.iSBN = iSBN;
		this.price = price;
	}

	/**
	 * Returns the title of this Book.
	 * @return the title
	 */
	public String getTitle() {
		return title;
	}

	/**
	 * Sets the title of this Book to title.
	 * @param title the title to set
	 */
	public void setTitle(String title) {
		title = this.title;
	}

	/**
	 * Returns the authors of this book.
	 * @return the authors
	 */
	public Author[] getAuthors() {
		return authors;
	}

	/**
	 * Sets the authors of this book to authors.
	 * @param authors the authors to set
	 */
	public void setAuthors(Author[] authors) {
		authors = this.authors;
	}

	/**
	 * Returns the ISBN of this Book.
	 * @return the iSBN
	 */
	public String getISBN() {
		return iSBN;
	}

	/**
	 * Sets the ISBN of this Book to iSBN.
	 * @param iSBN the iSBN to set
	 */
	public void setISBN(String iSBN) {
		iSBN = this.iSBN;
	}

	/**
	 *Returns the price of this Book.
	 * @return the price
	 */
	public double getPrice() {
		return price;
	}

	/**
	 * Sets the price of this Book to price.
	 * @param price the price to set
	 */
	public void setPrice(double price) {
		price = this.price;
	}

	/**
	 * Returns a string representation of this Book.
	 */
	public String toString() {
		
		String result = this.title + " (" + this.iSBN + ", $" + Double.toString(this.price) +
		", by ";
		
		for (int i = 0; i < authors.length - 1; i++) {
			
			result = result + authors[i].toString() + " and ";
		}
		
		result += authors[authors.length - 1].toString() + ")";
		
		return result;
	}
	
	public static void main(String[] args) {
		
		Author author1 = new Author("Russel", "Winder");
		Author author2 = new Author("Graham", "Roberts");
		Author[] authors = {author1, author2};
		
		Book book = new Book("Developing Java Software", authors, "978-0470090251", 79.75);
		
		System.out.println(book);
		
	}

}
