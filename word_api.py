"""
word_api.py
Provides random words and phrases for the Hangman game.
"""

import random


class WordAPI:
    """API to fetch words and phrases for Hangman."""

    def __init__(self, words=None, phrases=None):
        self.words = words or ["apple", "banana", "kiwi"]
        self.phrases = phrases or ["unit test", "hello world"]

    def get_word(self):
        """Return a random word."""
        return random.choice(self.words)

    def get_phrase(self):
        """Return a random phrase."""
        return random.choice(self.phrases)
