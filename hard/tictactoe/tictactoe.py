from random import randrange
from enum import Enum, auto
from typing import Mapping


# Defines the structure of the tic-tac-toe game board and provides useful operators and methods for changing and
# analyzing it in the context of a Game.
class Board:
    n_rows = 3
    n_cols = 3

    def __init__(self):  # creates an empty Board
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    # An implementation of the '[]' indexing operator which allows for the retrieval of a value at a specific index as
    # though Board objects were lists themselves.
    def __getitem__(self, item: int) -> str:
        return self.board[item]

    # An implementation of the '=' assignment operator which allows for the values stored in Board's list of cells to be
    # easily and quickly changed.
    def __setitem__(self, item: int, value: str):
        self.board[item] = value

    # A method which returns a nested list of lists containing each row's elements.
    def rows(self) -> [[]]:
        rows = []
        for i in range(self.n_rows):
            rows.append(self.board[i * self.n_cols:i * self.n_cols + self.n_cols])
        return rows

    # A method which returns a nested list of lists containing each column's elements.
    def cols(self) -> [[]]:
        cols = []
        for i in range(self.n_cols):
            cols.append(self.board[i * self.n_rows::self.n_cols])
        return cols

    # A method which determines the current state of the Board (win_x, win_o, draw, incomplete).
    def state(self):
        for r in self.rows():  # Check rows for 3 consecutive occurrences of either 'X' or 'O'.
            if r.count('X') == 3:
                return 'win_x'
            elif r.count('O') == 3:
                return 'win_o'

        for c in self.cols():  # Check columns for 3 consecutive occurrences of either 'X' or 'O'.
            if c.count('X') == 3:
                return 'win_x'
            elif c.count('O') == 3:
                return 'win_o'

        # Check diagonals for 3 consecutive occurrences of either 'X' or 'O'.
        if [self.board[0], self.board[4], self.board[8]].count('X') == 3 or \
                [self.board[6], self.board[4], self.board[2]].count('X') == 3:
            return 'win_x'
        if [self.board[0], self.board[4], self.board[8]].count('O') == 3 or \
                [self.board[6], self.board[4], self.board[2]].count('O') == 3:
            return 'win_o'

        # Board is a draw if neither player won, but there are no empty cells remaining.
        if self.board.count(' ') == 0:
            return 'draw'

        # Board incomplete if none of the above conditions are satisfied.
        return 'incomplete'

    # A simple method which returns a boolean value indicating whether or not the specified mark has won the Board.
    def is_winner(self, mark: str) -> bool:
        return self.state().endswith(mark.lower())

    # A method which prints a formatted representation of the Board's cells.
    def print(self):
        print('-' * 9)
        for row in self.rows():
            print('| ' + ' '.join(row) + ' |')
        print('-' * 9)


