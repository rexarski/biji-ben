import media
import random

# The Battleship constants.
HIDDEN = '-'
VACANT = 'X'
BOARD_SIZE = 10
SHIPS = ['A', 'B', 'C', 'D', 'E']
SIZES = [2, 3, 3, 4, 5]

# The functions that you need to implement.
# Replace pass with celthe function body.


def in_bounds(row, column):
    '''(int, int) -> bool
    Return True if both ints are between 0 (inclusive) and
    BOARD_SIZE (non-inclusive), and return False otherwise.'''

    return row in range(0, BOARD_SIZE) and column in range(0, BOARD_SIZE)


def is_win(hits_list):
    '''(list of ints) -> bool
    Return True if all elements of the list are 0 or if the list is empty,
    and False otherwise.'''

    L = True
    for element in hits_list:
	L = L and (element == 0)
    return L


def get_view_board():
    '''() -> list of lists of strs
    Return the board with BOARD_SIZE rows and BOARD_SIZE columns,
    where each cell contains the HIDDEN symbol.'''

    L_1 = []
    for i in range(BOARD_SIZE):
	L_2 = []
	for j in range(BOARD_SIZE):
	    L_2.append(HIDDEN)
	L_1.append(L_2)
    return L_1


def get_symbol_board(filename):
    '''(str) -> list of lists of strs
    Return the board contained in the file with the given name.'''

    L_1 = []
    input_file = open(filename, 'r')
    i = True
    while i:
	i = input_file.readline()
	L = []
	for j in i:
	    L.append(j)
	L_1.append(L)
    return L_1


def is_revealed(row, column, view_board):
    '''(int, int, list of lists of strs) -> (bool)
    The first two ints are a row and column, and the last parameter is
    a view board. Return True if cell at that row and column is revealed
    (not hidden), and return False otherwise.'''

    return view_board[row][column] != HIDDEN


def is_occupied(row1, col1, row2, col2, board):
    '''(int, int, int, int, list of list of strs) -> bool
    The first two ints are a row and column, and the third and fourth are an
    another row and column. The last parameter is a board. Return True if the
    path from the first row and column cell to the second row and column cell,
    including those two points, is not completely vacant, and return False
    otherwise. You may assume that the rows and columns given will form either
    a horizontal or vertical path, not diagonal.'''

    if row1 == row2:
	for item in board[row1][col1: col2] + [board[row2][col2]]:
	    if item != VACANT:
		return True
    elif col1 == col2:
	for item in board[row1: row2] + [board[row2]]:
	    if item[col1] != VACANT:
		return True
    return False


def is_hit(row, column, symbol_board, hits_list):
    '''(int, int, list of lists of strs, list of ints) -> int
    The first and second parameters are a row and column, the third is a board
     and the fourth is a hits list for that board. If the cell at that row and
     column of the board contains a ship, decrease the number of hits remaining
     to sink that ship by one at the appropriate position of the hits list, and
      return the number of hits remaining. If the cell does not contain a ship,
      return -1.'''

    for i in range(len(SHIPS)):
	if symbol_board[row][column] == SHIPS[i]:
	    hits_list[i] = hits_list[i] - 1
	    return hits_list[i]
    return -1


def update_board(row, column, view_board, symbol_board):
    '''(int, int, list of lists of strs, list of list of strs) -> Nonetype
    The two int parameters represent the row and column of a cell. Set the
    element of the cell at that location in the first list to value of the
    corresponding element from the second list.'''

    view_board[row][column] = symbol_board[row][column]


def get_num_moves(view_board):
    '''(list of lists of strs) -> int
    The parameter is a view board. Return the number of moves made so far for
    the board, based on the number of non-HIDDEN elements.'''

    number = 0
    for i in view_board:
	for j in i:
	    if j != HIDDEN:
		number += 1
    return number


# The starter code functions.

def display_board(board):
    '''(list of list of strs) -> ()
    Display the board.'''

    # Display the column numbers
    print ' ',
    for col_num in range(BOARD_SIZE):
	print col_num,
    print

    # Display row numbers and cell contents.
    row_num = 0
    for row in board:
	print row_num,
	for symbol in row:
	    print symbol,
	print
	row_num += 1


def place_ship(row1, col1, row2, col2, board, ship_symbol):
    '''(int, int, int, int, list of lists of strs, str) -> NoneType
    Place the ship with symbol ship_symbol on the board from (row1, col1)
    to (row2, col2).'''

    # place the ship vertically
    if (col1 == col2):
	for row in range(row1, row2):
	    board[row][col1] = ship_symbol

    # place the ship horizontally
    else:
	for col in range(col1, col2):
	    board[row1][col] = ship_symbol


