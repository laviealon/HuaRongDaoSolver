from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
import sys
from adts import Stack

# ====================================================================================

char_goal = '1'
char_single = '2'


class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v') 
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, self.coord_x, self.coord_y, self.orientation)

    def __copy__(self):
        return Piece(self.is_goal, self.is_single, self.coord_x, self.coord_y, self.orientation)

    def move(self, i, j):
        """ Move the top left corner of the piece to <i,j>.

        Precondition: it is legal for the piece to move to the specified coordinate.
        """
        self.coord_y, self.coord_x = j, i


class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = 5

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()

    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = char_goal
                self.grid[piece.coord_y][piece.coord_x + 1] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = char_goal
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()



class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces. 
    State has a Board and some extra information that is relevant to the search: 
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, f=None, depth=None, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param f: The f value of current state, initialized to None.
        :type f: Optional[int]
        :param depth: The depth of current state in the search tree, initialized to None.
        :type depth: Optional[int]
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.f = f
        self.depth = depth
        self.parent = parent
        self.id = hash(board)  # The id for breaking ties.


def is_goal(grid):
    """
    Return true if this grid is in the goal state.

    :param: grid
    :type: List
    :rtype bool
    """
    pass


def _get_vert_successors(grid, i, j):
    pass


def _get_horiz_successors(grid, i, j):
    pass


def _get_point_successors(grid, i, j):
    """Find successors for an isolated blank spot at <j, i>"""
    successors = []
    try:
        if grid[i - 1][j] == '2':
            # get board.pieces.copy()
            # create new single piece at <j, i>
            # replace it with the old single piece at <j, i-1>
            curr = grid.copy()
            curr[i - 1][j], curr[i][j] = '.', '2'
            successors.append(curr)
    except IndexError:
        pass
    try:
        if grid[i + 1][j] == '2':
            curr = grid.copy()
            curr[i + 1][j], curr[i][j] = '.', '2'
            successors.append(curr)
    except IndexError:
        pass
    try:
        if grid[i][j - 1] == '2':
            curr = grid.copy()
            curr[i][j - 1], curr[i][j] = '.', '2'
            successors.append(curr)
    except IndexError:
        pass
    try:
        if grid[i][j + 1] == '2':
            curr = grid.copy()
            curr[i][j + 1], curr[i][j] = '.', '2'
            successors.append(curr)
    except IndexError:
        pass
    try:
        if grid[i - 1][j] == 'v':
            curr = grid.copy()
            curr[i - 2][j], curr[i - 1][j], curr[i][j] = '.', '^', 'v'
            successors.append(curr)
    except IndexError:
        pass
    try:
        if grid[i + 1][j] == '^':
            curr = grid.copy()
            curr[i - 2][j], curr[i - 1][j], curr[i][j] = '.', 'v', '^'
            successors.append(curr)
    except IndexError:
        pass
    try:
        if grid[i][j - 1] == '>':
            curr = grid.copy()
            curr[i][j - 2], curr[i][j - 1], curr[i][j] = '.', '<', '>'
            successors.append(curr)
    except IndexError:
        pass
    try:
        if grid[i][j + 1] == '<':
            curr = grid.copy()
            curr[i][j + 2], curr[i][j + 1], curr[i][j] = '.', '>', '<'
            successors.append(curr)
    except IndexError:
        pass
    return successors



def get_successors(grid):
    """

    :param board:
    :type Board
    :rtype list
    """
    successors = []
    for i in range(5):
        for j in range(4):
            if grid[i][j] == '.':
                successors += _get_point_successors(grid, i, j)
                if i != 4 and board.grid[i + 1][j] == '.':
                    return successors + _get_vert_successors(grid, i, j)
                elif board.grid[i][j + 1] == '.':
                    return successors + _get_horiz_successors(grid, i, j)
                
                


def run_dfs(state):
    frontier = Stack(state)
    while not frontier.is_empty():
        curr = frontier.pop()
        if is_goal(curr.board):
            return curr
        frontier.add_lst(get_successors(curr.board))
    return None

def run_astar(state):
    pass


def run_search(algorithm, board):
    """

    :param algorithm:
    :param board:
    :rtype: Board
    """
    inp_state = State(board)
    if algorithm == "dfs":
        run_dfs(inp_state)
    else:
        run_astar(inp_state)
        

def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    g_found = False

    for line in puzzle_file:

        for x, ch in enumerate(line):

            if ch == '^':  # found vertical piece
                pieces.append(Piece(False, False, x, line_index, 'v'))
            elif ch == '<':  # found horizontal piece
                pieces.append(Piece(False, False, x, line_index, 'h'))
            elif ch == char_single:
                pieces.append(Piece(False, True, x, line_index, None))
            elif ch == char_goal:
                if not g_found:
                    pieces.append(Piece(True, False, x, line_index, None))
                    g_found = True
        line_index += 1

    puzzle_file.close()

    board = Board(pieces)

    return board


def output_file(outputfile, output):
    with open(f"{outputfile}.txt", "w") as file:
        file.write(output.display())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board = read_from_file(args.inputfile)
    # run specified algorithm on board
    output = run_search(args.algo, board)
    # write results to output file (create it if it is missing)
    output_file(args.outputfile, output)
