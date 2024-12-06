from sudoku import Sudoku


def get_puzzle():
    if (
        input(
            "Do you want to enter custom sudoku board or automatically generated board?\n (press 'c' for custom): "
        )
        == "c"
    ):
        custom_grid = _get_custom_puzzle()
        return Sudoku(3, board=custom_grid)
    else:
        difficulty = _get_difficulty()
        return Sudoku(3).difficulty(difficulty)


def _get_custom_puzzle() -> list[list[int]]:
    print("Enter your custom Sudoku grid (row by row, 9 values per row):")
    grid: list[list[int]] = []
    for i in range(9):
        while True:
            try:
                user_input = input(
                    f"Enter row {i + 1} (comma-separated numbers, 0 for empty cells): "
                ).strip()
                delimeter = "," if "," in user_input else " "
                row = [int(num.strip()) for num in user_input.split(delimeter)]
                if len(row) != 9:
                    raise ValueError("Each row must have exactly 9 values.")
                grid.append(row)
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Try again.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Try again.")
    return grid


def _get_difficulty():
    while True:
        try:
            user_input = input(
                "What difficulty would you like the puzzle to be?(0-1): "
            )
            if user_input == "":
                return 0.5
            difficulty = float(user_input)
            if difficulty > 0 and difficulty < 1:
                return difficulty
            print("Difficulty must be between 0 and 1")
        except ValueError:
            print("Invalid input: Please enter a number between 0 and 1. Try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Try again.")
