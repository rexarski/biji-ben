import nose
import buggy_functions

def test_is_lowercase_empty():
    assert buggy_functions.is_lowercase("") == True, "The empty string"
    
def test_is_lowercase_correct():
    assert buggy_functions.is_lowercase("abcdef"), "Lowercase string"
    
def test_is_lowercase_nonletter():
    assert not buggy_functions.is_lowercase("a123.,!a"), \
    "Non-alphabetic string"
    
def test_is_lowercase_uppercase():
    assert not buggy_functions.is_lowercase("abCdef"), "Uppercase string" 

def test_evens_empty():
    assert buggy_functions.evens([]) == [], 'Empty list'
    
def test_evens_no_even_index():
    assert buggy_functions.evens([1]) == [], 'No even index'
    
def test_evens_no_even_index_2():
    assert buggy_functions.evens([1, 2]) == [], 'No even index'

def test_evens_one_even_index():
    assert buggy_functions.evens([1, 2, 3]) == [3], 'One even index'
    
def test_evens_mult_even_indices():
    assert buggy_functions.evens([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])\
           == [3, 5, 7, 9], 'More than one even index'

def test_reverse_empty():
    assert buggy_functions.reverse([]) == [], 'Nothing to reverse'
        
def test_reverse_one_item():
    assert buggy_functions.reverse([1]) == [1], 'One item'

def test_reverse_two_items():
    assert buggy_functions.reverse([1, 2]) == [2, 1], 'Two items'

def test_reverse_odd_diff_numbers():
    assert buggy_functions.reverse([3, 2, 1]) == [1, 2, 3], \
           'Odd different numbers'

def test_reverse_same_first_and_last():
    assert buggy_functions.reverse([1, 2, 1]) == [1, 2, 1], \
           'First and last numbers are the same'

def test_reverse_more_diff_numbers():
    assert buggy_functions.reverse([5, 3, 1, 0]) == [0, 1, 3, 5],\
           'More different numbers'

def test_left_strip_two_empty():
    assert buggy_functions.left_strip('', '') == '', 'Two empty strings'
    
def test_left_strip_empty_test():
    assert buggy_functions.left_strip('', 's') == '', 'No test case'
    
def test_left_strip_empty_single_char():
    assert buggy_functions.left_strip('s', '') == 's', \
           'Nothing asked to be removed'
           
def test_left_strip_nothing_to_be_removed():
    assert buggy_functions.left_strip('wassup', 's') == 'wassup', \
           'Nothing to be removed'
    
def test_left_strip_stuff_to_strip():
    assert buggy_functions.left_strip('ddddude', 'd') == 'ude', \
           'Stuff stripped at beginning'
    
def test_left_strip_everything():
    assert buggy_functions.left_strip('ddddddd', 'd') == '', \
           'Everything stripped'

def test_halve_my_digits_empty():
    assert buggy_functions.halve_my_digits('') == '', 'Nothing to halve'
    
def test_halve_my_digits_number():
    assert buggy_functions.halve_my_digits('12345') == '01122', 'Halve \
    entire string'
    
def test_halve_my_digits_mix_str_num():
    assert buggy_functions.halve_my_digits('wh4t3v3r') == 'wh2t1v1r', \
           'Halve numbers in str only'

def test_halve_my_digits_no_num():
    assert buggy_functions.halve_my_digits('whatever') == 'whatever', \
           'No num appears in str'

def test_halve_my_digits_space_mix():
    assert buggy_functions.halve_my_digits('  123  abc  ') == \
           '  011 abc  ', 'Spaces and strs together'
    1
    
if __name__ == '__main__':
    nose.runmodule()
