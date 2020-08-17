# Print the tic-tac-toe game board.
def print_field():
    print('-' * 9)
    for i in range(0, 3):
        line = '| '
        for j in range(0, 3):
            line += cells[i][j] + ' '
        line += '|'
        print(line)
    print('-' * 9)


# Updates the game board at the specified location to contain the specified mark, if possible.
def move(x, y):
    if cells[3 - y][x - 1] == ' ':
        cells[3 - y][x - 1] = current_mark
        return True
    else:
        return False


# Count the number of occurrences of the specified mark given the current game state.
def count(mark):
    num = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if cells[i][j] == mark:
                num += 1
    return num


# Check if the specified mark (i.e. 'X' or 'O') is a winner given the current game state.
def check_winner(mark):
    # Check each row.
    for i in range(0, 3):
        if cells[i] == [mark, mark, mark]:
            return True
    # Check each column.
    for i in range(0, 3):
        if [cells[0][i], cells[1][i], cells[2][i]] == [mark, mark, mark]:
            return True
    # Check the diagonals.
    if [cells[0][0], cells[1][1], cells[2][2]] == [mark, mark, mark]:
        return True
    if [cells[0][2], cells[1][1], cells[2][0]] == [mark, mark, mark]:
        return True
    # Otherwise, the mark doesn't win on the current game board.
    return False


# Checks whether the current game state is that of a completed game.
def check_state():
    if check_winner(current_mark):
        print(current_mark + ' wins')
    elif count(' ') == 0:
        print('Draw')
    else:
        return False
    return True


# Prints the specified message and quits the game.
def result(message):
    print(message)
    quit()


cells = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
print_field()

completed = False
current_mark = 'X'
while not completed:  # Main game loop
    valid_input = False
    while not valid_input:  # Loop until the user enters valid input
        print('Enter the coordinates: ')
        coords = input().split()
        for c in coords:
            if not c.isnumeric():  # Check for valid numbers
                print('You should enter numbers!')
                break
            elif int(c) < 1 or int(c) > 3:
                print('Coordinates should be from 1 to 3!')  # Check for numbers in valid range
                break
        else:  # Check that the specified cell is empty
            if move(int(coords[0]), int(coords[1])):
                valid_input = True
            else:
                print('This cell is occupied! Choose another one!')
    print_field()
    completed = check_state()
