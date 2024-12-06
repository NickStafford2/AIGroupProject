from flask import Blueprint, jsonify, request

bp = Blueprint("main", __name__)


@bp.route("/test", methods=["GET"])
def test():
    return "success"

# main.py
from sudoku_py import Sudoku as Sud
from sudoku import Sudoku
from sudoku_solver import find_list_of_board, solve

difficulty = float(input("What difficulty would you like the puzzle to be?[0-1]: "))
puzzle = Sudoku(3).difficulty(difficulty)
puzzle.show()
solution = puzzle.solve()

board = find_list_of_board(puzzle.board)
print("This is the actual solution: ")
solution.show()

if solve(board):
    print("Solved Sudoku from AI:")
    result = Sud(board)
    print(result)
else:
    print("No solution exists.")
