# main.py
from sudoku_py import Sudoku as Sud
from sudoku import Sudoku

import cli as cli
import sudoku_solver as solver


def main(puzzle: Sudoku):
    puzzle.show()
    solution = puzzle.solve()

    print("This is the actual solution: ")
    solution.show()

    board = solver.format_board(puzzle.board)
    if solver.solve_heuristics(board):
        print("Solved Sudoku board:")
        # result = Sud(board)
        result = __format_board_ascii(board)
        print(result)
        # for row in board:
        #     print(row)
    else:
        print("No solution exists.")


def from_nothing(puzzle: Sudoku):
    puzzle.show()
    solution = puzzle.solve()

    print("This is the actual solution: ")
    solution.show()

    board = solver.format_board(puzzle.board)
    if solver.solve_heuristics(board):
        print("Solved Sudoku board:")
        # result = Sud(board)
        result = __format_board_ascii(board)
        print(result)
        # for row in board:
        #     print(row)
    else:
        print("No solution exists.")


def __format_board_ascii(board: list[list[int]]) -> str:
    width = 3
    height = 3
    size = width * height

    table = ""
    cell_length = len(str(size))
    format_int = "{0:0" + str(cell_length) + "d}"
    for i, row in enumerate(board):
        if i == 0:
            table += ("+-" + "-" * (cell_length + 1) * width) * height + "+" + "\n"
        table += (("| " + "{} " * width) * height + "|").format(
            *[(format_int.format(x) if x != 0 else " " * cell_length) for x in row]
        ) + "\n"
        if i == size - 1 or i % height == height - 1:
            table += ("+-" + "-" * (cell_length + 1) * width) * height + "+" + "\n"
    return table


if __name__ == "__main__":
    puzzle = cli.get_puzzle()
    main(puzzle)
