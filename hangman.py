"""Hangman game documentation.

Usage:
    hangman.py -demo   - run Hangman game in Demo mode

    hangman.py -p John
    hangman.py --player John
      - run Hangman game with single player 'John'

    hangman.py -p John -p Tom
      - run Hangman game with two players 'John' and 'Tom'
"""

from inputimeout import inputimeout, TimeoutOccurred
import sys
import argparse


class HangmanPlayer:
    """HangmanPlayer Class layer Doc-string"""

    def __init__(self, name):
        """Constructor for HangmanPlayer Class objects"""
        self.name = name

    def provide_character(self):
        """ ... """
        while True:
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

    def __init__(self, guessed_word, *gamers):
        """Initializes HangmanGame object

        Args:
            - guessed_word
        Returns:
            ...
        """
        self.guessed_word = guessed_word
        self.guessing_state = len(guessed_word) * "*"
        self.guessed_chars = {}
        self.players = [HangmanPlayer(gamer) for gamer in gamers]
        self.winner = None
        self.round_number = 0

    def __str__(self):
        return "Hello it is __str__ (special method) output of: " \
               "SingleHangmanPlayer classes"

    def is_finished(self):
        test_table = [1 if c1 not in self.guessed_chars else 0 for c1 in
                      self.guessed_word]
        if sum(test_table) == 0:
            return True
        elif self.guessing_state == self.guessed_word:
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

    def run_game(self):
        """Runs Hangman game.

        More information...
        """
        print("***********************************************************\n")
        print(*[x.name for x in self.players], "- Hello in Hangman Game!\n\n")

        while not self.is_finished():

            for player in self.players:
                if self.is_finished():
                    break
                print("\n" + player.name, "- it is your turn.")
                print("The state of game is following:", self.guessing_state)

                self.update_game_state(player.provide_character())
                if self.is_finished():
                    print("Super!", player.name, "- you guessed the word:",
                          self.guessed_word)
                    self.winner = player.name
                    break
                print("\nThe state of guessing is following:",
                      self.guessing_state)

                guess_try = player.guess_word()
                if guess_try == self.guessed_word:
                    print("Hurra", player.name,
                          "you guessed. The word is:", guess_try)
                    self.guessing_state = guess_try
                    self.winner = player.name
                    break
                else:
                    print("\nUnfortunately you did not guess.\n\n")

            self.round_number += 1

        else:
            print("\nIt is end of Hangman Game number XYZ. "
                  "Thank You!", self.winner, "won in round:", self.round_number)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        exit()
    elif len(sys.argv) == 2 and ("-h" or "--help" in sys.argv):
        print(__doc__)
        exit()
    elif "-demo" in sys.argv and len(sys.argv) == 2:
        gamers = ["Janek", "Tomek"]
        game = HangmanGame("kot", *gamers)
        game.run_game()
        print("\nGame stats:\n", game.guessed_chars)
        exit()
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--player",
                        action="append",
                        default=[])
        args = parser.parse_args()
        game = HangmanGame("kot", *args.player)
        game.run_game()
        print("\nGame stats:\n", game.guessed_chars)
