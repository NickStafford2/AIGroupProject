# sudoku_solver.py


def format_board(grid: list[list[int | None]]) -> list[list[int]]:
    """Replace the None values in the grid with 0's"""
    cols: list[list[int]] = []
    for i in range(9):
        row = []
        for j in range(9):
            elem = grid[i][j] if grid[i][j] is not None else 0
            row.append(elem)
        cols.append(row)
    return cols


def is_valid(board: list[list[int]], row: int, col: int, num: int) -> bool:
    """Checks if the input 'num, can be added to the board"""

    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def most_constrained_variable(board):
    # the cell(s) with the fewest valid values remaining.
    tied_cells = []
    min_valid_values = 10  # Start with a value larger than the max (9)

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                valid_values = [
                    num for num in range(1, 10) if is_valid(board, r, c, num)
                ]
                if len(valid_values) == min_valid_values:
                    tied_cells.append((r, c))  # addi to tied cells
                elif len(valid_values) < min_valid_values:
                    min_valid_values = len(valid_values)
                    tied_cells = [(r, c)]  # resetting with new minimum

    return tied_cells


def most_constraining_variable(board, tied_cells):
    # from a list of tied cells, find the cell that imposes the most constraints on its neighbors.
    max_constraints = -1
    most_constraining_cell = tied_cells[0]

    for r, c in tied_cells:
        constraints = 0

        # counting unassigned cells in the same row and column
        for i in range(9):
            if board[r][i] == 0:
                constraints += 1
            if board[i][c] == 0:
                constraints += 1

        # counting unassigned cells in the subgrid
        start_row, start_col = 3 * (r // 3), 3 * (c // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == 0:
                    constraints += 1

        # updating the most constraining variable
        if constraints > max_constraints:
            max_constraints = constraints
            most_constraining_cell = (r, c)

    return most_constraining_cell


def least_constraining_values(board, row, col):
    # sorting values for a cell by their least constraining effect
    candidates = []
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            # counting how many other cells this value would restrict
            constraint_count = 0
            for r in range(9):
                if board[r][col] == 0 and is_valid(board, r, col, num):
                    constraint_count += 1
            for c in range(9):
                if board[row][c] == 0 and is_valid(board, row, c, num):
                    constraint_count += 1
            candidates.append((num, constraint_count))
    # sorting by the number of constraints (ascending)
    candidates.sort(key=lambda x: x[1])
    return [x[0] for x in candidates]


def solve_heuristics(board):

    # findinjg the most constrained variable(s)
    tied_cells = most_constrained_variable(board)

    # if the board is solved
    if not tied_cells:
        return True

    # if there's a tie, use Most Constraining Variable to break it
    if len(tied_cells) > 1:
        row, col = most_constraining_variable(board, tied_cells)
    else:
        row, col = tied_cells[0]

    # trying the least constraining values for the selected cell
    for num in least_constraining_values(board, row, col):
        board[row][col] = num
        # print(f"Trying {num} at ({row}, {col})")
        if solve_heuristics(board):
            return True
        board[row][col] = 0
        # print(f"Backtracking at ({row}, {col})")

    return False
