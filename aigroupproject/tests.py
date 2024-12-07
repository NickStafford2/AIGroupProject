# tests.py
import argparse
from concurrent.futures import ProcessPoolExecutor
import random

from sudoku import Sudoku

import aigroupproject.cli as cli
import aigroupproject.sudoku_solver as solver


def test_single_board():
    """Test a single sudoku board."""
    board = get_random_board()
    success = solver.solve_heuristics(board)
    if not success:
        print("Failed Test")
        print(cli.format_board_ascii(board))
        return False
    return True


def get_random_board() -> list[list[int]]:
    """Generate a random board."""
    d = random.uniform(0, 1)
    x = Sudoku(3).difficulty(d).board
    return solver.format_board(x)


def test_batch(epoch: int = 100, parallel: bool = False):
    """Run tests on multiple boards (batch)."""
    print(f"Testing {epoch} test boards")

    if parallel:
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(run_single_test, range(epoch)))
        failed_tests = sum(1 for result in results if not result)
        if failed_tests > 0:
            print(f"Tests failed: {failed_tests}")
        else:
            print(f"Successfully passed {epoch} tests.")
    else:
        for i in range(epoch):
            if i % 10 == 0 and i != 0:
                print(f"{i} tests complete...")
            if not test_single_board():
                print("Test failed")
                break
        else:
            print(f"Successfully passed {epoch} tests.")


def run_single_test(_):
    """Helper function to run a single test in parallel."""
    return test_single_board()


def test_many_boards(epoch: int = 100, parallel: bool = False):
    """Run tests on multiple boards (batch)."""
    print(f"Testing {epoch} test boards")

    if parallel:
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(run_single_test, range(epoch)))
        failed_tests = sum(1 for result in results if not result)
        if failed_tests > 0:
            print(f"Tests failed: {failed_tests}")
        else:
            print(f"Successfully passed {epoch} tests.")
    else:
        for i in range(epoch):
            if i % 10 == 0 and i != 0:
                print(f"{i} tests complete...")
            if not test_single_board():
                print("Test failed")
                break
        else:
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
