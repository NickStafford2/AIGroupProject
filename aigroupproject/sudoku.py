from sudoku import Sudoku
import numpy as np
from sudoku_py import Sudoku as Sud

#Code to make a sudoku
#Have AI solve it
#board has to be board[col][row]
#this list(list()) is backwards
difficulty = float(input("What difficulty would you like the puzzle to be?[0-1]"))
puzzle = Sudoku(3).difficulty(.9)
puzzle.show()
solution = puzzle.solve()

print("This is the actual solution: ")
solution.show()
#print(type(puzzle))
#print(type(puzzle.board))

def find_list_of_board(grid):
    
    puzzle_cols = []
    for x in range(9):
        puzzle_string = []
        for i in range(9):
            elem = (grid[x][i])
            if elem == None:
                elem = 0
            puzzle_string.append(elem)
        #print(puzzle_string)
        puzzle_cols.append(puzzle_string)
    return puzzle_cols

board = find_list_of_board(puzzle.board)
# for list in board:
#     print(list)
string = find_list_of_board(solution.board)

def is_valid(board, row, col, num):
    for i in range(9):    # Check the row
        if board[row][i] == num:
            return False
    for i in range(9): # Check the column
        if board[i][col] == num:
            return False
    #start_row = row - row /3
    start_row = row - row % 3 #this is to check the 3x3 grid
    #print(start_row)
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            #print(board[i + start_row][j + start_col], num)
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve(board):
    # Find an empty cell
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0: 
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):#this is recursion for backtracking
                            return True
                        board[row][col] = 0  
                return False  
    return True  



# Solve the puzzle
if solve(board):
    #is_valid(board, 5, 2, 2)
    print("Solved Sudoku from AI:")
    # for row in board:
    #     print(row)
    result = Sud(board)
    print(result)
else:
    print("No solution exists.")
