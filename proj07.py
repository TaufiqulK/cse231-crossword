################################################################################
#   CSE Project 7 - Crossword Game
#   Algorithm Overview:
#       1 - Program starts
#       2 - User is asked for a file name
#       3 - The program opens the file
#       4 - The Down/Across word descriptions and the Menu are printed
#       5 - The user is prompted to pick an option from the Menu
#       6 - The user can guess, get a hint, reveal, restart or quit game
#       7 - The options perform different tasks depending on what is selected
#       8 - If incorrect option is chosen, the user is prompted again.
#       9 - The program continues to run until told to stop or user wins.
#       10- Program ends if user chooses the option
################################################################################

from crossword import Crossword, Clue
import sys


HELP_MENU = "\nCrossword Puzzler -- Press H at any time to bring up this menu" \
                "\nC n - Display n of the current puzzle's down and across clues" \
                "\nG i j A/D - Make a guess for the clue starting at row i, column j" \
                "\nR i j A/D - Reveal the answer for the clue starting at row i, column j" \
                "\nT i j A/D - Gives a hint (first wrong letter) for the clue starting at row i, column j" \
                "\nH - Display the menu" \
                "\nS - Restart the game" \
                "\nQ - Quit the program"


OPTION_PROMPT = "\nEnter option: "
PUZZLE_PROMPT = "Enter the filename of the puzzle you want to play: "
PUZZLE_FILE_ERROR = "No puzzle found with that filename. Try Again.\n"

RuntimeError("Guess length does not match the length of the clue.\n")
RuntimeError("Guess contains invalid characters.\n")

def input( prompt=None ):
    """
    DO NOT MODIFY: Uncomment this function when submitting to Codio
    or when using the run_file.py to test your code.
    This function is needed for testing in Codio to echo the input to the output
    Function to get user input from the standard input (stdin) with an optional prompt.
    Args:
     prompt (str, optional): A prompt to display before waiting for input. Defaults to None.
    Returns:
     str: The user input received from stdin.
    """

    if prompt:
        print( prompt, end="" )
        aaa_str = sys.stdin.readline()
        aaa_str = aaa_str.rstrip( "\n" )
        print( aaa_str )
        return aaa_str


def open_crossword_puzzle_file():
    '''
    Opens a file and returns it, checks for errors.
    '''
    filename = input(PUZZLE_PROMPT)
    while True:
        try:
            cross_word = Crossword(filename)
            return cross_word
        except FileNotFoundError:
            print(PUZZLE_FILE_ERROR)
            filename = input(PUZZLE_PROMPT)

def show_clue(cross_word, clues=0):
    '''
    Prints out a given number of clues for the given crossword,
    Otherwise prints out all clues.
    '''
    if clues == 0:
        clues = len(cross_word.clues)//2
    a_list = []
    d_list = []
    for key, value in cross_word.clues.items():
        if value.down_across == 'A':
            a_list.append(value)
        else:
            d_list.append(value)

    print("\nAcross")
    for i in range(clues):
        print(a_list[i])
    print("\nDown")
    for i in range(clues):
        print(d_list[i])



def command_menu(cross_word, user_inp):
    '''
    Prompts the user to perform specific functions from the menu.
    Incorrect input is followed by another prompt.
    Options perform different tasks.
    '''
    user_inp = user_inp.split()
    try:
        matching_clue = "bad input"

        if user_inp[0] in ['G', 'R', 'T']:
            if int(user_inp[1]) < 0 or int(user_inp[2]) < 0:
                ret = 2/0
            if len(user_inp) != 4:
                ret = 2/0
            for key in cross_word.clues:
                if key[0] == int(user_inp[1]) and key[1] == int(user_inp[2]) and key[2] == user_inp[3]:
                    matching_clue = cross_word.clues[key]
                    break
            if matching_clue == "bad input":
                ret = 2/0

        if user_inp[0] == 'C':
            if len(user_inp) >2:
                ret = 2/0
            show_clue(cross_word, int(user_inp[1]))

        elif user_inp[0] == 'G':
            inp = ""
            correct = False
            while correct == False:
                check1 = True
                check2 = True
                inp = input("Enter your guess (use _ for blanks): ").upper()
                if len(inp) != len(str(matching_clue.answer)):
                    print("Guess length does not match the length of the clue.\n")
                    check1 = False
                for letter in inp:
                    if letter not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                        print("Guess contains invalid characters.\n")
                        check2 = False
                        break
                correct = check1 and check2
            cross_word.change_guess(matching_clue, inp)
            print(cross_word)



        elif user_inp[0] == 'R':
            cross_word.reveal_answer(matching_clue)
            print(cross_word)


        elif user_inp[0] == 'T':
            ind = cross_word.find_wrong_letter(matching_clue)
            if ind == -1:
                print("This clue is already correct!")
            else:
                print(f"Letter {ind+1} is wrong, it should be {matching_clue.answer[ind]}")


        elif user_inp[0] == 'H':
            print(HELP_MENU)


        elif user_inp[0] == 'S':
            cross_word = open_crossword_puzzle_file()
            intro(cross_word)


        elif user_inp[0] == 'Q':
            return 'Q'

        else:
            ret = 2/0
    except:
        print("Invalid option/arguments. Type 'H' for help.")
        return None



def intro(puzzle):
    '''
    Prints the introduction to the game and the menu.
    '''
    show_clue(puzzle, 0)
    print(puzzle)
    print(HELP_MENU)

def main():
    puzzle = open_crossword_puzzle_file()
    intro(puzzle)
    while True:
        opt = command_menu(puzzle, input(OPTION_PROMPT))
        if opt == "Q":
            sys.exit()
        if puzzle.is_solved():
            print("\nPuzzle solved! Congratulations!")
            sys.exit()

    pass


if __name__ == "__main__":
    main()
