# main.py
from sudoku import Sudoku

import aigroupproject.cli as cli
import aigroupproject.sudoku_solver as solver


def main(puzzle: Sudoku):
    puzzle.show()
    solution = puzzle.solve()

    print("This is the actual solution: ")
    solution.show()

    board = solver.format_board(puzzle.board)
    if solver.solve_heuristics(board):
        print("Solved Sudoku board:")
        # result = Sud(board)
        result = cli.format_board_ascii(board)
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
        result = cli.format_board_ascii(board)
        print(result)
        # for row in board:
        #     print(row)
    else:
        print("No solution exists.")


if __name__ == "__main__":
    puzzle = cli.get_puzzle()
    main(puzzle)
