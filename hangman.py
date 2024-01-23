import random
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
    
class HangmanUI:
    def __init__(self):
        self.hangman = Hangman()
        self.ansi = Ansi()
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
        

    def draw_hangman(self):
        current_stage = min(self.hangman.incorrect_guesses, len(self.stages) - 1)
        print(self.stages[current_stage])

    def display_incorrect_char(self):
        return f"Incorrect guessed characters: {self.hangman.incorrect_guessed_chars}"

    # draws _ where character not guessed. puts correct guessed characters instead of _
    def draw_line(self):
        game_result = self.hangman.game_lost()
        for i in self.hangman.word:            
            if i in self.hangman.guessed_char:
                print(self.ansi.text_color(color=self.ansi.green, text=f"{i} "), end="")
            elif game_result:
                print(self.ansi.text_color(color=self.ansi.red, text=i,), end=" ")
            else:
                print(self.ansi.text_color(color=self.ansi.bright_cyan, text="_ "), end="")
            
        print()

    # Wrapper functions for class Hangman
    def split_user_guess(self, guess):
        self.hangman.split_user_guess(guess)

    def game_end(self):
        return self.hangman.game_end()
    
    def user_guess(self, guess):
        self.hangman.user_guess(guess)
    # Wrapper functions end


class Hangman:
    def __init__(self):
        self.files = FileHandler()
        self.ansi = Ansi()
        self.word = None
        self.char = set()
        self.guessed_char = []
        self.incorrect_guessed_chars = []
        self.incorrect_guesses = 0
        self.correct_guess = 0
        self.game_state = True
        self._random_word()
        
    # variable update
    def _update_guessed_chars(self, guessed_char):
        if not guessed_char in self.guessed_char:
            self.guessed_char.append(guessed_char)
            self.correct_guess += 1

    # Variable update
    def _update_incorrect_chars(self, guessed_char):
        if not guessed_char in self.incorrect_guessed_chars:
            self.incorrect_guessed_chars.append(guessed_char)
            self.incorrect_guesses += 1
        
    # reads words.txt
    def _get_data(self):
        return self.files.read_file(filename="words.txt")
    
    # splits word into characters
    def _letters_in_word(self):
        self.char = {char for char in self.word.strip()}

    # picks random word from words.txt
    def _random_word(self):
        data = self._get_data()
        word = random.choice(data)
        self.word = word.strip()
        self._letters_in_word()

    # reset game loop. else ends program
    def _restart(self):
        user = input(self.ansi.text_color(color=self.ansi.yellow, text="Restart? y/n: ")).lower()
        if user == 'y':
            print(self.ansi.reset_screen())
            self.correct_guess = 0
            self.incorrect_guesses = 0
            self.incorrect_guessed_chars = []
            self.guessed_char = []
            self._random_word()
            self.game_state = True
        else:
            print(self.ansi.reset_screen())
            self.game_state = False
    
    # checks if user guess is correct or not
    def user_guess(self, guess):
        if guess in self.char:
            self._update_guessed_chars(guess)
        elif not guess in self.char:
            self._update_incorrect_chars(guess)
    
    # splits user string input into char.
    def split_user_guess(self, guess):
        for char in guess:
            self.user_guess(char)

    def game_lost(self):
        return self.incorrect_guesses >= 7
    
    def game_won(self):
        return self.correct_guess == len(self.char)

    # game over / victory evaluation (defeat based on amount of img in stages list)
    def game_end(self):
        if self.game_lost():
            print(self.ansi.text_color(color=self.ansi.red, text="Game Over!"))
            self._restart()
        elif self.game_won():
            print(self.ansi.text_color(color=self.ansi.green, text="Victory!"))
            self._restart()
        else:
            return self.game_state

# main program loop
if __name__ == "__main__":
    hangmanui = HangmanUI()
    
    while hangmanui.hangman.game_state:
        print(hangmanui.display_incorrect_char())
        hangmanui.draw_hangman()
        hangmanui.draw_line()
        if hangmanui.game_end():
            user_guess = input(hangmanui.ansi.text_color(color=hangmanui.ansi.bright_cyan, text="Enter Guess: ")).lower()
            
            if len(user_guess) > 1:
                hangmanui.split_user_guess(user_guess)
            else:
                hangmanui.user_guess(user_guess)

            print(hangmanui.ansi.reset_screen())