################################################################################
#   CSE Project 7 - Crossword Game, Classes Page
#   Overview:
#       1 - Clue Class:
#           __init__: constructor for the class
#           __str__: returns clue as a string
#           __repr__: returns clue and answer as string
#           __lt__: checks order of indices
#       2 - Crossword Class
#           __init__: constructor for the class
#           _load: structures the puzzles from the csv file
#           __str__: returns crossword puzzle as string, labeled indices
#           __repr__: returns crossword puzzle as string, labeled indices
#           change_guess: checks user's guess into the crossword
#           reveal_answer: reveals answer for a clue
#           find_wrong_letter: finds first incorrect letter from user answer
#           is_solved: checks if crossword is solved
################################################################################

import csv

CROSSWORD_DIMENSION = 5

GUESS_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


class Clue:
    def __init__(self, indices, down_across, answer, clue):
        """
        Puzzle clue constructor
        :param indices: row,column indices of the first letter of the answer
        :param down_across: A for across, D for down
        :param answer: The answer to the clue
        :param clue: The clue description
        """
        self.indices = indices
        self.down_across = down_across
        self.answer = answer
        self.clue = clue

    def __str__(self):
        """
        Return a representation of the clue (does not include the answer)
        :return: String representation of the clue
        """
        return f"{self.indices} {'Across' if self.down_across == 'A' else 'Down'}: {self.clue}"

    def __repr__(self):
        """
        Return a representation of the clue including the answer
        :return: String representation of the clue
        """
        return str(self) + f" --- {self.answer}"

    def __lt__(self, other):
        """
        Returns true if self should come before other in order. Across clues come first,
        and within each group clues are sorted by row index then column index
        :param other: Clue object being compared to self
        :return: True if self comes before other, False otherwise
        """
        return ((self.down_across,) + self.indices) < ((other.down_across,) + other.indices)


class Crossword:
    def __init__(self, filename):
        """
        Crossword constructor
        :param filename: Name of the csv file to load from. If a file with
        this name cannot be found, a FileNotFoundError will be raised
        """
        self.clues = dict()
        self.board = [['■' for _ in range(CROSSWORD_DIMENSION)] for __ in range(CROSSWORD_DIMENSION)]
        self._load(filename)

    def _load(self, filename):
        """
        Load a crossword puzzle from a csv file
        :param filename: Name of the csv file to load from
        """
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                indices = tuple(map(int, (row['Row Index'], row['Column Index'])))
                down_across, answer = row['Down/Across'], row['Answer']
                clue_description = row['Clue']
                clue = Clue(indices, down_across, answer, clue_description)

                key = indices + (down_across,)
                self.clues[key] = clue

                i = 0
                while i < len(answer):
                    if down_across == 'A':
                        self.board[indices[0]][indices[1] + i] = '_'
                    else:
                        self.board[indices[0] + i][indices[1]] = '_'
                    i += 1

    def __str__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        board_str = '     ' + '    '.join([str(i) for i in range(CROSSWORD_DIMENSION)])
        board_str += "\n  |" + "-"*(6*CROSSWORD_DIMENSION - 3) + '\n'
        for i in range(CROSSWORD_DIMENSION):
            board_str += f"{i} |"
            for j in range(CROSSWORD_DIMENSION):
                board_str += f"  {self.board[i][j]}  "
            board_str += '\n'

        return board_str

    def __repr__(self):
        """
        Return a string representation of the crossword puzzle,
        where the first row and column are labeled with indices
        :return: String representation of the crossword puzzle
        """
        return str(self)

    def change_guess(self, clue, new_guess):
        '''
        Allows the user to enter a new guess into the crossword.
        The function checks if guess is valid,
        otherwise user is prompted again.
        '''
        if len(new_guess) != len(clue.answer):
            raise RuntimeError("Guess length does not match the length of the clue.\n")

        if not set(new_guess).issubset(GUESS_CHARS):
                raise RuntimeError("Guess contains invalid characters.\n")

        indices = clue.indices
        if clue.down_across == 'A':
            for i in range(len(new_guess)):
                self.board[indices[0]][indices[1] + i] = new_guess[i]
        else:
            for i in range(len(new_guess)):
                self.board[indices[0] + i][indices[1]] = new_guess[i]

    def reveal_answer(self, clue):
        '''
        Returns the answer of the crossword for a given clue.
        '''
        self.change_guess(clue, clue.answer)

    def find_wrong_letter(self, clue):
        '''
        Checks the answer for the first wrong letter in the crossword.
        The index of the incorrect answer is returned.
        '''
        indices = clue.indices
        if clue.down_across == 'A':
            for i in range(len(clue.answer)):
                if self.board[indices[0]][indices[1] + i] != clue.answer[i]:
                    return (i)
        else:
            for i in range(len(clue.answer)):
                if self.board[indices[0] + i][indices[1]] != clue.answer[i]:
                    return (i)
        return (-1)
    def is_solved(self):
        '''
        Checks crossword table to make sure it is solved.
        Returns True if crossword table is solved, False otherwise.
        '''
        for clue in self.clues.values():
            if self.find_wrong_letter(clue) != -1:
                return False
        return True
