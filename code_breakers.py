"""
Author: Ben Neeb, neebb@purdue.edu
Code Breakers
Date: 4/8/2024

Description:
    Program that plays code breakers with a user. The user interfaces with the program through menu options and the keyboard.

"""

import random, re, pathlib, os, datetime, numpy as np

class Game:

    def __init__(self, code, gameboard, clues, guess_ctr):
        self.code = code
        self.gameboard = gameboard
        self.clues = clues
        self.length = len(code)
        self.guess_ctr = guess_ctr

    def print(self, won):
        # Print the top line
        print('+', end='')
        print('-' * 18, end='')
        print('+-----+')

        # Print line 2
        print('|', end='')

        if won:
            # Print line 2 (for won)
            for i in self.code:
                print(' ' + i + ' ', end='')
            
            # Print remaining o chars if code isn't 6 digits
            for i in range(6 - len(self.code)):
                print(' o ', end='')
        else:
            # Print line 2 (for not won)
            print(' o ' * 6, end='')

        print('| R W |')

        # Print line 3
        print('+', end='')
        print('-' * 18, end='')
        print('+-----+')

        # Print 2d array for gameboard
        for i in reversed(range(10)):
            print('|', end='')
            
            for j in self.gameboard[i]:
                print(' ' + j + ' ',end='')

            print('|', end='')

            for j in self.clues[i]:
                print(' ' + str(j),end='')

            print(' |')

        # Print the last line
        print('+', end='')
        print('-' * 18, end='')
        print('+-----+')

def print_rules():
    print("\nCode Breakers Rules:")
    print("1. You get 10 guesses to break the lock.")
    print("2. Guess the correct code to win the game.")
    print("3. Codes can be either 4, 5, or 6 digits in length.")
    print("4. Codes can only contain digits 0, 1, 2, 3, 4, and 5.")
    print("5. Clues for each guess are given by a number of red and white pins.")
    print("   a. The number of red pins in the R column indicates the number of digits\n      in the correct location.")
    print("   b. The number of white pins in the W column indicates the number of\n      digits in the code, but in the wrong location.")
    print("   c. Each digit of the solution code or guess is only counted once in the\n      red or white pins.\n")


def generate_solution(min, max):
    # Code only contains the digits 0 through 5
    code_length = random.randint(min, max)
    code_str = ""

    # Loop through and make each digit
    for i in range(code_length):
        # Generate random number from 0 to 5
        n = random.randint(0, 5)

        # Append to code string
        code_str += str(n)

    # Return solution code as string
    return code_str


def play_game(game):
    # Print the gameboard
    game.print(False)

    while True:
        # Prompt user for next guess
        guess = input("What is your guess (q to quit, wq to save and quit): ")

        if guess.lower() == 'q':
            # Quit to menu without saving
            print("Ending Game.")
            break
        elif guess.lower() == 'wq':
            # Quit to menu with saving
            if save_game(game):
                print("Ending Game.")
                break
            else:
                print("cancelled")
                # Print the gameboard
                game.print(False)

        elif re.match(r'^\d{4,6}$', guess):
            # Only digits and correct length, now check for correct digits (0 - 5)
            if re.match(r'^[0-5]+$', guess):
                # Valid guess, continue
                if(check_guess(game, guess)):
                    # Print the ending game board
                    game.print(True)

                    # Announce win
                    print("Congratulations, you broke the lock!")
                    print("The grades are safe!")

                    break
                else:
                    # Increment counter
                    game.guess_ctr += 1

                    # Check if the user used all their tries
                    if game.guess_ctr >= 10:
                        # Print the ending game board
                        game.print(True)

                        print("You hear a machine yell OUT OF TRIES!")
                        print("  ...")
                        print("Is that burning you smell?")
                        print("  ...")
                        print("OH, NO! It looks like IU has destroyed all the EBEC grades!\n")
                        break
                    else:
                        # Print the game board
                        game.print(False)
            else:
                print("Your guess was \"" + guess + "\". It must be only numbers 0 through 5.")
        elif (re.match(r'^\d+$', guess) and len(guess) < 4) or guess == '':
            # All digits, but not long enough guess
            print("Your guess was \"" + guess + "\". This is too short.")
            print("Guess lengths must be between 4 and 6.")
        elif re.match(r'^\d+$', guess) and len(guess) > 6:
            # All digits, but too long of a guess
            print("Your guess was \"" + guess + "\". This is too long.")
            print("Guess lengths must be between 4 and 6.")
        else:
            # Contains a character that isn't a digit
            print("Your guess was \"" + guess + "\". It must be only numbers!")


