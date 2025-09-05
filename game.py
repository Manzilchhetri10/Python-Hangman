"""
game.py
Defines HangmanGame class with game logic.
"""


class HangmanGame:
    """Core Hangman game logic with lives and hidden word tracking."""

    def __init__(self, api, lives=6, time_limit=15):
        self.api = api
        self.lives = lives
        self.time_limit = time_limit
        self.word = ""
        self.hidden_word = []
        self.guessed_letters = set()

    def start_game(self, level="basic"):
        """Start a game by selecting a word or phrase based on level."""
        if level == "intermediate":
            self.word = self.api.get_phrase()
        else:
            self.word = self.api.get_word()
        self.hidden_word = ["_" if c.isalpha() else c for c in self.word]
        self.guessed_letters.clear()
        return "".join(self.hidden_word)

    def guess_letter(self, letter):
        """Process a guessed letter."""
        if not letter.isalpha() or len(letter) != 1:
            return "invalid", "".join(self.hidden_word)
        letter = letter.lower()
        if letter in self.guessed_letters:
            return "already", "".join(self.hidden_word)
        self.guessed_letters.add(letter)
        if letter in self.word.lower():
            for i, c in enumerate(self.word):
                if c.lower() == letter:
                    self.hidden_word[i] = c
            return "correct", "".join(self.hidden_word)
        else:
            self.lives -= 1
            return "incorrect", "".join(self.hidden_word)

    def is_finished(self):
        """Check if the game is finished (won or lost)."""
        return self.lives <= 0 or "".join(self.hidden_word) == self.word

    def is_won(self):
        """Check if the player has won."""
        return "".join(self.hidden_word) == self.word

    def reveal_answer(self):
        """Reveal the answer."""
        return self.word