# Defines a player in a game of tic-tac-toe.
class Player:
    # Defines the various types of players.
    class PType(Enum):
        USER = auto()
        EASY = auto()
        MEDIUM = auto()
        HARD = auto()

    def __init__(self, p_type: PType, mark: str):
        self.p_type = p_type
        self.mark = mark
        if mark == 'X':
            self.opp = 'O'
        else:
            self.opp = 'X'

    # Calculates and returns the coordinates of an AI player's move based on it's corresponding difficulty.
    def calc_move(self, board: Board) -> int:
        print('Making move level "{}"'.format(self.p_type.name.lower()))

        if self.p_type == self.PType.EASY:
            return check_rand(board)
        elif self.p_type == self.PType.MEDIUM:
            return self.calc_move_medium(board)
        elif self.p_type == self.PType.HARD:
            return self.calc_move_hard(board)

    # Calculates the move of a 'medium' AI by calling the check_rows, check_cols, and check_diag functions, and if there
    # is not enough information for those algorithms to select a move, reverts to the calc_move_easy method to pick a
    # random move.
    def calc_move_medium(self, board: Board) -> int:
        n = check_win_shallow(board, self.mark)
        if n == -1:
            return check_rand(board)
        else:
            return n

    # Calculates the move of a 'hard' AI by way of an implementation of a brute-force minimax algorithm.
    def calc_move_hard(self, board: Board) -> int:
        # Create a new board object and copy the cells from the original board to it, replacing empty cells with their
        # index.
        new_board = Board()
        for i in range(9):
            if board[i] == ' ':
                new_board[i] = str(i)
            else:
                new_board[i] = board[i]

        # Return the value associated with the 'index' key in the mapping returned by the minimax function.
        return self.minimax(new_board, self.mark)['index']

    # A brute-force implementation of the minimax algorithm which recursively assesses all possible outcomes of the
    # specified game board. This is accomplished by first weighting each possible outcome of the game based on the
    # desired outcome. Therefore, since an AI Player is attempting to win the game, the possible outcomes are weighted
    # as follows: win = +10 (desirable outcome), tie = 0 (neutral outcome), and loss = -10 (undesirable outcome). To
    # determine the 'best' move for the AI to make at any point in the game, each of the moves that can be made are
    # evaluated by finding the best score of all of the moves that can be made immediately following the first move.
    # This pattern recurs until one of the base cases is reached and a move object is returned. Once scores have been
    # calculated for all of the possible moves at any level, the 'best' move is chosen based on who the player is at the
    # current level of recursion. If the current player is the original player, the highest score is chosen since that
    # player is trying to win. Otherwise, if the current player is the opponent of the original player, the lowest score
    # is chosen since the original player is trying to beat the current player.
    def minimax(self, new_board: Board, turn_mark: str) -> Mapping[str, int]:
        # Determine and store the locations of cells where moves can be made on the current board.
        avail_idxes = []
        for i in range(9):
            if new_board[i].isdigit() or new_board[i] == ' ':
                avail_idxes.append(i)

        # Handle the recursive base cases of win, loss and tie.
        if new_board.is_winner(self.mark):
            # If the player who originally called the minimax function wins the current board, return a positive score.
            return {'score': 10}
        elif new_board.is_winner(self.opp):
            # If the opponent of the player who originally called the minimax function wins the current board (i.e the
            # original player loses the current board), return a negative score.
            return {'score': -10}
        elif len(avail_idxes) == 0:
            # If neither player wins on the current board, and there are no moves left to make, the result is a tie, so
            # return a neutral score.
            return {'score': 0}

        # Determine the mark of the opponent of the player whose turn it is.
        turn_opp = 'O' if turn_mark == 'X' else 'X'

        # Iterate through all available cells and store objects representing all possible moves.
        moves = []
        for i in range(len(avail_idxes)):
            # Create an object for the current move and store the index of the cell.
            move = {'index': int(new_board[avail_idxes[i]])}

            # Set the empty cell to the current player's mark.
            new_board[avail_idxes[i]] = turn_mark

            # The recursive case. Find the resulting score of calling the minimax function for the opponent of the
            # current player. Since the current cell was marked with the current player's mark, this call to minimax
            # will proceed as though the current player made that move.
            result = self.minimax(new_board, turn_opp)
            move['score'] = result['score']

            # Change the current cell back to the value it had previously and add the move object to the list of moves.
            new_board[avail_idxes[i]] = str(move['index'])
            moves.append(move)

        # Determine the best move to make, depending on whether or not the current player is the player that originally
        # called the minimax function.
        best_move = 0
        best_score = moves[0]['score']
        if turn_mark == self.mark:
            # If the current player is the player that originally called the minimax function, iterate through the
            # results of all currently possible moves and store the largest score.
            i = 0
            for m in moves:
                if m['score'] > best_score:
                    best_score = m['score']
                    best_move = i
                i += 1
        else:
            # Otherwise, the current player is opponent of the player that originally called the minimax function.
            # Iterate through the results of all currently possible moves and store the smallest score.
            i = 0
            for m in moves:
                if m['score'] < best_score:
                    best_score = m['score']
                    best_move = i
                i += 1

        # Return the object that represents the best move.
        return moves[best_move]