def check_guess(game, guess):    
    # Pin counters
    red = 0
    white = 0

    # Update gameboard array
    for i in range(6):
        if i < len(guess):
            # Update gameboard array
            game.gameboard[game.guess_ctr][i] = guess[i]
        else:
            game.gameboard[game.guess_ctr][i] = 'o'

    # Determine bigger of two strings
    if len(game.code) > len(guess):
        bigger_str = game.code
        smaller_str = guess
    else:
        bigger_str = guess
        smaller_str = game.code

    # Get red pins    
    for i in range(len(smaller_str)):
        if smaller_str[i] == bigger_str[i]:
            red += 1

            smaller_str = smaller_str.replace(smaller_str[i], ' ', 1)
            bigger_str = bigger_str.replace(bigger_str[i], ' ', 1)

    smaller_str = smaller_str.replace(' ', '')
    bigger_str = bigger_str.replace(' ', '')

    # Get white pins
    for i in bigger_str:
        if i in smaller_str:
            white += 1

            smaller_str = smaller_str.replace(i, '', 1)
            bigger_str = bigger_str.replace(i, '', 1)
    
    # Update clues array
    game.clues[game.guess_ctr][0] = red
    game.clues[game.guess_ctr][1] = white

    # Check if correct
    if game.code == guess:
        return True
    else:
        return False


def fetch_saves():
    # Make the memory card directory if it doesn't exist
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    save_path = __location__ + "/memory_card"
    pathlib.Path(save_path).mkdir(exist_ok=True)

    # Check for any files in memory card folder
    dir_list = os.listdir(save_path)

    # Save slots
    slots = [1, 2, 3]
    dates = [1, 2, 3]

    # Print slot selection for the user    
    print("Files:")

    # Get any existing saves
    for file in dir_list:                
        # Get slot number and remove from slot list
        slot_number = file[file.index('-') - 1]
        slots[int(slot_number) - 1] = file

        # Get first line of the text file which is date/time info
        date_and_time = open(save_path + '/' + file, "r").read().split('\t')[0]
        dates[int(slot_number) - 1] = date_and_time
    
    # Print save options
    for i in range(3):
        if len(str(slots[i])) == 1:
            slots[i] = 'none'
            print(" " + str(i + 1) + ": empty")
        else:
            print(" " + str(i + 1) + ": " + slots[i][slots[i].index('-') + 1:slots[i].index('.')] + " - Time: " + dates[i])

    return slots, save_path


def save_game(game):
    # Get the current saves
    dir_list, save_path = fetch_saves()

    # Get user choice for slot
    while True:
        # Prompt user
        choice = input("What save would you like to overwrite (1, 2, 3, or c to cancel): ")
        
        if choice == 'c':
            # Exit loop and return
            return False
        elif choice == '1' or choice == '2' or choice == '3':
            # Get index of file to overwrite
            index = int(choice) - 1

            # Get the name for the file
            while True:
                # Prompt user for name
                name = input("What is your name (no special characters): ")

                if re.match(r"^[A-Za-z0-9\s]+$", name):
                    break
                else:
                    print("That is an invalid name.")

            # Delete existing file before saving            
            file_to_overwrite = save_path + "/" + dir_list[index]
            if os.path.exists(file_to_overwrite):
                os.remove(file_to_overwrite)

            # Make file name and file
            save_file_name = save_path + "/" + str(choice) + "-" + name + ".txt"
            save_file = open(save_file_name, "w+")
 
            # Save the date/time to text file
            save_file.write(str(datetime.datetime.now().isoformat(timespec="seconds")))
            
            # Tab to separate data
            save_file.write("\t")
            
            # Save gameboard as a 2d array to text file
            save_file.write(str(np.array(game.gameboard)))
            save_file.write("\t")

            # Save clues as a 2d array to text file
            save_file.write(str(np.array(game.clues)))
            save_file.write("\t")

            # Save code as string to text file
            save_file.write(game.code)
            save_file.write("\t")

            # Save guess counter to text file
            save_file.write(str(game.guess_ctr))

            # Close file
            save_file.close()

            print("Game saved in slot " + choice + " as " + name + ".")

            # Exit loop and return
            return True
        else:
            print("That is an invalid selection.")


