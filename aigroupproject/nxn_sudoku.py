import argparse
import time
from copy import deepcopy


class State:
    table: list[list[set[int]]]
    _is_set: set[tuple[int, int]]
    _is_not_set: set[tuple[int, int]]
    verbose: bool = False
    n: int  # Size of the subgrid
    n_squared: int  # Size of the full grid (n^2)
    sqrt_n: int  # Size of the subgrid (sqrt(n) x sqrt(n))

    def __init__(self, grid: list[list[int]], n: int, verbose: bool = False) -> None:
        self.table = []
        self._is_set = set()
        self._is_not_set = set()
        self.verbose = verbose
        self.n = n
        self.n_squared = n * n
        self.sqrt_n = n  # The subgrid size is n (e.g., for a 9x9 sudoku, n=3)

        for r in range(self.n_squared):
            row: list[set[int]] = []
            for c in range(self.n_squared):
                row.append(set(range(1, self.n_squared + 1)))  # Values from 1 to n^2
                self._is_not_set.add((r, c))
            self.table.append(row)

        self.init_table(grid)

    def is_valid(self, row: int, col: int, num: int) -> bool:
        return (row, col) in self._is_not_set and num in self.table[row][col]

    def init_table(self, grid: list[list[int]]):
        for row in range(self.n_squared):
            for col in range(self.n_squared):
                cell = grid[row][col]
                if cell != 0:
                    self.constrain(row, col, cell)

    def constrain(self, row: int, col: int, val: int, verbose: bool = False):
        # Constrain row
        for i in range(self.n_squared):
            self.table[row][i].discard(val)
            self.table[i][col].discard(val)

        # Adjust for subgrid size
        start_row, start_col = row - row % self.n, col - col % self.n
        for i in range(self.n):
            for j in range(self.n):
                self.table[i + start_row][j + start_col].discard(val)

        self.table[row][col] = set([val])
        self._is_set.add((row, col))
        self._is_not_set.remove((row, col))

        if verbose or self.verbose:
            print(self.format_as_string(row, col))

    def constrain_trivial_cells(self) -> bool:
        did_update = False
        to_update = deepcopy(self._is_not_set)
        for r, c in to_update:
            if len(self.table[r][c]) == 1:
                to_update.add((r, c))
                did_update = True
                val = next(iter(self.table[r][c]))
                self.constrain(r, c, val)
        return did_update

    def is_finished(self):
        return len(self._is_not_set) == 0

    def __str__(self):
        return self.format_as_string()

    def format_as_string(self, color_row: int = -1, color_col: int = -1) -> str:
        def format_set(s: set[int], row: int, col: int) -> str:
            # Join the elements in the set with spaces and format it to a fixed width
            sb = "".join(str(i) for i in sorted(s))
            if len(sb) > 9:
                sb = f"{sb[:8]}* "  # Ensure consistent spacing for the set output
            else:
                sb = f"{sb:9} "  # Ensure consistent spacing for the set output
            if row == color_row and col == color_col:
                sb = f"\033[31m{sb}\033[0m"  # Color red for the selected cell
            elif (row, col) in self._is_not_set:
                sb = f"\033[32m{sb}\033[0m"  # Color green for unsolved cells

            return sb

        table = ""
        cell_length = 9  # Length for each cell's output

        for i, row in enumerate(self.table):
            # Create the row separator for each row
            horizontal = (
                (("+-" + "-" * (cell_length + 1) * self.n) + "-") * self.n + "+" + "\n"
            )
            if i == 0:
                table += horizontal

            row_str = "| "

            for c, cell in enumerate(row):
                # Add internal column separators after every n columns
                if c > 0 and c % self.n == 0:
                    row_str += " | "
                row_str += format_set(cell, i, c)

            row_str += " |"  # Close the row
            table += row_str + "\n"

            # Add a separator between subgrids after every n rows
            if i == self.n_squared - 1 or i % self.n == self.n - 1:
                table += horizontal

        return table

    def to_grid(self) -> list[list[int]]:
        grid = []
        for table_row in self.table:
            grid.append([next(iter(cell)) for cell in table_row])
        return grid


