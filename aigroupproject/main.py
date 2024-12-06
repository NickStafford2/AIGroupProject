# main.py
from sudoku import Sudoku

import aigroupproject.cli as cli
from aigroupproject.sudoku_solver import (
    Sud,
    find_list_of_board,
    solve_heuristics,
)


def main(puzzle: Sudoku):
    puzzle.show()
    solution = puzzle.solve()

    board = find_list_of_board(puzzle.board)
    print("This is the actual solution: ")
    solution.show()

    if solve_heuristics(board):
        print("Solved Sudoku board:")
        result = Sud(board)
        print(result)
        # for row in board:
        #     print(row)
    else:
        print("No solution exists.")


if __name__ == "__main__":
    puzzle = cli.get_puzzle()
    main(puzzle)
