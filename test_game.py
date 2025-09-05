"""
test_game.py
Unit tests for HangmanGame class using unittest.
"""

import unittest
from game import HangmanGame
from word_api import WordAPI


class TestHangmanGame(unittest.TestCase):
    """Unit tests for HangmanGame."""

    def setUp(self):
        """Set up a game instance before each test."""
        self.api = WordAPI()
        self.game = HangmanGame(api=self.api, lives=6)

    def test_start_game_basic(self):
        """Test starting a game at basic level."""
        display = self.game.start_game(level="basic")
        self.assertIsInstance(display, str)
        self.assertTrue(len(display) > 0)
        self.assertTrue(all(c == "_" or not c.isalpha() for c in display))

    def test_start_game_intermediate(self):
        """Test starting a game at intermediate level."""
        display = self.game.start_game(level="intermediate")
        self.assertIsInstance(display, str)
        self.assertTrue(len(display) > 0)
        self.assertTrue(all(c == "_" or not c.isalpha() for c in display))

    def test_correct_guess(self):
        """Test guessing a correct letter."""
        self.game.start_game(level="basic")
        letter = self.game.word[0]  # take first letter from word
        status, _ = self.game.guess_letter(letter)
        self.assertEqual(status, "correct")

    def test_incorrect_guess(self):
        """Test guessing an incorrect letter."""
        self.game.start_game(level="basic")
        letter = "z"
        if letter in self.game.word.lower():
            self.skipTest("Word contains 'z', skipping test.")
        else:
            status, _ = self.game.guess_letter(letter)
            self.assertEqual(status, "incorrect")

    def test_is_won(self):
        """Test game win detection."""
        self.game.start_game(level="basic")
        for letter in set(self.game.word.lower()):
            self.game.guess_letter(letter)
        self.assertTrue(self.game.is_won())
        self.assertTrue(self.game.is_finished())

    def test_is_finished_on_lives_zero(self):
        """Test if game finishes when lives reach zero."""
        self.game.start_game(level="basic")
        self.game.lives = 1
        _, _ = self.game.guess_letter("z")
        self.assertTrue(self.game.is_finished())
        self.assertFalse(self.game.is_won())

    def test_invalid_input(self):
        """Test handling invalid guesses (non-letter or multiple letters)."""
        self.game.start_game(level="basic")
        for invalid in ["1", "@", "ab", ""]:
            status, _ = self.game.guess_letter(invalid)
            self.assertEqual(status, "invalid")

    def test_repeated_guess(self):
        """Test guessing the same letter twice."""
        self.game.start_game(level="basic")
        letter = self.game.word[0]
        status, _ = self.game.guess_letter(letter)
        self.assertEqual(status, "correct")
        status, _ = self.game.guess_letter(letter)  # guess same again
        self.assertEqual(status, "already")


if __name__ == "__main__":
    # verbosity=2 shows detailed output with test names
    unittest.main(verbosity=2)
