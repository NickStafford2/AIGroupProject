# tests.py
import argparse
import concurrent.futures
import random

from sudoku import Sudoku

import aigroupproject.cli as cli
import aigroupproject.sudoku_solver as solver


def get_random_board() -> list[list[int]]:
    while True:
        d = random.uniform(0, 1)
        if d > 0 and d < 1:
            x = Sudoku(3).difficulty(d).board
            return solver.format_board(x)


def test_single_board(board: list[list[int]]) -> bool:
    """Test a single sudoku board"""
    success = solver.solve_heuristics(board)
    if not success:
        print("Failed Test")
        print(cli.format_board_ascii(board))
        return False
    return True


def test_many_boards(epoch: int = 1000, parallel: bool = False):
    """Test multiple sudoku boards, optionally in parallel"""
    print(f"Testing {epoch} test boards")

    if parallel:
        # Create a ThreadPoolExecutor to run tests in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(epoch):
                if i % 100 == 0 and i != 0:
                    print(f"  {i} tests complete...")

                board = get_random_board()
                # Submit the test task to the executor
                futures.append(executor.submit(test_single_board, board))

            # Wait for all futures to complete and check results
            for future in concurrent.futures.as_completed(futures):
                if not future.result():
                    print("Test failed, stopping...")
                    return
    else:
        # Run tests sequentially if not in parallel
        for i in range(epoch):
            if i % 100 == 0 and i != 0:
                print(f"  {i} tests complete...")
            board = get_random_board()
            success = test_single_board(board)
            if not success:
                print("Test failed, stopping...")
                return

    print(f"Successfully passed {epoch} tests.")


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


def main():
    """Main function for parsing CLI arguments and running tests"""
    # Set up argparse to handle CLI arguments
    parser = argparse.ArgumentParser(description="Run multiple Sudoku tests.")

    # Add argument for epochs (number of test boards to run)
    parser.add_argument(
        "epochs",
        type=int,
        nargs="?",  # Make this argument optional
        default=1000,
        help="Number of test boards to run (default is 1000)",
    )

    # Add argument for parallel execution
    parser.add_argument(
        "-p",
        "--parallel",
        action="store_true",  # This flag doesn't need a value; it's a toggle
        help="Run the tests in parallel",
    )

    args = parser.parse_args()

    # Run tests with the number of epochs and parallelism option provided by the user
    test_many_boards(epoch=args.epochs, parallel=args.parallel)


if __name__ == "__main__":
    main()
