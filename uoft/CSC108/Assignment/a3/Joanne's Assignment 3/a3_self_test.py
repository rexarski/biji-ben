'''A self-test module for Assignment 3. Save it in the same folder as bacon.py
and then run self_test. It will test each of the required functions on one 
simple test case.'''

# Some "magic" code that will cause an error message if your module
# does any raw_input (which you aren't supposed to do in your Assignment 3 
# functions).
def disable_input(*args):
   raise Exception("You must not call raw_input in your A3 functions!")
__builtins__.raw_input = disable_input

import bacon_functions

if __name__ == "__main__":
   
   # True iff your code has passed every test so far.
   ok = True
   
   # Test function parse_actor_data.
   if hasattr(bacon_functions, 'parse_actor_data'):
      import StringIO
      reader = StringIO.StringIO('''CRC: 0xDE308B96	 File: actors.list	Date: Fri Aug 12 00:00:00 2011

Copyright 1990-2007 The Internet Movie Database, Inc.  All rights reserved.

COPYING POLICY: Internet Movie Database (IMDb)
==============================================

    This is a  database  of  movie  related  information  compiled  by
    Internet  Movie  Database  Ltd (IMDb). While every effort has been
    made to  ensure  the  accuracy  of  the  database  IMDb  gives  no
    warranty  as  to  the accuracy of the information contained in the
    database.  IMDb  reserves  the  right  to   withdraw   or   delete
    information at any time. 
       
    This service is provided for the information of users only. It  is
    not   provided  with  the  intention  that  users  rely  upon  the
    information for any purposes. Accordingly,  IMDb  shall  under  no
    circumstances  be liable for any loss or damage, including but not
    limited to loss of profits, goodwill or indirect or  consequential
    loss   arising   out   of  any  use  of  or  inaccuracies  in  the
    information. All warranties express or  implied  are  excluded  to
    the fullest extent permissible by law. 
       
    All information in this file  is  Copyright  2005  Internet  Movie
    Database  Limited.  Reproduction,  distribution or transmission by
    any means without the prior permission of IMDb is prohibited.  All
    rights reserved. 

    For further info visit http://www.imdb.com/licensing/contact

CUTTING HEADER

THE ACTORS LIST
===============

Name					Titles
----					------
Bacon, Kevin			A Few Good Men (1992)  [Capt. Jack Ross]  <4>

De Niro, Robert			Sleepers (1996)	 [Father Bobby]  <3>

-----------------------------------------------------------------------------

SUBMITTING UPDATES
==================

CUTTING UPDATES

For further info visit http://www.imdb.com/licensing/contact
''')
      expected = {"Kevin Bacon": ["A Few Good Men (1992)"],
                "Robert De Niro": ["Sleepers (1996)"]}
      result = bacon_functions.parse_actor_data(reader)
      if expected != result:
          print "Failure of function parse_actor_data: " + \
                "Result should be %s, not %s" % (str(expected), str(result))
          ok = False
   else:
      print "Function 'parse_actor_data' is not defined"
      ok = False
       
   if hasattr(bacon_functions, 'invert_actor_dict'):
      expected = {"A Few Good Men (1992)": ["Kevin Bacon"],
                  "Sleepers (1996)": ["Kevin Bacon"]}
      result = bacon_functions.invert_actor_dict({"Kevin Bacon": ["A Few Good Men (1992)",
                                                        "Sleepers (1996)"]})
      if expected != result:
          print "Failure of function invert_actor_dict: " + \
                "Result should be %s, not %s" % (str(expected), str(result))
          ok = False
   else:
      print "Function 'invert_actor_dict' is not defined"
      ok = False

   if hasattr(bacon_functions, 'find_connection'):
      expected = [('Sleepers (1996)', 'Kevin Bacon')]
      result = bacon_functions.find_connection("Robert De Niro", 
                                     {"Kevin Bacon": ["Sleepers (1996)"],
                                      "Robert De Niro": ["Sleepers (1996)"]},
                                     {"Sleepers (1996)": ["Kevin Bacon", 
                                                          "Robert De Niro"]})
      if expected != result:
         print "Failure of function find_connection: " + \
                "Result should be %s, not %s" % (str(expected), str(result))
         ok = False
   else:
      print "Function 'find_connection' is not defined"
      ok = False

      
   # No assertions failed, so everything looks okay, at least for the
   # things we checked.
   if ok:
      print "okay"
    
