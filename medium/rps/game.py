import random


def lose(option):
    print('Sorry, but the computer chose {}'.format(option))


def draw(option):
    global score
    score += 50
    print('There is a draw ({})'.format(option))


def win(option):
    global score
    score += 100
    print('Well done. The computer chose {} and failed'.format(option))


def result(usr_choice):
    rnd_choice = choices[random.randint(0, len(choices) - 1)]

    if usr_choice == rnd_choice:
        draw(rnd_choice)
    elif usr_choice in choices:
        # Build a list containing all game choices excluding the user's selection.
        idx = choices.index(usr_choice)
        excluded = choices[idx + 1:] + choices[:idx]

        # If the random choice is in the first half of this new list, the user loses.
        if rnd_choice in excluded[:round((len(excluded) + len(excluded) % 2) / 2)]:
            lose(rnd_choice)
        else:
            win(rnd_choice)
    else:
        print('Invalid input')


print('Enter your name:')
name = input()
print('Hello, {}'.format(name))

score = 0
rating = open('rating.txt', 'r')
for line in rating:
    split_line = line.split()
    if split_line[0] == name:
        score = int(split_line[1])
        break
rating.close()

choices = ['rock', 'paper', 'scissors']
user_choices = input()
if user_choices != '':
    choices = user_choices.split(',')
print("Okay, let's start")

choice = input()
while choice != '!exit':
    if choice == '!rating':
        print('Your rating: {}'.format(score))

    result(choice)
    choice = input()

print('Bye!')
