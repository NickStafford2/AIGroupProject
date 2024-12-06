from flask import Blueprint, jsonify, request

bp = Blueprint("main", __name__)


@bp.route("/test", methods=["GET"])
def test():
    return "success"

# main.py
from sudoku import Sudoku
from sudoku_solver import find_list_of_board, Sud, get_custom_puzzle, solve_heuristics, solve


# get the custom puzzle from the user
custom_grid = None
puzzle = None



if (input("Do you want to enter custom sudoku board or automatically generated board?\n (press 'c' for custom): ") == "c"):
    custom_grid = get_custom_puzzle()
    puzzle = Sudoku(3, board=custom_grid)
else:
    difficulty = float(input("What difficulty would you like the puzzle to be?[0-1]: "))
    puzzle = Sudoku(3).difficulty(difficulty)
    

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
