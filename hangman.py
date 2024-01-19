import random
import time

class FileHandler:
    # read and return data from file
    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                file_data = file.readlines()
                return file_data
        except PermissionError as e:
            print(f"Permission Error: {e}")
        except IOError as e:
            print(f"I/O Error: {e}")

# Holds ansi codes
class Ansi:
    def __init__(self):
        self.red = '\033[31m'
        self.green = '\033[32m'
        self.yellow = '\033[33m'
        self.blue = '\033[34m'
        self.magenta = '\033[35m'
        self.cyan = '\033[36m'
        self.white = '\033[37m'
        self.bright_blue = '\033[94m'
        self.bright_cyan = '\033[96m'
        self.reset_color = '\033[0m'
        self.clear_screen = '\033[2J\033[H'

    # called to change text to color declared in __init__
    def text_color(self, color, text):
        return f"{color}{text}{self.reset_color}"
    
    def reset_screen(self):
        return f"{self.clear_screen}"

class Hangman:
    def __init__(self):
        self.files = FileHandler()
        self.ansi = Ansi()
        self.word = None
        self.char = []
        self.guessed_char = []
        self.incorrect_guessed_chars = []
        self.incorrect_guesses = 0
        self.correct_guess = 0
        self.game_state = True
        self._random_word()
        self.stages = [
            """
            -----
            |   |
            |
            |
            |
            |
           ---
            """,
            """
            -----
            |   |
            |   O
            |
            |
            |
           ---
            """,
            """
            -----
            |   |
            |   O
            |   |
            |
            |
           ---
            """,
            """
            -----
            |   |
            |   O
            |  /|
            |
            |
           ---
            """,
            """
            -----
            |   |
            |   O
            |  /|\\
            |
            |
           ---
            """,
            """
            -----
            |   |
            |   O
            |  /|\\
            |  /
            |
           ---
            """,
            """
            -----
            |   |
            |   O
            |  /|\\
            |  / \\
            |
           ---
            """,
        ]

    # variable update
    def _update_guessed_chars(self, guessed_char):
        if not guessed_char in self.guessed_char:
            self.guessed_char.append(guessed_char)
            self.correct_guess += 1

    # Variable update
    def _update_incorrect_chars(self, guessed_char):
        self.incorrect_guessed_chars.append(guessed_char)
        self.incorrect_guesses += 1
    
    # reads words.txt
    def _get_data(self):
        return self.files.read_file(filename="words.txt")
    
    # splits word into characters
    def _letters_in_word(self):
        self.char = [char for char in self.word.strip()]

    # picks random word from words.txt
    def _random_word(self):
        data = self._get_data()
        word = random.choice(data)
        self.word = word
        self._letters_in_word()

    # reset game loop. else ends program
    def _restart(self):
        usr = input(self.ansi.text_color(color=self.ansi.yellow, text="Restart? y/n: ")).lower()
        #usr = input("Restart? ").lower()
        if usr == 'y':
            self.correct_guess = 0
            self.incorrect_guesses = 0
            self.incorrect_guessed_chars = []
            self.guessed_char = []
            self._random_word()
            self.game_state = True
        else:
            self.game_state = False

    def draw_hangman(self):
        current_stage = min(self.incorrect_guesses, len(self.stages) - 1)
        print(self.stages[current_stage])

    # draws _ where character not guessed. puts correct guessed characters instead of _
    def draw_line(self):
        for i in self.char:
            if i in self.guessed_char:
                print(self.ansi.text_color(color=self.ansi.green, text=f"{i} "), end="")
            else:
                print(self.ansi.text_color(color=self.ansi.bright_cyan, text="_ "), end="")
        print()
    
    # checks if user guess is correct or not
    def usr_guess(self, guess):
        if guess in self.char:
            print(self.ansi.text_color(color=self.ansi.green, text=f"{guess} is correct"))
            self._update_guessed_chars(guess)
            # time.sleep(1)
            # print(self.ansi.clear_screen)
        elif not guess in self.char:
            print(self.ansi.text_color(color=self.ansi.red, text=f"{guess} is not correct"))
            self._update_incorrect_chars(guess)
            # time.sleep(1)
            # print(self.ansi.clear_screen)
    
    # splits user string input into char.
    def split_user_guess(self, guess):
        for char in guess:
            self.usr_guess(char)

    # game over / victory evaluation (defeat based on img in stages list)
    def game_end(self):
        if self.incorrect_guesses >= 7:
            print(self.ansi.text_color(color=self.ansi.red, text="Game Over!"))
            self._restart()
        elif self.correct_guess == len(self.char):
            print(self.ansi.text_color(color=self.ansi.green, text="Victory!"))
            self._restart()
        else:
            return self.game_state

# main program loop
if __name__ == "__main__":
    hangman = Hangman()

    while hangman.game_state:
        hangman.draw_hangman()
        hangman.draw_line()
        
        user_guess = input(hangman.ansi.text_color(color=hangman.ansi.bright_cyan, text="Enter Guess: "))
        if len(user_guess) > 1:
            hangman.split_user_guess(user_guess)
            hangman.game_end()
        else:
            hangman.usr_guess(user_guess)
            hangman.game_end()
    

