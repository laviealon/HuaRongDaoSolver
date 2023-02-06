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

def get_point_succesors(grid):
    return get_point_successors_single(grid) + get_point_successors_double(grid)

if __name__ == '__main__':
    grid = create_grid_from_file('tests/test-input-file-3')
    for grid in get_point_succesors(grid):
        print(display_grid(grid))
