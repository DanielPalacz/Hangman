"""Hangman game implementation.

(stand-alone program / module) - more DocString details - line_1
(stand-alone program / module) - more DocString details - line_2
...
(stand-alone program / module) - more DocString details - line_n
"""

from inputimeout import inputimeout, TimeoutOccurred
import sys


class HangmanGame():
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
        self.last_character = ""
        self.guessed_chars = {"NULL": 0}

    def __str__(self):
        return "Hello it is __str__ (special method) output of: " \
               "SingleHangmanPlayer classes"

    def update_game_state(self):
        """Updates game state.

        More method information...
        More method information...
        """

        if self.last_character not in self.guessed_chars.keys():
            self.guessed_chars[self.last_character] = 0
        self.guessed_chars[self.last_character] += 1

        if self.last_character in self.guessing_state:
            pass
        elif self.last_character in self.guessed_word:
            last_character_distribution_in_word = []
            temp = ''
            for elem in enumerate(self.guessed_word):
                if self.last_character == elem[1]:
                    last_character_distribution_in_word.append(elem[0])
            for elem in enumerate(self.guessing_state):
                if elem[0] in last_character_distribution_in_word:
                    temp = temp + self.last_character
                else:
                    temp = temp + elem[1]
            self.guessing_state = temp

    def run_game(self, player):
        """Runs game.

        More method information...
        More method information...
        """

        print("""
        Hello in Hangman Game!
        """)
        while self.guessed_word != self.guessing_state:
            print("The state of guessing is following:", self.guessing_state)
            self.last_character = player.provide_character()
            self.update_game_state()
            if self.guessing_state == self.guessed_word:
                print("Super! You guessed the word:", self.guessed_word)
                print("\nIt is end of Hangman Game. Thank You!!!")
                break
            print("\nThe state of guessing is following:", self.guessing_state)

            guess_try = player.guess_word()
            if guess_try == self.guessed_word:
                print("Hurra you guessed. The word is:", guess_try)
                self.guessing_state = guess_try
            elif not guess_try:
                pass
        else:
            print("\nIt is end of Hangman Game. Thank You!!!")

#    print(player1.__doc__)
#    print(player1)
#    print(SingleHangmanPlayer.__doc__)
#    print(player1.__init__.__doc__)


class HangmanPlayer():
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
                char_input = "NULL"
                break
            else:
                print("Please enter only one character")
        return char_input

    def guess_word(self):
        """  ... """
        guess_attempt = input("\nDo you want to guess the word? "
                              "Type word if 'Yes'. 'No', click enter. ")

        return guess_attempt


if __name__ == "__main__":
    if "-h" in sys.argv:
        print(__doc__)
        exit()

    janek = HangmanPlayer("Janek")
    game = HangmanGame("kot")
    game.run_game(janek)
    print("\nGame stats:\n", game.guessed_chars)
