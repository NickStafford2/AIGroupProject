# tests.py
import argparse
import random
import time
from concurrent.futures import ProcessPoolExecutor

import brute_force as bf
import cli as cli
import lookup_table as tbl
import sudoku_solver as solver
from sudoku import Sudoku


def test_single_board(lookup_table: bool = False, brute_force: bool = False):
    """Test a single sudoku board."""
    board = get_random_board()
    if lookup_table:
        success = tbl.solve_heuristics_root(board)
    elif brute_force:
        success = bf.brute_force(board)
    else:
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


def run_single_test(lookup_table: bool = False, brute_force: bool = False):
    """Helper function to run a single test in parallel."""
    return test_single_board(lookup_table, brute_force)


def test_many_boards(
    epoch: int = 100,
    parallel: bool = False,
    lookup_table: bool = False,
    brute_force: bool = False,
    verbose: bool = False,
):
    """Run tests on multiple boards (batch)."""
    print(f"Testing {epoch} test batch")

    start_time = time.time()
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
            if verbose and i % 10 == 0 and i != 0:
                print(f"{i} tests complete...")
            if not test_single_board(lookup_table, brute_force):
                print("Test failed")
                break
        else:
            print(f"Successfully passed {epoch} tests.")
    end_time = time.time()
    print(f"Heuristic solving time: {end_time - start_time:.6f} seconds.")


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

    parser.add_argument(
        "-lt",
        "--lookup_table",
        action="store_true",  # This flag doesn't need a value; it's a toggle
        help="Run the tests with a lookup table",
    )
    parser.add_argument(
        "-bf",
        "--brute_force",
        action="store_true",  # This flag doesn't need a value; it's a toggle
        help="Run the tests with the brute force algorithm",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",  # This flag doesn't need a value; it's a toggle
        help="Print extra information to the console.",
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
    test_many_boards(
        epoch=args.epochs,
        parallel=args.parallel,
        lookup_table=args.lookup_table,
        brute_force=args.brute_force,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
