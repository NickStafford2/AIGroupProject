# lookup_table.py
import time
from copy import deepcopy
from typing import override

import cli
import sudoku_solver as solver
import tests


class State:
    table: list[list[set[int]]]
    is_set: list[list[bool]]

    def __init__(self, grid: list[list[int]]) -> None:
        self.table = []
        self.is_set = []
        for _ in range(9):
            row: list[set[int]] = []
            for _ in range(9):
                row.append(set(range(1, 10)))
            self.table.append(row)
            self.is_set.append([False] * 9)

        self.init_table(grid)

    def is_valid(self, row: int, col: int, num: int) -> bool:
        return not self.is_set[row][col] and num in self.table[row][col]

    def init_table(self, grid: list[list[int]]):
        for row in range(9):
            for col in range(9):
                cell = grid[row][col]
                if cell != 0:
                    self.constrain(row, col, cell)

    def constrain(self, row: int, col: int, val: int, verbose: bool = False):
        for i in range(9):
            self.table[row][i].discard(val)
            self.table[i][col].discard(val)

        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                self.table[i + start_row][j + start_col].discard(val)
        self.table[row][col] = set([val])
        self.is_set[row][col] = True
        if verbose:
            print(self)

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
            return sb

        width = 3
        height = 3
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


def most_constrained_variables(
    state: State,
) -> list[tuple[int, int, set[int]]]:
    tied_cells: list[tuple[int, int, set[int]]] = []
    min_valid_values = 10  # Start with a value larger than the max (9)

    for r in range(9):
        for c in range(9):
            if not state.is_set[r][c]:
                possible_values = state.table[r][c]
                new_min = len(possible_values)
                if new_min == min_valid_values:
                    # ties are allowed, if two cells are equally constrained
                    tied_cells.append((r, c, possible_values))
                elif new_min < min_valid_values:
                    min_valid_values = new_min
                    # remove old cells, since this cell is more constrined.
                    tied_cells = [(r, c, possible_values)]
    return tied_cells


def most_constraining_variable(
    state: State, tied_cells: list[tuple[int, int, set[int]]]
) -> tuple[int, int, set[int]]:
    """From a list of tied cells, find the cell that imposes the most constraints on its
    neighbors. if there is a tie, return random of the maxs"""
    max_constraints = -1
    most_constraining_cell = tied_cells[0]

    for r, c, s in tied_cells:
        constraints = 0
        possible_values: set[int] = state.table[r][c]

        # counting unassigned cells in the same row and column
        for i in range(9):
            for v in possible_values:
                if state.is_valid(r, i, v):
                    constraints += 1
                if state.is_valid(i, c, v):
                    constraints += 1

        # counting unassigned cells in the subgrid
        start_row, start_col = 3 * (r // 3), 3 * (c // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                for v in possible_values:
                    if state.is_valid(i, j, v):
                        constraints += 1

        # updating the most constraining variable
        if constraints > max_constraints:
            max_constraints = constraints
            most_constraining_cell = (r, c, s)

    return most_constraining_cell


def least_constraining_values(state: State, row: int, col: int) -> list[int]:
    """Get the possible values of a cell, ordered by their least constraining effect"""
    assert not state.is_set[row][col]
    candidates: list[tuple[int, int]] = []
    for num in state.table[row][col]:
        # counting how many other cells this value would restrict
        constraint_count = 0
        # A cell can not constrain itself so don't include it.
        rows = set(range(9))
        cols = set(range(9))
        rows.remove(col)
        cols.remove(row)

        for r in rows:
            if state.is_valid(r, col, num):
                constraint_count += 1
        for c in cols:
            if state.is_valid(row, c, num):
                constraint_count += 1

        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if state.is_valid(i + start_row, j + start_col, num):
                    constraint_count += 1

        candidates.append((num, constraint_count))

    # Sort by the number of constraints (ascending)
    candidates.sort(key=lambda x: x[1])
    return [x[0] for x in candidates]


def solve_heuristics_root(grid: list[list[int]]) -> State:
    state = State(grid)
    return solve_heuristics(state)


def solve_heuristics(state: State, depth: int = 0) -> State:
    tab = " " * depth
    # print(f"{tab}Depth={depth}")
    # Finding the most constrained variable(s)
    tied_cells: list[tuple[int, int, set[int]]] = most_constrained_variables(state)
    # print(f"{tab}{len(tied_cells)} most constrained = {tied_cells}")

    # If the board is solved
    if not tied_cells:
        return state

    # If there's a tie, use Most Constraining Variable to break it
    if len(tied_cells) > 1:
        # print(f"{tab}Tie found. find most constraining")
        row, col, values = most_constraining_variable(state, tied_cells)
    else:
        row, col, values = tied_cells[0]

    # print(f"{tab} most constraining = ({row},{col})={values}")
    # trying the least constraining values for the selected cell
    for num in least_constraining_values(state, row, col):
        # if not is_valid(look_ahead_table, row, col, num):
        #     print(f"can not add {num} at ({row},{col})")
        #     continue
        next_state = deepcopy(state)
        # print(f"Trying {num} at ({row}, {col})")
        next_state.constrain(row, col, num, False)
        if solve_heuristics(next_state, depth + 1):
            # print(f"{tab}Backtracking Success")
            return state

    # print(f"{tab}Backtracking Fail")
    return state


def main(board: list[list[int]]):
    start_time = time.time()
    solution = solve_heuristics_root(board)
    if solution:
        end_time = time.time()
        grid = solution.to_grid()
        print(f"Heuristic solving time: {end_time - start_time:.6f} seconds.")
        print("Solution Found. Testing for accuracy...")
        print(cli.format_board_ascii(grid))
        if tests.is_board_solved(grid):
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
