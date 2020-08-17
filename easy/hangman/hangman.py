import random


# A simple function which returns a string concatenation of a list containing strings.
def list_to_str(plist):
    p_str = ''
    for ch in plist:
        p_str += ch
    return p_str


# This function contains the main game loop.
def play():
    # Print a welcome message.
    print("H A N G M A N")

    # Store a list of the possible words to be used by the game.
    words = ['python', 'java', 'kotlin', 'javascript']

    # Randomly select the hidden word for the current game.
    hidden = words[random.randint(0, len(words) - 1)]

    # Build a list of dashes with the same length as the hidden word.
    display = list()
    for i in range(0, len(hidden)):
        display.append('-')

    # Store a set containing the user's guesses.
    prev = set()

    # Store the number of guesses that the user has left, starting at 8.
    guesses = 8

    # The main game loop; iterate until the user is out of moves.
    while guesses > 0 and '-' in display:
        # Print a new line.
        print()

        # Print the display list and a prompt for the user to enter a letter.
        print(list_to_str(display))
        print("Input a letter: > ")

        # Store the user's guess and check it's validity.
        guess = input()
        if guess in prev:
            print("You already typed this letter")
            continue
        elif len(guess) != 1:
            print("You should input a single letter")
            continue
        elif not guess.isascii() or not guess.islower():
            print("It is not an ASCII lowercase letter")
            continue

        # Check if the guess is in the hidden word.
        i = 0
        no_matches = True
        while i < len(hidden):
            if guess == hidden[i]:
                no_matches = False
                # Mark any matches in the display list.
                display[i] = guess

            # Increment the index.
            i += 1

        # Display a message if the guess was not present in the hidden string; reduce the number of attempts remaining.
        if no_matches:
            print('No such letter in the word')
            prev.add(guess)
            guesses -= 1
            continue

        # Add the guess to the set of the user's previous guesses.
        prev.add(guess)

    # Print an appropriate message based on the outcome of the game.
    if '-' in display:
        print('You are hanged!')
    else:
        print('You guessed the word {}!'.format(hidden))
        print('You survived!')


# Declare a variable to store the user's input.
command = ''

# Loop until the user enters 'exit'.
while command != 'exit':
    # Prompt the user to enter a command and store their input.
    print('Type "play" to play the game, "exit" to quit: > ')
    command = input()

    # Enter the main game loop if the player entered 'play'.
    if command == 'play':
        play()
