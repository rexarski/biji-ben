'''This module should be used to test the parameter and return types of your
functions.  Run this on your a2.py and make sure there are no errors before
submitting.'''

import a2
import media

if __name__ == "__main__":
	
    # Type check a2.in_bounds	
    result = a2.in_bounds(2, 7)
    
    assert isinstance(result, bool),\
    '''a2.in_bounds(2, 7) should return a bool, 
    but returned %s.''' % (type(result))

    # Type check a2.is_win
    result = a2.is_win([1, 2, 3, 0, 1])

    assert isinstance(result, bool),\
    '''a2.is_win([1, 2, 3, 0, 1]) should return a bool, 
    but returned %s.''' % (type(result))
    
    # Type check a2.get_view_board
    result = a2.get_view_board()

    assert isinstance(result, list),\
    '''a2.get_view_board should return a list of lists of strs, 
    but returned %s.''' % (type(result))

    for inner_list in result:
        for element in inner_list:
            assert isinstance(element, str),\
            '''a2.get_view_board should return a list of lists of strs, 
            but an element in an inner list was %s.''' % (type(element))

    # Type check a2.get_symbol_board
    result = a2.get_symbol_board('sample_board.txt')

    assert isinstance(result, list),\
    '''a2.get_symbol_board should return a list of lists of strs, 
    but returned %s.''' % (type(result))

    for inner_list in result:
        for element in inner_list:
            assert isinstance(element, str),\
            '''a2.get_symbol_board should return a list of lists of strs, 
            but an element in an inner list was %s.''' % (type(element))
            
    # Type check a2.is_revealed
    board = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
             ['X', 'X', 'X', 'X', 'A', 'A', 'X', 'X', 'C', 'X'], 
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'C', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'X', 'C', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
             ['X', 'E', 'X', 'B', 'B', 'B', 'X', 'D', 'X', 'X'], 
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]
    result = a2.is_revealed(0, 0, board)    

    assert isinstance(result, bool),\
    '''a2.is_revealed(0, 0, board) should return a bool, 
    but returned %s.''' % (type(result))
    
    # Type check a2.is_occupied
    board = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
             ['X', 'X', 'X', 'X', 'A', 'A', 'X', 'X', 'C', 'X'], 
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'C', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'X', 'C', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
             ['X', 'E', 'X', 'B', 'B', 'B', 'X', 'D', 'X', 'X'], 
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]
    result = a2.is_occupied(0, 2, 2, 2, board)

    assert isinstance(result, bool),\
    '''a2.is_occupied(0, 2, 2, 2, board) should return a bool, 
    but returned %s.''' % (type(result))
    
    # Type check a2.is_hit
    board = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
             ['X', 'X', 'X', 'X', 'A', 'A', 'X', 'X', 'C', 'X'], 
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'C', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'X', 'C', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
             ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
             ['X', 'E', 'X', 'B', 'B', 'B', 'X', 'D', 'X', 'X'], 
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]
    result = a2.is_hit(0, 0, board, [2, 3, 3, 4, 5])

    assert isinstance(result, int),\
    '''a2.is_hit(0, 0, board, [2, 3, 3, 4, 5]) should return an int, 
    but returned %s.''' % (type(result))



    # Type check a2.update_board
    symbol_board = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
                    ['X', 'X', 'X', 'X', 'A', 'A', 'X', 'X', 'C', 'X'], 
                    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'C', 'X'], 
                    ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'X', 'C', 'X'], 
                    ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
                    ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
                    ['X', 'E', 'X', 'X', 'X', 'X', 'X', 'D', 'X', 'X'], 
                    ['X', 'E', 'X', 'B', 'B', 'B', 'X', 'D', 'X', 'X'], 
                    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
                    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

    view_board = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]

    result = a2.update_board(0, 0, view_board, symbol_board)

    assert isinstance(result, type(None)),\
    '''a2.update_board(0, 0, view_board, symbol_board) should return None, 
    but returned %s.''' % (type(result))

    # Type check a2.get_num_moves
    view_board = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                  ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]

    result = a2.get_num_moves(view_board)

    assert isinstance(result, int),\
    '''a2.get_num_moves(view_board) should return an int, 
    but returned %s.''' % (type(result))    
