# cli.py
from sudoku import Sudoku

import aigroupproject.cli as cli
from aigroupproject.sudoku_solver import (
    Sud,
    find_list_of_board,
    solve_heuristics,
)


def get_puzzle_from_cli():
    if (
        input(
            "Do you want to enter custom sudoku board or automatically generated board?\n (press 'c' for custom): "
        )
        == "c"
    ):
        custom_grid = cli.get_custom_puzzle()
        return Sudoku(3, board=custom_grid)
    else:
        difficulty = cli.get_difficulty()
        return Sudoku(3).difficulty(difficulty)


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
    puzzle = get_puzzle_from_cli()
    main(puzzle)
