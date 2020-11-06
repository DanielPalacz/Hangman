"""Hangman game implementation.

Usage:
    hangman.py -demo   - running Hangman game in Demo mode
"""

from inputimeout import inputimeout, TimeoutOccurred
import sys


class HangmanPlayer:
    """HangmanPlayer Class layer Doc-string"""

    def __init__(self, name):
        """Constructor for HangmanPlayer Class objects"""
        self.name = name

    def provide_character(self):
        """ ... """
        while True:
            char_input = ""
            try:
                char_input = inputimeout(prompt="\nProvide single character "
                                                "(in 5 seconds): ", timeout=5)
            except TimeoutOccurred:
                char_input = ""

            if len(char_input) == 1:
                break
            elif len(char_input) == 0:
                char_input = ""
                break
            else:
                print("Please enter only one character")
        return char_input

    def guess_word(self):
        """  ... """
        try:
            return inputimeout(prompt="\nGuess word in (in 10 seconds): ",
                               timeout=10)
        except TimeoutOccurred:
            return ""


class HangmanGame:
    """Summary of HangmanGame Class

    Longer class information....
    Longer class information....

    Attributes:
        guessed_word:
            - string contains word to be guessed
        guessing_state:
            - string contains state of Game
            - it is '***' if guessed_word is initialised as 'cat'
        last_character:
            - string indicates the latest input provided by User
            - it is always single character apart of situation when:
               User did not provide input then it is set by Game to "NULL"
        guessed_chars:
            - dictionary contains appearing the given characters or NULL
    """

    def __init__(self, guessed_word):
        """Initializes HangmanGame object

        Args:
            - guessed_word
        Returns:
            ...
        """
        self.guessed_word = guessed_word
        self.guessing_state = len(guessed_word) * "*"
        self.guessed_chars = {}

    def __str__(self):
        return "Hello it is __str__ (special method) output of: " \
               "SingleHangmanPlayer classes"

    def is_finished(self):
        test_table = [1 if c1 not in self.guessed_chars else 0 for c1 in
                      self.guessed_word]
        if sum(test_table) == 0:
            return True
        else:
            return False

    def update_game_state(self, character: str) -> None:
        """Updates game state.

        More method information...
        More method information...
        """

        if character not in self.guessed_chars.keys():
            self.guessed_chars[character] = 0
        self.guessed_chars[character] += 1

        self.guessing_state = "".join([c1 if c1 in self.guessed_chars else "*"
                                       for c1 in self.guessed_word])

    def run_game(self, player: HangmanPlayer) -> None:
        """Runs game.

        More method information...
        More method information...
        """

        print("""
        Hello in Hangman Game!
        """)
        print(self.is_finished())
        while not self.is_finished():
            print("The state of guessing is following:", self.guessing_state)
            self.update_game_state(player.provide_character())

            if self.is_finished():
                print("Super! You guessed the word:", self.guessed_word)
                print("\nIt is end of Hangman Game. Thank You!!!")
                break
            print("\nThe state of guessing is following:", self.guessing_state)

            guess_try = player.guess_word()
            if guess_try == self.guessed_word:
                print("Hurra you guessed. The word is:", guess_try)
                self.guessing_state = guess_try
                break
            else:
                print("\nUnfortunately you did not guess.\n\n")
        else:
            print("\nIt is end of Hangman Game. Thank You!!!")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        exit()
    elif "-demo" in sys.argv:
        janek = HangmanPlayer("Janek")
        game = HangmanGame("kot")
        game.run_game(janek)
        print("\nGame stats:\n", game.guessed_chars)
    else:
        print("\nThe given way of running Hangman game is not implemented")