def load_game():
    # Get the current saves
    dir_list, save_path = fetch_saves()

    # Get user choice for slot
    while True:
        # Prompt user
        choice = input("What save would you like to load (1, 2, 3, or c to cancel): ")
        
        if choice == 'c':
            # Exit loop and return
            return None
        elif choice == '1' or choice == '2' or choice == '3':            
            # Get index of file to overwrite
            index = int(choice) - 1

            # Check if user chose a valid slot
            if dir_list[index] == "none":
                print("That file is empty!")
            else:            
                # Get file
                save_file_name = save_path + "/" + dir_list[index]
                
                # Read the file and split on tab chars
                save_file = open(save_file_name, "r")
                split_content = save_file.read().split('\t')

                # Close file
                save_file.close()

                # Assign split content to vars
                code = split_content[3]
                gameboard = convert_to_matrix(split_content[1], 6)
                clues = convert_to_matrix(split_content[2], 2)
                guess_ctr = int(split_content[4])

                # Make a new game from loaded data
                loaded_game = Game(code, gameboard, clues, guess_ctr)

                # Return the loaded game
                return loaded_game
        else:
            print("That is an invalid selection.")


def convert_to_matrix(str, length):
    # Convert string to 2d array and get rid of brackets for array
    x = str[1:-1]
    x = x.replace('[', '')
    x = x.replace(']', '')
    x = x.replace(' ', '')
    x = x.replace('\'', '')

    row = 0
    col = 0
    matrix = [['q'] * length for _ in range(10)]
    for n in x:
        if n == '\n':
            row += 1
            col = 0
        else:
            matrix[row][col] = n
            col += 1

    return matrix

def main():
    # Print welcome message    
    print("You are part of Unladened Swallow Society trying to break the infamous Holy")
    print("Grail lock.  This lock protects a vault where IU has locked up all the EBEC")
    print("grades.  To get your grades you will have to break this lock.  Luckily")
    print("those silly IU students messed up when making this lock, and it will give")
    print("you hints on what the code is.  However, you don't know the length of the")
    print("passcode and only have 10 guesses.  You don't want to run out of these.")
    print("Maybe the vault will turn you into a newt!.  Maybe it will destroy the")
    print("grades.  What if you have to rewrite time-calculator!")
    print("\nWill you be able to break this lock before your grades are lost forever?\n")

    while True:
        # Print menu
        print("Menu:")
        print("  1: Rules")
        print("  2: New Game")
        print("  3: Load Game")
        print("  4: Quit")

        # Prompt user for choice
        userChoice = input("Choice: ")

        match userChoice:
            case '1':
                print_rules()
            case '2':
                code = generate_solution(4, 6)
                
                # Make the 2d arrays for gameboard and clues
                gameboard = [['o'] * 6 for _ in range(10)]
                clues = [['0'] * 2 for _ in range(10)]

                # Make a new game
                new_game = Game(code, gameboard, clues, 0)

                # Play the game
                play_game(new_game)
            case '3':
                # Get a saved game from disk
                loaded_game = load_game()
                
                # Make sure we got a valid save slot
                if loaded_game == None:
                    print("cancelled")
                else:
                    # Play the loaded game
                    play_game(loaded_game)
                    
            case '4':
                # Exit program
                print("Goodbye")
                return
            case _:
                # Incorrect entry, remind user of options
                print("Please enter 1, 2, 3, or 4.")


"""Do not change anything below this line."""
if __name__ == "__main__":
    main()