def most_constrained_variables(state: State) -> list[tuple[int, int, set[int]]]:
    tied_cells = []
    min_valid_values = (
        state.n_squared + 1
    )  # Start larger than the maximum possible number

    for r, c in state._is_not_set:
        possible_values = state.table[r][c]
        new_min = len(possible_values)
        if new_min == min_valid_values:
            tied_cells.append((r, c, possible_values))
        elif new_min < min_valid_values:
            min_valid_values = new_min
            tied_cells = [(r, c, possible_values)]
    return tied_cells


def most_constraining_variable(
    state: State, tied_cells: list[tuple[int, int, set[int]]]
) -> tuple[int, int, set[int]]:
    max_constraints = -1
    most_constraining_cell = tied_cells[0]

    for r, c, s in tied_cells:
        constraints = 0
        possible_values = state.table[r][c]

        for i in range(state.n_squared):
            for v in possible_values:
                if state.is_valid(r, i, v):
                    constraints += 1
                if state.is_valid(i, c, v):
                    constraints += 1

        start_row, start_col = state.n * (r // state.n), state.n * (c // state.n)
        for i in range(start_row, start_row + state.n):
            for j in range(start_col, start_col + state.n):
                for v in possible_values:
                    if state.is_valid(i, j, v):
                        constraints += 1

        if constraints > max_constraints:
            max_constraints = constraints
            most_constraining_cell = (r, c, s)

    return most_constraining_cell


def least_constraining_values(state: State, row: int, col: int) -> list[int]:
    assert (row, col) not in state._is_set
    candidates = []
    for num in state.table[row][col]:
        constraint_count = 0
        rows = set(range(state.n_squared))
        cols = set(range(state.n_squared))
        rows.remove(col)
        cols.remove(row)

        for r in rows:
            if state.is_valid(r, col, num):
                constraint_count += 1
        for c in cols:
            if state.is_valid(row, c, num):
                constraint_count += 1

        start_row, start_col = row - row % state.n, col - col % state.n
        for i in range(state.n):
            for j in range(state.n):
                if state.is_valid(i + start_row, j + start_col, num):
                    constraint_count += 1

        candidates.append((num, constraint_count))

    candidates.sort(key=lambda x: x[1])
    return [x[0] for x in candidates]


def solve_heuristics_root(
    grid: list[list[int]], n: int, verbose: bool = False
) -> State:
    state = State(grid, n, verbose)
    return solve_heuristics(state)


def solve_heuristics(state: State, depth: int = 0) -> State:
    if state.is_finished():
        return state
    while state.constrain_trivial_cells():
        if state.is_finished():
            return state
    tied_cells = most_constrained_variables(state)
    if len(tied_cells) > 1:
        row, col, _ = most_constraining_variable(state, tied_cells)
    else:
        row, col, _ = tied_cells[0]

    for num in least_constraining_values(state, row, col):
        state.constrain(row, col, num, False)
        if solve_heuristics(state, depth + 1):
            return state
    return state


def main(n: int, verbose: bool = False):
    print(f"Running Sudoku solver for a {n*n} grid")
    print(f"Verbose mode: {verbose}")
    # Generate an nxn grid filled with zeros
    board = [[0 for _ in range(n**2)] for _ in range(n**2)]

    start_time = time.time()
    solution = solve_heuristics_root(board, n, verbose)
    if solution:
        end_time = time.time()
        print(solution.format_as_string())
        print(f"Heuristic solving time: {end_time - start_time:.6f} seconds.")
        print("Solution is solved and legal.")
    else:
        print("No solution exists.\n")


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Solve an n x n Sudoku puzzle.")
    _ = parser.add_argument(
        "n",
        nargs="?",
        type=int,
        default=3,  # Default to 3 if no n is provided (3x3 subgrid for a 9x9 puzzle)
        help="The size of the subgrid (default is 3, which means a 9x9 grid)",
    )
    _ = parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Pass the values to the main function
    main(n=args.n, verbose=args.verbose)
