from hrd_starter import _get_point_successors, read_from_file

def locate_empty(board):
    for i in range(board.height):
        for j in range(board.width):
            if board.grid[i][j] == '.':
                return i, j
def test_get_point_successors():
    board = read_from_file("test-input-file-1")
    i, j = locate_empty(board)
    return _get_point_successors(board.grid, i, j)


def display(grid):
    s = ''
    for line in grid:
        for ch in line:
            s += ch
        s += '\n'
    return s


if __name__ == '__main__':
    for grid in test_get_point_successors():
        print(display(grid))


