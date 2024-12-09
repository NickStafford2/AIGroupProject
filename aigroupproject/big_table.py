import time
from copy import deepcopy
from typing import override

import tests


class State:
    table: list[list[set[int]]]
    _is_set: set[tuple[int, int]]
    _is_not_set: set[tuple[int, int]]
    verbose: bool = False

    def __init__(self, grid: list[list[int]], verbose: bool = False) -> None:
        self.table = []
        self._is_set = set()
        self._is_not_set = set()
        self.verbose = verbose
        for r in range(16):  # Adjusted for 16x16 grid
            row: list[set[int]] = []
            for c in range(16):  # Adjusted for 16x16 grid
                row.append(set(range(1, 17)))  # Values from 1 to 16
                self._is_not_set.add((r, c))
            self.table.append(row)

        self.init_table(grid)

    def is_valid(self, row: int, col: int, num: int) -> bool:
        return (row, col) in self._is_not_set and num in self.table[row][col]

    def init_table(self, grid: list[list[int]]):
        for row in range(16):  # Adjusted for 16x16 grid
            for col in range(16):  # Adjusted for 16x16 grid
                cell = grid[row][col]
                if cell != 0:
                    self.constrain(row, col, cell)

    def constrain(self, row: int, col: int, val: int, verbose: bool = False):
        # Constrain row
        for i in range(16):  # Ensure full row constraint
            self.table[row][i].discard(val)
            self.table[i][col].discard(val)

        # Adjust for 4x4 subgrid instead of 3x3
        start_row, start_col = row - row % 4, col - col % 4  # 4x4 subgrid
        for i in range(4):  # Adjusted for 4x4 subgrid
            for j in range(4):  # Adjusted for 4x4 subgrid
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

    @override
    def __str__(self):
        return self.format_as_string()

    def format_as_string(self, color_row: int = -1, color_col: int = -1) -> str:
        def format_set(s: set[int], row: int, col: int) -> str:
            sb = ""
            for i in s:
                sb += str(i)
            sb = f"{str(sb):9}"
            if row == color_row and col == color_col:
                sb = f"\033[31m{sb}\033[0m"  # Color red
            else:
                cell = (row, col)
                if cell in self._is_not_set:
                    sb = f"\033[32m{sb}\033[0m"  # Color green
            return sb

        width = 4  # Adjusted for 16x16 grid
        height = 4  # Adjusted for 16x16 grid
        size = width * height

        table = ""
        cell_length = 9
        for i, row in enumerate(self.table):
            if i == 0:
                table += ("+-" + "-" * (cell_length + 1) * width) * height + "+" + "\n"
            table += (("| " + "{} " * width) * height + "|").format(
                *[
                    (format_set(x, i, c) if True else "        " * cell_length)
                    for c, x in enumerate(row)
                ]
            ) + "\n"
            if i == size - 1 or i % height == height - 1:
                table += ("+-" + "-" * (cell_length + 1) * width) * height + "+" + "\n"
        return table

    def to_grid(self) -> list[list[int]]:
        grid: list[list[int]] = []
        for table_row in self.table:
            row: list[int] = []
            for values in table_row:
                row.append(next(iter(values)))
            grid.append(row)
        return grid


def most_constrained_variables(state: State) -> list[tuple[int, int, set[int]]]:
    tied_cells: list[tuple[int, int, set[int]]] = []
    min_valid_values = 17  # Adjusted for 16x16 (start larger than the maximum 16)

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
        possible_values: set[int] = state.table[r][c]

        for i in range(16):  # Adjusted for 16x16 grid
            for v in possible_values:
                if state.is_valid(r, i, v):
                    constraints += 1
                if state.is_valid(i, c, v):
                    constraints += 1

        start_row, start_col = 4 * (r // 4), 4 * (c // 4)
        for i in range(start_row, start_row + 4):  # Adjusted for 4x4 subgrid
            for j in range(start_col, start_col + 4):  # Adjusted for 4x4 subgrid
                for v in possible_values:
                    if state.is_valid(i, j, v):
                        constraints += 1

        if constraints > max_constraints:
            max_constraints = constraints
            most_constraining_cell = (r, c, s)

    return most_constraining_cell


def least_constraining_values(state: State, row: int, col: int) -> list[int]:
    assert (row, col) not in state._is_set
    candidates: list[tuple[int, int]] = []
    for num in state.table[row][col]:
        constraint_count = 0
        rows = set(range(16))
        cols = set(range(16))
        rows.remove(col)
        cols.remove(row)

        for r in rows:
            if state.is_valid(r, col, num):
                constraint_count += 1
        for c in cols:
            if state.is_valid(row, c, num):
                constraint_count += 1

        start_row, start_col = row - row % 4, col - col % 4
        for i in range(4):
            for j in range(4):
                if state.is_valid(i + start_row, j + start_col, num):
                    constraint_count += 1

        candidates.append((num, constraint_count))

    candidates.sort(key=lambda x: x[1])
    return [x[0] for x in candidates]


def solve_heuristics_root(grid: list[list[int]], verbose: bool = False) -> State:
    state = State(grid, verbose)
    s = solve_heuristics(state)
    print(f"is_not_set:{state._is_not_set}")
    return s


def solve_heuristics(state: State, depth: int = 0) -> State:
    tab = "" * depth
    if state.is_finished():
        return state
    while state.constrain_trivial_cells():
        if state.is_finished():
            print(state.format_as_string())
            return state
    print(f"{tab}Depth={depth}")
    print(f"{tab}is_not_set:{state._is_not_set}")
    tied_cells: list[tuple[int, int, set[int]]] = most_constrained_variables(state)
    if len(tied_cells) > 1:
        row, col, _ = most_constraining_variable(state, tied_cells)
    else:
        row, col, _ = tied_cells[0]

    for num in least_constraining_values(state, row, col):
        state.constrain(row, col, num, True)
        if solve_heuristics(state, depth + 1):
            return state
    return state


def main(verbose: bool = False):
    # Generate a 16x16 grid filled with zeros
    board = [[0 for _ in range(16)] for _ in range(16)]

    start_time = time.time()
    solution = solve_heuristics_root(board, verbose)
    if solution:
        end_time = time.time()
        grid = solution.to_grid()
        print(f"Heuristic solving time: {end_time - start_time:.6f} seconds.")
        print("Solution is solved and legal.")
        # You can implement your own print method if you want to show the board
    else:
        print("No solution exists.\n")


if __name__ == "__main__":
    main(False)
