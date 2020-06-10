import nose
from bacon_functions import invert_actor_dict

def same_dict(dict1, dict2):
    '''Return True if dict1 and dict2 have the same keys and the same values
    mapped to the keys, regardless of the sequence of keys. Return False 
    otherwise.
    '''
    
    for key in dict1:
        # The value mapped to each key is a list.
        lst1 = dict1[key].sort()
        
        if dict2.has_key(key):
            lst2 = dict2[key].sort()
            if lst1 != lst2:
                return False        
        else:
            return False
    
    # At this stage, the comparison of every key and value pair between dict1
    # and dict2 have completed, no difference is found.
    return True
        
def test_empty_actor_dict():
    '''The function invert_actor_dict should return an empty dict if 
    "actor_dict" is an empty dict. Otherwise, assertion error occurs.
    '''
    
    assert invert_actor_dict({}) == {}, \
           'The inversion of an empty actor_dict should be also an empty dict.'

def test_one_key_actor_dict():
    '''The function invert_actor_dict should be able to handle an actor_dict
    with only one key. Otherwise, assertion error occurs.
    '''
    
    actor_dict = {'A Actor': ['m1 (2007)', 'm2 (2009)']}
    expected = {'m2 (2009)': ['A Actor'], 'm1 (2007)': ['A Actor']}

    assert same_dict(invert_actor_dict(actor_dict), expected)

def test_multiply_keys_actor_dict():
    '''The function invert_actor_dict should be able to handle an actor_dict 
    with more than one keys. Otherwise, assertion error occurs.
    '''
    
    actor_dict = {'A Actor': ['m1 (2007)', 'm2 (2009)'],
                  'B Actor': ['m3 (2008)'],
                  'C Actor': ['m4 (2010)']}
    
    expected = {'m1 (2007)': ['A Actor'],
                'm3 (2008)': ['B Actor'],
                'm4 (2010)': ['C Actor'],
                'm2 (2009)': ['A Actor'],}
    
    assert same_dict(invert_actor_dict(actor_dict), expected)

def test_several_actors_in_one_movie():
    '''The function invert_actor_dict should be able to handle an actor_dict
    with more than one actors are in the same movie. Otherwise, assertion error
    occurs.
    '''
    
    actor_dict = {'A Actor': ['m1 (2007)', 'm2 (2009)'],
                  'B Actor': ['m2 (2009)', 'm3 (2010)'],
                  'C Actor': ['m2 (2009)', 'm3 (2010)']}
    
    expected = {'m1 (2007)': ['A Actor'],
                'm2 (2009)': ['C Actor', 'A Actor', 'B Actor'],
                'm3 (2010)': ['C Actor', 'B Actor']}
    
    assert same_dict(invert_actor_dict(actor_dict), expected)
    
if __name__ == "__main__":
    nose.runmodule()