import argparse
from queue import PriorityQueue

WIDTH, HEIGHT = 4, 5

def create_grid_from_file(filename):
    with open(filename) as f:
        grid = []
        for line in f:
            grid.append(list(line.strip()))
        return grid

def display_grid(grid):
    s = ''
    for line in grid:
        for ch in line:
            s += ch
        s += '\n'
    return s

def get_point_successors_single(grid):
    """Return a list of successor states for a single empty point adjacent to a 1x1 piece."""
    successors = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if grid[i][j] == '.':
                if i != 0 and grid[i - 1][j] == '2':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i - 1][j], curr[i][j] = '.', '2'
                    successors.append(curr)
                if i != HEIGHT - 1 and grid[i + 1][j] == '2':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i + 1][j], curr[i][j] = '.', '2'
                    successors.append(curr)
                if j != 0 and grid[i][j - 1] == '2':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i][j - 1], curr[i][j] = '.', '2'
                    successors.append(curr)
                if j != WIDTH - 1 and grid[i][j + 1] == '2':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i][j + 1], curr[i][j] = '.', '2'
                    successors.append(curr)
    return successors

def get_point_successors_double(grid):
    """Return a list of successor states for a single empty point adjacent to a 1x2  or 2x1 piece."""
    successors = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if grid[i][j] == '.':
                if i >= 2 and grid[i - 1][j] == 'v':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i - 2][j], curr[i - 1][j], curr[i][j] = '.', '^', 'v'
                    successors.append(curr)
                if i <= HEIGHT - 2 and grid[i + 1][j] == '^':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i + 2][j], curr[i + 1][j], curr[i][j] = '.', 'v', '^'
                    successors.append(curr)
                if j >= 2 and grid[i][j - 1] == '>':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i][j - 2], curr[i][j - 1], curr[i][j] = '.', '<', '>'
                    successors.append(curr)
                if j <= WIDTH - 2 and grid[i][j + 1] == '<':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i][j + 2], curr[i][j + 1], curr[i][j] = '.', '>', '<'
                    successors.append(curr)
    return successors

def get_point_successors(grid):
    return get_point_successors_single(grid) + get_point_successors_double(grid)

def get_vertical_successors(grid):
    successors = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if i != HEIGHT - 1 and grid[i][j] == '.' and grid[i+1][j] == '.':
                if j != 0 and grid[i][j - 1] == '^':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i][j - 1], curr[i + 1][j - 1], curr[i][j], curr[i + 1][j] = '.', '.', '^', 'v'
                    successors.append(curr)
                if j != WIDTH - 1 and grid[i][j+1] == '^':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i][j + 1], curr[i + 1][j + 1], curr[i][j], curr[i + 1][j] = '.', '.', '^', 'v'
                    successors.append(curr)
                if j != 0 and grid[i][j-1] == '1' and grid[i+1][j-1] == '1':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i][j - 2], curr[i + 1][j - 2] = '.', '.'
                    curr[i][j - 1], curr[i + 1][j - 1] = '1', '1'
                    curr[i][j], curr[i + 1][j] = '1', '1'
                    successors.append(curr)
                if j != WIDTH - 1 and grid[i][j+1] == '1' and grid[i+1][j+1] == '1':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i][j + 2], curr[i + 1][j + 2] = '.', '.'
                    curr[i][j + 1], curr[i + 1][j + 1] = '1', '1'
                    curr[i][j], curr[i + 1][j] = '1', '1'
                    successors.append(curr)
    return successors

def get_horizontal_successors(grid):
    successors = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if j != WIDTH - 1 and grid[i][j] == '.' and grid[i][j+1] == '.':
                if i != 0 and grid[i-1][j] == '<':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i - 1][j], curr[i - 1][j + 1], curr[i][j], curr[i][j + 1] = '.', '.', '<', '>'
                    successors.append(curr)
                if i != HEIGHT - 1 and grid[i+1][j] == '<':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i + 1][j], curr[i + 1][j + 1], curr[i][j], curr[i][j + 1] = '.', '.', '<', '>'
                    successors.append(curr)
                if i != 0 and grid[i-1][j] == '1' and grid[i-1][j+1] == '1':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i - 2][j], curr[i - 2][j + 1] = '.', '.'
                    curr[i - 1][j], curr[i - 1][j + 1] = '1', '1'
                    curr[i][j], curr[i][j + 1] = '1', '1'
                    successors.append(curr)
                if i != HEIGHT - 1 and grid[i+1][j] == '1' and grid[i+1][j+1] == '1':
                    curr = []
                    for k in range(HEIGHT):
                        curr.append(grid[k].copy())
                    curr[i + 2][j], curr[i + 2][j + 1] = '.', '.'
                    curr[i + 1][j], curr[i + 1][j + 1] = '1', '1'
                    curr[i][j], curr[i][j + 1] = '1', '1'
                    successors.append(curr)
    return successors

def get_successors(grid):
    return get_vertical_successors(grid) + get_horizontal_successors(grid) + get_point_successors(grid)

def is_goal(grid):
    return grid[3][1] == '1' and grid[3][2] == '1' and grid[4][1] == '1' and grid[4][2] == '1'

def get_manhattan_distance(grid):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if grid[i][j] == '1':
                return abs(i - 3) + abs(j - 1)

def run_dfs(grid):
    stack = [grid]
    while len(stack) > 0:
        curr = stack.pop()
        if is_goal(curr):
            return curr
        for successor in get_successors(curr):
            stack.append(successor)
    return None

def run_astar(grid, debug=False):
    queue = PriorityQueue()
    moves = 0
    queue.put((get_manhattan_distance(grid), (grid, moves)))
    seen = set()
    while not queue.empty():
        curr, moves = queue.get()[1]
        if display_grid(curr) in seen:
            continue
        seen.add(display_grid(curr))
        if is_goal(curr):
            return curr
        if debug:
            print(display_grid(curr), moves)
        for successor in get_successors(curr):
            queue.put((get_manhattan_distance(successor) + moves + 1, (successor, moves + 1)))
    return None

def run_search(algo, grid):
    if algo == 'dfs':
        return run_dfs(grid)
    elif algo == 'astar':
        return run_astar(grid)

def output_file(filename, input_grid, output_grid):
    with open(f"{filename}", "w") as file:
        file.write(f"{display_grid(input_grid)}\n{display_grid(output_grid)}")

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
    inp = create_grid_from_file(args.inputfile)
    # run specified algorithm on board
    outp = run_search(args.algo, inp)
    # write results to output file (create it if it is missing)
    output_file(args.outputfile, inp, outp)