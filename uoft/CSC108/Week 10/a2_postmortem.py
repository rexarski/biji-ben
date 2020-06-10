BOARD_SIZE = 10
HIDDEN = '-'
VACANT = 'X'

def make_board(symbol):
    board = []
    for row in range(BOARD_SIZE):
	board.append([])
	for column in range(BOARD_SIZE):
	    board[row].append(symbol)
    return board

if __name__ == '__main__':
    print make_board(HIDDEN)
    print make_board(VACANT)