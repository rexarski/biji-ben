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
		Statement stmt = null;
		String query = "SELECT DISTINCT Artist.name " +
				 "FROM Artist, Album, Genre " +
				 "WHERE Genre.genre = " + genre + 
				 " AND Genre.genre_id = Album.genre_id " + 
				 "AND Album.artist_id = Artist.artist_id";
		try {
			stmt = connection.createStatement();
			stmt.execute("SET search_path TO artistdb");
			ResultSet rs = stmt.executeQuery(query);
			while (rs.next()){
		        ArtistsInGenre.add(rs.getString("Artist.name"));
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
		Statement stmt = null;
		String query = "CREATE VIEW Target AS "
				 + "SELECT Artist.artist_id "
				 + "FROM Artist "
				 + "WHERE Artist.name = " + artist
				 + "; " 
				 + "CREATE VIEW Target_as_main AS "
				 + "SELECT DISTINCT Artist.name "
				 + "FROM Artist, Collaboration Co, Target "
				 + "WHERE Target.artist_id = Co.artist1 AND Co.artist2 = Artist.artist_id; "
				 + "CREATE VIEW Target_as_guest AS "
				 + "SELECT DISTINCT Artist.name "
				 + "FROM Artist, Collaboration Co, Target "
				 + "WHERE Target.artist_id = Co.artist2 AND Co.artist1 = Artist.artist_id; "
				 + "(SELECT * FROM Target_as_main) UNION (SELECT * FROM Target_as_guest); "
				 + "DROP VIEW Target_as_main; "
				 + "DROP VIEW Target_as_guest; "
				 + "DROP VIEW Target";
		try {
			stmt = connection.createStatement();
			stmt.execute("SET search_path TO artistdb");
			ResultSet rs = stmt.executeQuery(query);
			while (rs.next()){
				Collaborators.add(rs.getString("Artist.name"));
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
		Statement stmt = null;
		String query = "CREATE VIEW All_song AS "
				+ "SELECT bta.song_id, Artist.artist_id "
				+ "FROM Album, Artist, BelongsToAlbum bta "
				+ "WHERE Artist.name = " + artist + "; "
				+ "AND Album.artist_id = Artist.artist_id "
				+ "AND bta.album_id = Album.album_id; "
				+ "CREATE VIEW All_song_by_others AS "
				+ "SELECT All_song.song_id "
				+ "FROM All_song, Song "
				+ "WHERE ALL_song.artist_id <> Song.songwriter_id AND All_song.song_id = Song.song_id; "
				+ "SELECT DISTINCT Artist.name "
				+ "FROM All_song_by_others asbo, Artist, Song "
				+ "WHERE asbo.song_id = Song.song_id AND Song.songwriter_id = Artist.artist_id; "
				+ "DROP VIEW All_song_by_others; "
				+ "DROP VIEW All_song";
		try {
			stmt = connection.createStatement();
			stmt.execute("SET search_path TO artistdb");
			ResultSet rs = stmt.executeQuery(query);
			while (rs.next()){
				Songwriters.add(rs.getString("Artist.name"));
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