# Iterates until an empty cell is found in the specified Board (pseudo-randomly) and returns its index.
def check_rand(board: Board):
    while True:
        idx = randrange(9)
        if board[idx] == ' ':
            return idx


# Iterates through all possible '3-in-a-row' locations of 3x3 Board in search of one where two cells contain the
# specified mark and the third is empty. Returns the index (0 to 8) of that space, or -1 if no 1-turn win scenarios
# were found.
def check_win_shallow(board: Board, mark):
    n = 0
    for r in board.rows():  # check Board rows for 1-turn win scenarios
        if r.count(mark) == 2 and r.count(' '):
            return r.index(' ') + n * board.n_cols
        n += 1

    n = 0
    for c in board.cols():  # check Board cols for 1-turn win scenarios
        if c.count(mark) == 2 and c.count(' '):
            return c.index(' ') + n * board.n_rows
        n += 1

    d = [board[0], board[4], board[8]]  # check '\' diagonal
    if d.count(mark) == 2 and d.count(' '):
        return 4 * d.index(' ')

    d = [board[6], board[4], board[2]]  # check '/' diagonal
    if d.count(mark) == 2 and d.count(' '):
        return 6 - 2 * d.index(' ')

    return -1  # indicate lack of any 1-turn win scenarios


# A finite state machine which controls the state of a game in the program, handling moves made by both users and AI.
class Game:
    # Defines the various states that the Game can be in.
    class State(Enum):
        TURN_START = auto()
        AWAIT_INDEX = auto()
        TURN_END = auto()
        COMPLETE = auto()

    def __init__(self, p1_type, p2_type):
        self.board = Board()
        self.p1 = Player(p1_type, 'X')
        self.p2 = Player(p2_type, 'O')
        self.current_player = self.p1
        self.__setstate__(self.State.TURN_START)

    # Update the Game's state attribute then proceed according to the specified state and the previous state.
    def __setstate__(self, state):
        self.state = state
        if state == self.State.TURN_START:
            # Go ahead and complete the turn if the current player is not a user.
            if self.current_player.p_type != Player.PType.USER:
                self.move()
            else:
                self.__setstate__(self.State.AWAIT_INDEX)
        elif state == self.State.TURN_END:
            # Print the current board.
            self.board.print()

            if self.board.state() == 'incomplete':
                # Swap the current player for the other player.
                if self.current_player is self.p1:
                    self.current_player = self.p2
                elif self.current_player is self.p2:
                    self.current_player = self.p1

                # Start the next turn.
                self.__setstate__(self.State.TURN_START)
            else:
                self.__setstate__(self.State.COMPLETE)
        elif state == self.State.COMPLETE:
            # Determine the final board state and print the appropriate message based on the result.
            final_board = self.board.state()
            if final_board == 'win_x':
                print('X wins\n')
            elif final_board == 'win_o':
                print('O wins\n')
            elif final_board == 'draw':
                print('Draw\n')

    # Completes a move by marking one of the positions in the Board.
    def move(self, index=-1):
        if self.state == self.State.TURN_START:
            # Calculate the position to mark if the current player is an AI.
            self.board[self.current_player.calc_move(self.board)] = self.current_player.mark
            self.__setstate__(self.State.TURN_END)
        else:
            # Mark the specified index if the current player is a user.
            self.board[index] = self.current_player.mark
            self.__setstate__(self.State.TURN_END)


