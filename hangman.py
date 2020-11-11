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
import time
import argparse
import db
import sqlite3


class HangmanPlayer:
    """HangmanPlayer Class implementation.

    Attributes:
        name:
            - name of the player
    """

    def __init__(self, name: str):
        """Inits HangmanPlayer object."""
        self.name = name

    def provide_character(self) -> str:
        """Implements providing character by the player.

        Player has 5 seconds to provide character.
        """
        t_start = time.time()
        t_delta = 0
        while True:
            t = 5 - t_delta
            try:
                char_input = inputimeout(prompt="\nProvide single character "
                                                "(in 5 seconds): ", timeout=t)
            except TimeoutOccurred:
                return ""

            if len(char_input) == 1:
                break
            else:
                print("Please enter one character.")

            t_end = time.time()
            t_delta = t_end - t_start

        return char_input

    def guess_word(self) -> str:
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

    def __init__(self, guessed_word: str, *gamers: HangmanPlayer):
        """Initializes HangmanGame object.

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

    def end_game(self, the_player, storage):
        print("Super!", the_player, "- you guessed the word:",
              self.guessed_word)
        self.guessing_state = self.guessed_word
        self.winner = the_player
        self.round_number += 1
        storage.update_game_actions_storage(the_player,
                                            self.round_number,
                                            self.guessed_word)

    def run_game(self, storage):
        """Runs Hangman game."""

        print("***********************************************************\n")
        print(*[x.name for x in self.players], "- Hello in Hangman Game!\n\n")

        while not self.is_finished():

            for player_obj in self.players:
                if self.is_finished():
                    break
                print("\n" + player_obj.name, "- it is your turn.")
                print("The state of game is following:", self.guessing_state)

                self.update_game_state(player_obj.provide_character())
                if self.is_finished():
                    self.end_game(player_obj.name, storage)
                    break

                print("\nThe state of game is following:", self.guessing_state)
                guess_try = player_obj.guess_word()
                if guess_try == self.guessed_word:
                    self.end_game(player_obj.name, storage)
                    break
                else:
                    print("\nUnfortunately you did not guess.\n\n")

                self.round_number += 1
                storage.update_game_actions_storage(player_obj.name,
                                                    self.round_number,
                                                    guess_try)
        else:
            print("\nIt is end of Hangman Game number XYZ. "
                  "Thank You!", self.winner, "won in round", self.round_number)


class GameActionsStorage:
    """Class implements storing/getting all game actions.

    Attributes:
        storage:
            - data structure stores all game actions.
              It is done by by executing the Class method:
              update_game_actions_storage(...)

    Methods:
        update_game_actions_storage(self, gamer, round_id, guess_try)
             - Method stores input for the given round of game.
        """

    def __init__(self, *gamers):
        self.storage = {gamer: dict() for gamer in gamers}

    def update_game_actions_storage(self, gamer, round_id, guess_try):
        self.storage[gamer][round_id] = guess_try

    def get_all_game_actions(self):
        return self.storage


if __name__ == "__main__":
    # Setting-up script input parameters
    parser = argparse.ArgumentParser(description="Hangman Game edu project.")
    parser.add_argument("-p", "--player", action="append", default=[],
                        help="Create Hangman Player")
    parser.add_argument("--history", action="store_true",
                        help="show all historical results")
    parser.add_argument("--documentation", action="store_true",
                        help="show module documentation")
    parser.add_argument("--nodb", action="store_true",
                        help="Game results are not written to db")
    parser.add_argument("--dbname", default="hangmandb",
                        help="defines Sqlite3 file DB to store game actions")
    args = parser.parse_args()

    # Additional printing documentation feature:
    if args.documentation:
        print(__doc__)
        exit()

    # Initial players check:
    if not args.player:
        print("You havent`t specified any player.\n")
        answer = input("Would like to play in single mode as John? "
                       "Type 'ok' if yes. ")
        if answer == "ok":
            args.player.append("John")
        else:
            print("You don`t want to play as 'John'. Quitting...")
            exit()

    # DB related Objects initializing
    if args.nodb:
        dbname = ":memory:"
    else:
        dbname = args.dbname + ".sqlite"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    db.initialize_db(c)

    # Game related Objects initializing, triggering the game
    game_actions_storage = GameActionsStorage(*args.player)
    game = HangmanGame("kot", *args.player)
    game.run_game(game_actions_storage)

    # when game is ended:
    game_actions = game_actions_storage.get_all_game_actions()
    # getting all game actions data structure
    last_game_id = db.get_last_game_id(c)
    # getting last game_id from db
    # ??? it is conceptual issue, because game_id depend on DBNAME
    # ??? it doesnt have have sense when we use more than 1 db.
    # --- > lets omit this "issue" for now

    for player in args.player:
        for game_round in game_actions[player].keys():
            if game_actions[player][game_round] != game.guessed_word:
                winner = None
            else:
                winner = game.winner
            db.update_db(c,
                         last_game_id + 1,
                         winner=winner,
                         game_round_id=game_round,
                         name=player,
                         guess=game_actions[player][game_round]
                         )
    conn.commit()
    conn.close()
