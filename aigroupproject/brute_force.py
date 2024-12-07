# brute_force.py
import aigroupproject.tests as tests
import time

import aigroupproject.cli as cli
import aigroupproject.sudoku_solver as solver


def brute_force(board: list[list[int]]) -> bool:
    """
    A brute-force backtracking solution to solve Sudoku.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                # Try every number from 1 to 9
                for num in range(1, 10):
                    if solver.is_valid(board, row, col, num):
                        board[row][col] = num
                        # print(f"Placing {num} at ({row},{col})...")
                        if brute_force(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def main(board: list[list[int]]):
    print("Starting brute-force Sudoku solver...")
    start_time = time.time()
    if brute_force(board):
        end_time = time.time()
        print(f"Brute-force solving time: {end_time - start_time:.6f} seconds.")

        print(cli.format_board_ascii(board))
        print("Solution Found. Testing for accuracy...")
        if tests.is_board_solved(board):
            print("Solution is solved and legal.")
        else:
            print("Solution is not legal")
    else:
        print("No solution exists.")


if __name__ == "__main__":
    puzzle = cli.get_puzzle()
    board = solver.format_board(puzzle.board)
    main(board)
