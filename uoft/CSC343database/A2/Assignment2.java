import java.util.ArrayList;
import java.sql.*;
import java.util.Collections;


public class Assignment2 {

	/* A connection to the database */
	private Connection connection;

	/**
	 * Empty constructor. There is no need to modify this. 
	 */
	public Assignment2() {
		try {
			Class.forName("org.postgresql.Driver");
		} catch (ClassNotFoundException e) {
			System.err.println("Failed to find the JDBC driver");
		}
	}

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
		try {
			this.connection = DriverManager.getConnection(url, username, password);
			return true;
		} catch (SQLException se) {
			System.err.println("SQL Exception. <Message>: " + se.getMessage());
			return false;
		}
	}

	/**
	* Closes the database connection.
	*
	* @return true if the closing was successful, false otherwise
	*/
	public boolean disconnectDB() {
		try {
			this.connection.close();
		return true;
		} catch (SQLException se) {
			System.err.println("SQL Exception. <Message>: " + se.getMessage());
			return false;
		}
	}

	/**
	 * Returns a sorted list of the names of all musicians and bands 
	 * who released at least one album in a given genre. 
	 *
	 * Returns an empty list if no such genre exists or no artist matches.
	 *
	 * NOTE:
	 *    Use Collections.sort() to sort the names in ascending
	 *    alphabetical order.
	 *
	 * @param genre  the genre to find artists for
	 * @return       a sorted list of artist names
	 */
	public ArrayList<String> findArtistsInGenre(String genre) {
		ArrayList<String> ArtistsInGenre = new ArrayList<String>();
		PreparedStatement stmt = null;
		ResultSet rs = null;
		String query = "SELECT DISTINCT Artist.name " +
				 "FROM Artist, Album, Genre " +
				 "WHERE Genre.genre = ? " +
				 " AND Genre.genre_id = Album.genre_id " + 
				 "AND Album.artist_id = Artist.artist_id";
		try {
			Statement st = connection.createStatement();
			st.execute("SET search_path TO artistdb");
			stmt = connection.prepareStatement(query);
			stmt.setString(1, genre);
			rs = stmt.executeQuery();
			while (rs.next()){
		        ArtistsInGenre.add(rs.getString("name"));
			}
		} catch (SQLException e ) {
			e.printStackTrace();
	    } finally {
	    	try{
	            stmt.close();
	         }catch(Exception e){e.printStackTrace();}
	    }
		Collections.sort(ArtistsInGenre);
		return ArtistsInGenre;
	}	

	/**
	 * Returns a sorted list of the names of all collaborators
	 * (either as a main artist or guest) for a given artist.  
	 *
	 * Returns an empty list if no such artist exists or the artist 
	 * has no collaborators.
	 *
	 * NOTE:
	 *    Use Collections.sort() to sort the names in ascending
	 *    alphabetical order.
	 *
	 * @param artist  the name of the artist to find collaborators for
	 * @return        a sorted list of artist names
	 */
	public ArrayList<String> findCollaborators(String artist) {
		ArrayList<String> Collaborators = new ArrayList<String>();
		PreparedStatement stmt = null;
		ResultSet rs = null;
		String query = "SELECT DISTINCT a2.name "
				+ "FROM Artist a1, Artist a2, Collaboration Co "
				+ "WHERE a1.name = ? "
				+ "AND ((a1.artist_id = Co.artist1 AND Co.artist2 = a2.artist_id) "
				+ "OR (a1.artist_id = Co.artist2 AND Co.artist1 = a2.artist_id)) ";

		try {
			Statement st = connection.createStatement();
			st.execute("SET search_path TO artistdb");
			stmt = connection.prepareStatement(query);
			stmt.setString(1, artist);
			rs = stmt.executeQuery();
			while (rs.next()){
				Collaborators.add(rs.getString("name"));
			}
		} catch (SQLException e ) {
			e.printStackTrace();
	    } finally {
	    	try{
	            stmt.close();
	         }catch(Exception e){e.printStackTrace();}
	    }
			
		Collections.sort(Collaborators);
		return Collaborators;
	}


	/**
	 * Returns a sorted list of the names of all songwriters
	 * who wrote songs for a given artist (the given artist is excluded).  
	 *
	 * Returns an empty list if no such artist exists or the artist 
	 * has no other songwriters other than themself.
	 *
	 * NOTE:
	 *    Use Collections.sort() to sort the names in ascending
	 *    alphabetical order.
	 *
	 * @param artist  the name of the artist to find the songwriters for
	 * @return        a sorted list of songwriter names
	 */
	public ArrayList<String> findSongwriters(String artist) {
		ArrayList<String> Songwriters = new ArrayList<String>();
		PreparedStatement stmt = null;
		ResultSet rs = null;
		String query = "SELECT DISTINCT a2.name "
				+ "FROM Album, Artist a1, Artist a2, BelongsToAlbum bta, Song "
				+ "WHERE a1.name = ? "
				+ " AND Album.artist_id = a1.artist_id AND bta.album_id = Album.album_id "
				+ "AND a1.artist_id <> Song.songwriter_id AND a2.artist_id = Song.songwriter_id "
				+ "AND bta.song_id = Song.song_id ";
		try {
			Statement st = connection.createStatement();
			st.execute("SET search_path TO artistdb");
			stmt = connection.prepareStatement(query);
			stmt.setString(1, artist);
			rs = stmt.executeQuery();
			while (rs.next()){
				Songwriters.add(rs.getString("name"));
			}
		} catch (SQLException e ) {
			e.printStackTrace();
	    } finally {
	    	try{
	            stmt.close();
	         }catch(Exception e){e.printStackTrace();}
	    }
			
		Collections.sort(Songwriters);
		return Songwriters;
	}

	/**
	 * Returns a sorted list of the names of all acquaintances
	 * for a given pair of artists.  
	 *
	 * Returns an empty list if either of the artists does not exist, 
	 * or they have no acquaintances.
	 *
	 * NOTE:
	 *    Use Collections.sort() to sort the names in ascending
	 *    alphabetical order.
	 *
	 * @param artist1  the name of the first artist to find acquaintances for
	 * @param artist2  the name of the second artist to find acquaintances for
	 * @return         a sorted list of artist names
	 */
	public ArrayList<String> findAcquaintances(String artist1, String artist2) {
		ArrayList<String> CommonCollaborators = new ArrayList<String>();
		ArrayList<String> CommonSongwriters = new ArrayList<String>();
		ArrayList<String> CommonAcq = new ArrayList<String>();
		CommonCollaborators = this.intersection(findCollaborators(artist1), findCollaborators(artist2));
		CommonSongwriters = this.intersection(findSongwriters(artist1), findSongwriters(artist2));
		CommonAcq.addAll(CommonCollaborators);
		CommonAcq.addAll(CommonSongwriters);
		Collections.sort(CommonAcq);
		return CommonAcq;
	}
	
	 public ArrayList<String> intersection(ArrayList<String> list1, ArrayList<String> list2) {
		 ArrayList<String> list = new ArrayList<String>();
		 for (String t : list1) {
			 if(list2.contains(t)) {
				 list.add(t);
	         }
	     }
		 return list;
	}
	
	

	
	public static void main(String[] args) {
		
		Assignment2 a2 = new Assignment2();
		
		/* TODO: Change the database name and username to your own here. */
		a2.connectDB("jdbc:postgresql://localhost:5432/csc343h-g3irui",
		             "g3irui",
		             "");
		
        System.err.println("\n----- ArtistsInGenre -----");
        ArrayList<String> res = a2.findArtistsInGenre("Rock");
        for (String s : res) {
             System.err.println(s);
        }

		System.err.println("\n----- Collaborators -----");
		res = a2.findCollaborators("Michael Jackson");
		for (String s : res) {
		  System.err.println(s);
		}
		
		System.err.println("\n----- Songwriters -----");
	    res = a2.findSongwriters("Justin Bieber");
		for (String s : res) {
		  System.err.println(s);
		}
		
		System.err.println("\n----- Acquaintances -----");
		res = a2.findAcquaintances("Jaden Smith", "Miley Cyrus");
		for (String s : res) {
		  System.err.println(s);
		}

		
		a2.disconnectDB();
	}
}
