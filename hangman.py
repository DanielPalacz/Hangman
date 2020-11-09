"""Hangman game documentation.

Usage:
    hangman.py -demo
      - run Hangman game in Demo mode

    hangman.py -history
      - show all historical results

    hangman.py -p John
    hangman.py --player John
      - run Hangman game with single player 'John'

    hangman.py -p John -p Tom
      - run Hangman game with two players 'John' and 'Tom'
"""

from inputimeout import inputimeout, TimeoutOccurred
import sys
import argparse
from dbsupport import GameDbInterface as db


class HangmanPlayer:
    """HangmanPlayer Class implementation.

    Attributes:
        name:
            - name of the player
    """

    def __init__(self, name: str) -> None:
        """Inits HangmanPlayer object."""
        self.name = name

    def provide_character(self):
        """Implements providing character by the player.

        Player has 5 seconds to provide character.
        """
        while True:
            try:
                char_input = inputimeout(prompt="\nProvide single character "
                                                "(in 5 seconds): ", timeout=5)
            except TimeoutOccurred:
                return None

            if len(char_input) == 1:
                break
            else:
                print("Please enter only one character")

        return char_input

    def guess_word(self):
        """Implements guessing word by the player.

        Player has 10 seconds to guess the word.
        """
        try:
            return inputimeout(prompt="\nGuess word in (in 10 seconds): ",
                               timeout=10)
        except TimeoutOccurred:
            return ""


class HangmanGame:
    """HangmanGame Class implementation.

    Implements Hangman-like game, based only on guessing the word.
    Attributes:
        guessed_word:
            - string contains word to be guessed
        guessing_state:
            - string contains state of Game
            - it is '***' if guessed_word is initialised as 'cat'
        guessed_chars:
            - dictionary contains appearing the given characters or NULL
        players:
            - list with players (objects of HangmanPlayer)
        winner:
            - name of player who won the game
        round_number:
            - number tracking rounds of the game
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
        self.results = {gamer: dict() for gamer in gamers}

    def __str__(self):
        return "Hello it is __str__ (special method) output of: " \
               "SingleHangmanPlayer classes"

    def is_finished(self):
        """Check if the game is finished."""
        test_table = [1 if c1 not in self.guessed_chars else 0 for c1 in
                      self.guessed_word]
        if sum(test_table) == 0:
            return True
        elif self.guessing_state == self.guessed_word:
            return True
        else:
            return False

    def update_game_state(self, character: str) -> None:
        """Updates game state."""

        if character not in self.guessed_chars.keys():
            self.guessed_chars[character] = 0
        self.guessed_chars[character] += 1

        self.guessing_state = "".join([c1 if c1 in self.guessed_chars else "*"
                                       for c1 in self.guessed_word])

    def end_game(self, the_player):
        print("Super!", the_player, "- you guessed the word:",
              self.guessed_word)
        self.guessing_state = self.guessed_word
        self.winner = the_player
        self.round_number += 1
        self.results[the_player][self.round_number] = self.guessed_word

    def run_game(self):
        """Runs Hangman game."""

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
                    self.end_game(player.name)
                    break

                print("\nThe state of game is following:", self.guessing_state)
                guess_try = player.guess_word()
                if guess_try == self.guessed_word:
                    self.end_game(player.name)
                    break
                else:
                    print("\nUnfortunately you did not guess.\n\n")

                self.round_number += 1
                self.results[player.name][self.round_number] = guess_try

        else:
            print("\nIt is end of Hangman Game number XYZ. "
                  "Thank You!", self.winner, "won in round", self.round_number)

    def get_game_stats(self):
        return self.results


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        exit()
    elif "-demo" in sys.argv and len(sys.argv) == 2:
        gamers = ["Janek", "Tomek"]
        game = HangmanGame("kot", *gamers)
        game.run_game()
        print("\nGame stats:\n", game.guessed_chars)
        exit()
    elif "-history" in sys.argv and len(sys.argv) == 2:
        db.show_all_rows("hangmandb.sqlite")
    elif ("-h" or "--help" in sys.argv) and len(sys.argv) == 2:
        print(__doc__)
        exit()
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--player", action="append", default=[])
        args = parser.parse_args()

        db.initialise_db("hangmandb.sqlite")
        game = HangmanGame("kot", *args.player)
        game.run_game()

        last_game_num = db.take_last_game_number("hangmandb.sqlite")
        game_stats = game.get_game_stats()

        for player in args.player:
            for game_round in game_stats[player].keys():
                if game_stats[player][game_round] != game.guessed_word:
                    winner = None
                else:
                    winner = game.winner
                db.update_db("hangmandb.sqlite",
                             last_game_num + 1,
                             winner=winner,
                             round_it=game_round,
                             name=player,
                             guess=game_stats[player][game_round]
                             )
