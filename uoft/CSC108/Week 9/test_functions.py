import nose
import functions

def test_our_max_first_bigger():
    
    assert functions.our_max(8, 4) == 8, \
           'First number is larger.'

def test_our_max_second_bigger():
    
    assert functions.our_max(4, 7) == 7, \
           'Second number is larger.'
    
def test_our_max_same():
    
    assert functions.our_max(5, 5) == 5,\
           'The numbers are the same.'

def test_same_string_empty():
    
    assert functions.same_string('', ''),\
           'Empty strings.'
    
def test_same_string_diff_contents():
    
    assert not functions.same_string('abc', 'efg'),\
           'Different string contents.'

def test_same_string_diff_case():
    
    assert functions.same_string('abc', 'ABC'),\
           'Same string, different case.'

if __name__ == '__main__':
    nose.runmodule()