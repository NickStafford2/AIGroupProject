# main.py
import time
from sudoku import Sudoku

import aigroupproject.cli as cli
import aigroupproject.tests as tests
import aigroupproject.sudoku_solver as solver


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
        # result = Sud(board)
        result = cli.format_board_ascii(board)
        print(result)
        # for row in board:
        #     print(row)
    else:
        print("No solution exists.")


if __name__ == "__main__":
    puzzle = cli.get_puzzle()
    puzzle.show()
    board = solver.format_board(puzzle.board)
    main(board)
