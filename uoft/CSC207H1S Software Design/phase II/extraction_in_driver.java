	public static void main(String args[]) throws ClassNotFoundException, IOException {
		User launcher = new User("hello", "hello", "hello", "hello", "hello",
				"hello", "hello", "hello");
		try {
			uploadClientInfo(path2);
		} catch (ClassNotFoundException e) {
			System.out.println("Exception1.");
		} catch (IOException e) {
			System.out.println("Exception2.");
		}
		try {
			uploadFlightInfo(path1);
		} catch (ClassNotFoundException e) {
			System.out.println("Exception3.");
		} catch (IOException e) {
			System.out.println("Exception4.");
		}
		try {
			String client = getClient("rexarski@gmail.com");
			System.out.println(client);
		} catch (ClassNotFoundException e) {
			System.out.println("Exception5.");
		} catch (IOException e) {
			System.out.println("Exception6.");
		}

		// String flight = getFlights("2015-03-11", "A", "D");
		// String itiCost = getItinerariesSortedByCost("2015-03-11", "A", "D");
		// String itiTime = getItinerariesSortedByTime("2015-03-11", "A", "D");
		// System.out.println(flight);
		// System.out.println(itiCost);
		// System.out.println(itiTime);
		String simpleItinerary = getItineraries("2015-03-11", "A", "D");
	}