def make_computer_board():
    '''() -> list of list of strs
    Return a new BOARD_SIZE by BOARD_SIZE board with the ships with symbols
    from SHIPS and sizes from SIZES placed either horizontally or vertically
    on the board at random locations and the rest of the spots VACANT.'''

    # make a BOARD_SIZE by BOARD_SIZE board that is entirely VACANT
    board = []
    for row in range(BOARD_SIZE):
	board.append([])
	for column in range(BOARD_SIZE):
	    board[row].append(VACANT)

    for index in range(len(SHIPS)):

	# get the symbol and size of the next ship to place on the board
	placed = False
	ship = SHIPS[index]
	ship_size = SIZES[index]

	while not placed:

	    # randomly generate a location at which to place the ship
	    start_row = random.randint(0, BOARD_SIZE - 1)
	    start_col = random.randint(0, BOARD_SIZE - 1)

	    # randomly determine whether to place horizontally or vertically
	    direction = random.randint(0, 1)

	    # determine the location for vertical placement
	    if direction == 0:
		end_row = start_row + ship_size
		end_col = start_col

	    # determine the location for horizontal placement
	    else:
		end_row = start_row
		end_col = start_col + ship_size

	    # check to see if the ship can be placed at this location
	    if in_bounds(start_row, end_row) \
	       and in_bounds(start_col, end_col)\
	       and not is_occupied(start_row, start_col,
	                           end_row, end_col, board):
		place_ship(start_row, start_col, end_row, end_col, board, ship)
		placed = True

    return board


def make_move(view_board):
    '''(list of list of strs) -> list of ints
    Prompt the user to enter a row and column, until a pair within the range
    0 to BOARD_SIZE - 1 (inclusive) is selected and the cell at that location
    of view_board is hidden, then return a list containing that row and
    column.'''

    row = int(raw_input("Please enter the row: ").strip())
    col = int(raw_input("Please enter the column: ").strip())

    while not in_bounds(row, col) or is_revealed(row, col, view_board):

	if not in_bounds(row, col):
	    print "Invalid cell location!  Select another cell."
	else:
	    print "That cell has already been viewed! Select another cell"
	row = int(raw_input("Please enter the row: ").strip())
	col = int(raw_input("Please enter the column: ").strip())

    return [row, col]


def display_hit_message(hit):
    '''(int) -> NoneType
    Display a message to the user saying whether a ship was hit, sunk, or
    missed.'''

    if hit > 0:
	print 'You hit a ship!  Only %d more hit(s) to sink the ship!' % (hit)
    elif hit == 0:
	print 'You sunk a ship!'
    else:
	print 'Miss!'


def main_human_no_opponent():
    '''() -> NoneType
    A single player game with no opponent.
    This exists for testing purposes.'''

    filename = media.choose_file()
    symbol_board = get_symbol_board(filename)
    view_board = get_view_board()
    display_board(view_board)
    hits_list = SIZES[:]

    while not is_win(hits_list):

	[row, col] = make_move(view_board)

	hit = is_hit(row, col, symbol_board, hits_list)
	display_hit_message(hit)

	update_board(row, col, view_board, symbol_board)
	display_board(view_board)

    print 'You won in %d moves!' % (get_num_moves(view_board))


def make_computer_move(view_board):
    ''' (list of list of strs) -> list of ints
    Randomly generate a row and column until a cell that is still HIDDEN in
    view_board is found, and return that row and column.'''

    row = random.randint(0, BOARD_SIZE - 1)
    col = random.randint(0, BOARD_SIZE - 1)

    while is_revealed(row, col, view_board):
	row = random.randint(0, BOARD_SIZE - 1)
	col = random.randint(0, BOARD_SIZE - 1)

    return [row, col]


def main_human_versus_computer():
    '''() -> NoneType
    Play the game with a single player vs. the computer.'''

    filename = media.choose_file()
    symbol_board_player = get_symbol_board(filename)
    view_board_player = get_view_board()
    hits_player = SIZES[:]

    symbol_board_computer = make_computer_board()
    view_board_computer = get_view_board()
    hits_computer = SIZES[:]

    player_turn = True

    while not is_win(hits_player) and not is_win(hits_computer):

	if player_turn:
	    symbol_board = symbol_board_computer
	    view_board = view_board_computer
	    print "Player 1's turn:"
	    display_board(view_board_computer)
	    [row, col] = make_move(view_board_computer)
	    hits_list = hits_player
	else:
	    symbol_board = symbol_board_player
	    view_board = view_board_player
	    print "Computer's turn: "
	    display_board(view_board_player)
	    #display_board(symbol_board_player)
	    [row, col] = make_computer_move(view_board_player)
	    hits_list = hits_computer

	hit = is_hit(row, col, symbol_board, hits_list)
	display_hit_message(hit)

	update_board(row, col, view_board, symbol_board)
	display_board(view_board)
	raw_input('Please enter to continue... ')
	player_turn = not player_turn

    if is_win(hits_player):
	print 'You won in %d moves!' % (get_num_moves(view_board_computer))
    else:
	print 'The computer won in %d moves.  Please try again' % \
	      (get_num_moves(view_board_player))


if __name__ == '__main__':

    # Put any code used to verify your functions here.
    a = main_human_versus_computer()
