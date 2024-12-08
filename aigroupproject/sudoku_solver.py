# sudoku_solver.py
import time

import cli
import sudoku_solver as solver
import tests


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


def most_constrained_variables(board: list[list[int]]) -> list[tuple[int, int]]:
    tied_cells: list[tuple[int, int]] = []
    min_valid_values = 10  # Start with a value larger than the max (9)

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                valid_values = [
                    num for num in range(1, 10) if is_valid(board, r, c, num)
                ]
                if len(valid_values) == min_valid_values:
                    # ties are allowed, if two cells are equally constrained
                    tied_cells.append((r, c))
                elif len(valid_values) < min_valid_values:
                    min_valid_values = len(valid_values)
                    # remove old cells, since this cell is more constrined.
                    tied_cells = [(r, c)]

    return tied_cells


def most_constraining_variable(
    board: list[list[int]], tied_cells: list[tuple[int, int]]
) -> tuple[int, int]:
    """From a list of tied cells, find the cell that imposes the most constraints on its
    neighbors. if there is a tie, return random of the maxs"""
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


def least_constraining_values(board: list[list[int]], row: int, col: int) -> list[int]:
    """Get the possible values of a cell, ordered by their least constraining effect"""
    candidates: list[tuple[int, int]] = []
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

    # Sort by the number of constraints (ascending)
    candidates.sort(key=lambda x: x[1])
    return [x[0] for x in candidates]


def solve_heuristics(board: list[list[int]]) -> bool:
    # Finding the most constrained variable(s)
    tied_cells: list[tuple[int, int]] = most_constrained_variables(board)

    # If the board is solved
    if not tied_cells:
        return True

    # If there's a tie, use Most Constraining Variable to break it
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


def main(board: list[list[int]]):
    start_time = time.time()
    if solver.solve_heuristics(board):
        end_time = time.time()
        print(f"Heuristic solving time: {end_time - start_time:.6f} seconds.")
        print("Solution Found. Testing for accuracy...")
        if tests.is_board_solved(board):
            print("Solution is solved and legal.")
        else:
            print("Solution is not legal")

        print("\nSolved Sudoku board:")
        result = cli.format_board_ascii(board)
        print(result)
    else:
        print("No solution exists.")


if __name__ == "__main__":
    puzzle = cli.get_puzzle()
    puzzle.show()
    board = solver.format_board(puzzle.board)
    main(board)
