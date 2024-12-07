# main.py
from sudoku import Sudoku

import aigroupproject.cli as cli
import aigroupproject.sudoku_solver as solver


def main(puzzle: Sudoku):
    puzzle.show()
    # solution = puzzle.solve()

    # print("This is the actual solution: ")
    # solution.show()

    board = solver.format_board(puzzle.board)
    if solver.solve_heuristics(board):
        print("Solution Found. Testing for accuracy...")
        if is_board_solved(board):
            print("Solution is solved and legal.")
        else:
            print("Solution is not legal")

        print("\nSolved Sudoku board:")
        # result = Sud(board)
        result = cli.format_board_ascii(board)
        print(result)
        # for row in board:
        #     print(row)
    else:
        print("No solution exists.")


def test_many_boards():

    pass


def is_board_legal(board: list[list[int]]) -> bool:
    def is_subgrid_legal(start_row: int, start_col: int):
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for r in range(3):
            for c in range(3):
                cell_value = board[r + start_row][c + start_col]
                if cell_value in digits:
                    digits.remove(cell_value)
        return not len(digits)

    # Check rows
    for row in board:
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for cell in row:
            if cell in digits:
                digits.remove(cell)
            elif cell == 0:
                continue
            else:
                return False

    # Check columns
    for col_idx in range(9):
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for row in board:
            cell = row[col_idx]
            if cell in digits:
                digits.remove(cell)
            elif cell == 0:
                continue  # Skip empty cells
            else:
                return False  # Duplicate value in the column

    # Check each Subgrid
    for r in range(0, 7, 3):
        for c in range(0, 7, 3):
            if not is_subgrid_legal(r, c):
                return False

    return True


def is_board_complete(board: list[list[int]]) -> bool:
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for row in board:
        for cell in row:
            if cell not in digits:
                return False
    return True


def is_board_solved(board: list[list[int]]) -> bool:
    return is_board_legal(board) and is_board_complete(board)


if __name__ == "__main__":
    puzzle = cli.get_puzzle()
    main(puzzle)
