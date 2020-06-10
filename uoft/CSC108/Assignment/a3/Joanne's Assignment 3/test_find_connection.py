import nose
from bacon_functions import find_connection

def test_actorname_empty():
       '''The function find_connection should return an empty list 
       if actor_name is an empty str and the Bacon Number is Infinity.
       '''
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)'],
                    'Kevin Bacon': ['m2 (2006)', 'm3 (2007)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor', 'Kevin Bacon'],
                    'm3 (2007)': ['C Actor', 'Kevin Bacon'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection("", actor_dict, movie_dict) == [], \
             'An empty list should be returned when actor_name is "".'

def test_actorname_containing_only_spaces():
       '''The function find_connection should return an empty list when 
       actor_name is a str containing only space since the Bacon Number of 
       actor_name is Infinity.
       '''
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)'],
                    'Kevin Bacon': ['m2 (2006)', 'm3 (2007)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor', 'Kevin Bacon'],
                    'm3 (2007)': ['C Actor', 'Kevin Bacon'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection('  ', actor_dict, movie_dict) == [], \
              'The Bacon Num of "  " is Infinity, an empty list is returned.'  
       
def test_data_dicts_empty():
       
       actor_dict = {}
       movie_dict = {}
       
       assert find_connection('A Actor', actor_dict, movie_dict) == [], \
             'There is no actor-movie data, an empty list should be returned.'

def test_search_from_kevinbacon_in_dicts_containing_kevinbacon():
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)'],
                    'Kevin Bacon': ['m2 (2006)', 'm3 (2007)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor', 'Kevin Bacon'],
                    'm3 (2007)': ['C Actor', 'Kevin Bacon'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection('Kevin Bacon', actor_dict, movie_dict) == [], \
             'The Bacon Num of actor_name "Kevin Bacon" is 0 when Kevin Bacon \
             exists in both actor_dict and movie_dict, return an empty list.'
       
def test_search_from_kb_in_dicts_not_containing_kb():
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor'],
                    'm3 (2007)': ['C Actor'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection('Kevin Bacon', actor_dict, movie_dict) == [], \
              'The Bacon Num of actor_name "Kevin Bacon" is 0, although Kevin \
              Bacon is not in either actor_dict or movie_dict. An empty \
              list should be returned.' 
       
def test_bacon_num_one():
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)'],
                    'Kevin Bacon': ['m2 (2006)', 'm3 (2007)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor', 'Kevin Bacon'],
                    'm3 (2007)': ['C Actor', 'Kevin Bacon'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection('C Actor', actor_dict, movie_dict) == \
             [('m3 (2007)', 'Kevin Bacon')], \
             'The Bacon Num of actor_name "C Actor" is one, return a list \
             with only one tuple representing the connection.'

def test_finite_bacon_num_more_than_one():
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)'],
                    'Kevin Bacon': ['m2 (2006)', 'm3 (2007)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor', 'Kevin Bacon'],
                    'm3 (2007)': ['C Actor', 'Kevin Bacon'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection('E Actor', actor_dict, movie_dict) == \
             [('m7 (2011)', 'A Actor'), ('m2 (2006)', 'Kevin Bacon')], \
             'The Bacon Num of actor_name "E Actor" is two, return a list with \
             two tuples representing the shortest connection.'

def test_bacon_num_infinity_dicts_not_containing_kb():
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor'],
                    'm3 (2007)': ['C Actor'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection('A Actor', actor_dict, movie_dict) == [], \
              'The Bacon Num of actor_name "A Actor" is Infinity according \
              to actor_dict and movie_dict which contain "A Actor" but not \
              contain Kevin Bacon, an empty list should be returned.'

def test_bacon_num_infinity_dicts_not_containing_actorname():
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)'],
                    'Kevin Bacon': ['m2 (2006)', 'm3 (2007)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor', 'Kevin Bacon'],
                    'm3 (2007)': ['C Actor', 'Kevin Bacon'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection('Z Actor', actor_dict, movie_dict) == [], \
             'The Bacon Num of actor_name "Z Actor" is Infinity according \
             to actor_dict and movie_dict which do not contain "Z Actor" but \
             contain Kevin Bacon, an empty list should be returned.'

def test_bacon_num_infinity_dicts_not_containing_kb_or_actorname():
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor'],
                    'm3 (2007)': ['C Actor'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection('Y Actor', actor_dict, movie_dict) == [], \
             'The Bacon Num of actor_name "Y Actor" is Infinity according \
             to "actor_dict" and "movie_dict" which do not contain "Y Actor" \
             or Kevin Bacon, an empty list should be returned.'
       
def test_bacon_num_infinity_dicts_containing_kb_and_actorname():
       
       actor_dict = {'A Actor': ['m1 (2005)', 'm2 (2006)', 'm7 (2011)'], 
                    'B Actor': ['m4 (2008)'],  
                    'C Actor': ['m1 (2005)', 'm3 (2007)', 'm4 (2008)'],
                    'D Actor': ['m4 (2008)', 'm5 (2009)'],
                    'E Actor': ['m5 (2009)', 'm7 (2011)'],
                    'F Actor': ['m6 (2010)'],
                    'G Actor': ['m6 (2010)'],
                    'H Actor': ['m6 (2010)'],
                    'Kevin Bacon': ['m2 (2006)', 'm3 (2007)']}
       
       movie_dict = {'m1 (2005)': ['A Actor', 'C Actor'],
                    'm2 (2006)': ['A Actor', 'Kevin Bacon'],
                    'm3 (2007)': ['C Actor', 'Kevin Bacon'],
                    'm4 (2008)': ['B Actor', 'C Actor', 'D Actor'],
                    'm5 (2009)': ['D Actor', 'E Actor'],
                    'm6 (2010)': ['F Actor', 'G Actor', 'H Actor'],
                    'm7 (2011)': ['A Actor', 'E Actor']}
       
       assert find_connection('G Actor', actor_dict, movie_dict) == [], \
             'The Bacon Num of actor_name "G Actor" is Infinity according \
             to "actor_dict" and "movie_dict" which contain "G Actor" and \
             Kevin Bacon, an empty list should be returned.'
      
if __name__ == "__main__":
       nose.runmodule()