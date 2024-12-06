import unittest
from unittest.mock import patch


import aigroupproject.cli as cli
import aigroupproject.main as main


class TestCliFunctions(unittest.TestCase):

    @patch("builtins.input", return_value="")
    def test_get_puzzle_empty_input(self):
        puzzle = cli.get_puzzle()
        # Check if the puzzle difficulty is set to 0.5 by default
        self.assertEqual(puzzle.difficulty, 0.5)

    @patch("builtins.input", side_effect=["", ""])
    def test_get_puzzle_custom_and_empty_difficulty(self):
        puzzle = cli.get_puzzle()

        # Check if the puzzle difficulty is set to 0.5 after two empty inputs
        self.assertEqual(puzzle.difficulty, 0.5)

    @patch("builtins.input", side_effect=["", ""])
    def test_main_runs(self):
        puzzle = cli.get_puzzle()
        main.main(puzzle)


if __name__ == "__main__":
    _ = unittest.main()
