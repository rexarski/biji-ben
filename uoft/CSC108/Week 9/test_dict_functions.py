import nose
import dict_functions

def test_increment_count_empty_dict():
    
    d = {}
    dict_functions.increment_count(d, 'a')
    assert d == {'a' : 1}
    
def test_increment_count_key_present():
    
    d = {1 : 3, 2 : 1, 7 : 4}
    dict_functions.increment_count(d, 2)
    assert d == {1 : 3, 2 : 2, 7 : 4}
    
def test_increment_count_key_absent():
    
    d = {1 : 3, 2 : 1, 7 : 4}
    dict_functions.increment_count(d, 8)
    assert d == {1 : 3, 2 : 1, 7 : 4, 8 : 1}

if __name__ == '__main__':
    nose.runmodule()