# A finite state machine which controls the outer-most layer of program execution (i.e. starting a game, passing user
# input to the game layer of the program, and exiting the program).
class Menu:
    # Defines the various states that the Menu can be in.
    class State(Enum):
        INIT = auto()
        AWAIT_COMMAND = auto()
        TURN_START = auto()
        AWAIT_COORDINATES = auto()
        TURN_END = auto()
        EXIT = auto()

    def __init__(self):
        self.accept_input = False
        self.game = None
        self.__setstate__(self.State.AWAIT_COMMAND)

    # Update the Menu's state attribute then proceed according to the specified state and the state of the current game,
    # if any.
    def __setstate__(self, state):
        self.state = state
        if state == self.State.INIT:
            # If initializing, give attributes default values and await the next user command.
            self.accept_input = False
            self.game = None
            self.__setstate__(self.State.AWAIT_COMMAND)
        elif state == self.State.AWAIT_COMMAND:
            # If awaiting a user command, accept input and prompt the user to enter it.
            self.accept_input = True
            print('Input command: ', end='')
        elif state == self.State.TURN_START:
            # At turn start, check whether the game's current player is a 'user' or not.
            if self.game.current_player.p_type == Player.PType.USER:
                # If they are a user, await user input of coordinates.
                self.__setstate__(self.State.AWAIT_COORDINATES)
            else:
                # Otherwise, end the turn.
                self.__setstate__(self.State.TURN_END)
        elif state == self.State.AWAIT_COORDINATES:
            # If awaiting coordinates, accept input and prompt the user to enter them.
            self.accept_input = True
            print('Enter the coordinates: ', end='')
        elif state == self.State.TURN_END:
            # At turn end, check if the game has been completed.
            if self.game.state == self.game.State.COMPLETE:
                # If so, reinitialize the menu.
                self.__setstate__(self.State.INIT)
            else:
                # Otherwise, start the next turn.
                self.__setstate__(self.State.TURN_START)

    # A method which steps the program to its next state based on its current state and the state of the game, if any,
    # as well as handles any user input.
    def command(self, cmd=None):
        if self.state == self.State.AWAIT_COMMAND:
            # Process the command and update the Menu's state accordingly.
            splt_cmd = cmd.split()
            types = [t.lower() for t in Player.PType.__members__]
            if splt_cmd[0] == 'start' and splt_cmd[1] in types and splt_cmd[2] in types and len(splt_cmd) == 3:
                self.game = Game(Player.PType[splt_cmd[1].upper()], Player.PType[splt_cmd[2].upper()])
                self.__setstate__(self.State.TURN_START)
            elif cmd == 'exit':
                self.__setstate__(menu.State.EXIT)
            else:
                print('Bad parameters!')
                self.__setstate__(self.State.AWAIT_COMMAND)
        elif self.state == self.State.AWAIT_COORDINATES:
            # Ensure that the user input consists only of digits.
            if all([c.isdigit() for c in cmd.split()]):
                # Convert the coordinates to integers, ensure there are only 2, and ensure they are both in the range
                # 0 < digit < 4.
                coords = [int(i) for i in cmd.split()]  # convert the coordinates to digits
                if len(coords) == 2 and 0 < coords[0] < 4 and 0 < coords[1] < 4:
                    # Calculate the index (0 to 8 from left to right and top to bottom on the board) that the
                    # coordinates correspond to and ensure that the cell located at that index is empty.
                    idx = 3 * (3 - coords[1]) + coords[0] - 1
                    if self.game.board[idx] == ' ':
                        # Make the move and and end the turn.
                        self.game.move(idx)
                        self.__setstate__(self.State.TURN_END)
                        return
                else:
                    print('Coordinates should be from 1 to 3!')
            else:
                print('You should enter numbers!')

            # Reset the Menu's state to prompt the user to enter new coordinates.
            self.__setstate__(self.State.AWAIT_COORDINATES)


# Create a Menu and execute commands until it reaches the Menu.State.EXIT state.
menu = Menu()
while menu.state != menu.State.EXIT:
    if menu.accept_input:
        menu.command(input())
    else:
        menu.command()
