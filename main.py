"""
main.py
Run Hangman game with timed input and word API.
"""

import time
import sys
import threading
from typing import Optional
from game import HangmanGame
from word_api import WordAPI


def timed_input(prompt: str, timeout: int = 15) -> Optional[str]:
    """
    Ask player for input with visible countdown timer.

    Returns:
        str: input string if entered before timeout
        None: if timeout expires
    """
    print(prompt)
    buf = []
    start = time.time()
    done = threading.Event()

    def read_input():
        user_input = sys.stdin.readline().rstrip("\n")
        buf.append(user_input)
        done.set()

    # Start input thread
    t = threading.Thread(target=read_input, daemon=True)
    t.start()

    while not done.is_set():
        remaining = int(timeout - (time.time() - start))
        if remaining < 0:
            print("\n⏰ Time's up!")
            return None
        # Show countdown
        print(
            f"\r⏰ Time left: {remaining:2d}s | "
            f"Your input: {''.join(buf)}",
            end="",
            flush=True,
        )
        time.sleep(1)

    print()  # move to next line after input
    return buf[0] if buf else None


def main():
    """Main function to run Hangman game."""
    api = WordAPI()
    game = HangmanGame(api=api, lives=6)
    print("🎮 Welcome to Hangman!")

    level = input(
        "Choose level (basic / intermediate): "
    ).strip().lower() or "basic"

    display = game.start_game(level)
    print("Word:", display)

    while not game.is_finished():
        print(f"\nLives left: {game.lives}")
        print("Current word:", "".join(game.hidden_word))

        # Use timed_input instead of plain input
        guess = timed_input(
            "\nEnter a letter (or 'quit' to stop): ",
            timeout=game.time_limit,
        )

        if guess is None:  # timeout
            game.lives -= 1
            print("⏰ Timeout! You lost a life.")
            continue

        guess = guess.strip().lower()
        if guess == "quit":
            print("Game over. The word was:", game.reveal_answer())
            break

        status, display = game.guess_letter(guess)
        if status == "correct":
            print("✅ Correct!")
        elif status == "incorrect":
            print("❌ Wrong!")
        elif status == "invalid":
            print("⚠️ Invalid input!")
        elif status == "already":
            print("↩️ Already guessed!")

        print("Word:", display)

    if game.is_won():
        print("\n🎉 Congratulations! You guessed it:", game.word)
    elif game.lives <= 0:
        print("\n💀 You lost. The word was:", game.reveal_answer())


if __name__ == "__main__":
    main()
