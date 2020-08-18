import random
import sqlite3


# Finds the checksum of the specified 15-digit number
def find_checksum(number):
    digits = [int(i) for i in number]

    # Multiply odd digits by 2 and subtract 9 if they are larger than 9.
    for i in range(0, len(digits), 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9

    # Sum all digits to find the control number.
    control_num = 0
    for i in digits:
        control_num += i

    # Calculate and return the checksum.
    checksum = (10 - control_num % 10) % 10
    return str(checksum)


# Generates a credit card number with default IIN, random account number and the appropriate checksum.
def gen_card_num():
    iin = '400000'  # Issuer Identification Number

    account_num = str(random.randrange(0, 999999999))  # customer account number
    account_num = '0' * (9 - len(account_num)) + account_num  # prepend 0s to make 9 digits long

    return iin + account_num + find_checksum(iin + account_num)  # find checksum and append to card number


# Generates a random 4-digit pin number.
def gen_pin_num():
    pin_num = str(random.randrange(0, 9999))
    pin_num = '0' * (4 - len(pin_num)) + pin_num  # prepend 0s to make 4 digits long
    return pin_num


class BankSystem:
    def __init__(self, database):
        # Initialize SQL components of the BankSystem with SQLite3.
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.cursor.executescript('''CREATE TABLE IF NOT EXISTS card(
                                     id INTEGER PRIMARY KEY,
                                     number TEXT,
                                     pin TEXT,
                                     balance INTEGER DEFAULT 0)''')
        self.connection.commit()

        # Initialize instance attributes.
        self.logged_in = False
        self.account_id = None
        self.temp_card = None
        self.state = 'await_command'

    def card_exists(self, number):
        self.cursor.execute('SELECT number FROM card WHERE number=:n', {'n': number})
        if self.cursor.fetchone() is not None:
            return True
        return False

    def create_card(self, number, pin):
        self.cursor.execute('INSERT INTO card (number, pin) VALUES (?, ?)', (number, pin))
        self.connection.commit()

        print('Your card has been created')
        print('Your card number:')
        print(number)
        print('Your card PIN:')
        print(pin)

    def create_account(self):
        # Generate card numbers until an unused one is found.
        number = gen_card_num()
        while self.card_exists(number):
            number = gen_card_num()

        # Generate pin and add new account information to the database.
        pin = gen_pin_num()
        self.create_card(number, pin)

    def login(self, pin):
        self.cursor.execute('SELECT id FROM card WHERE number=:n AND pin=:p', {'n': self.temp_card, 'p': pin})
        account = self.cursor.fetchone()
        if account is not None:
            print('You have successfully logged in!')
            self.logged_in = True
            self.account_id = account[0]
        else:
            print('Wrong card number or PIN!')

    def balance(self):
        self.cursor.execute('SELECT balance FROM card WHERE id=:account_id', {'account_id': self.account_id})
        return self.cursor.fetchone()[0]

    def add_income(self, amount):
        self.cursor.execute('''UPDATE card
                               SET balance=balance+:income
                               WHERE id=:id''', {'income': int(amount), 'id': self.account_id})
        self.connection.commit()
        print('Income was added!')

    def do_transfer(self, amount):
        if self.balance() >= amount:
            self.cursor.execute('''UPDATE card
                                   SET balance=balance-:amount 
                                   WHERE id=:id''',
                                {'amount': amount, 'id': self.account_id})
            self.cursor.execute('''UPDATE card
                                   SET balance=balance+:amount 
                                   WHERE number=:number''',
                                {'amount': amount, 'number': self.temp_card})
            self.connection.commit()
            print('Success!')
        else:
            print('Not enough money!')

    def close_account(self):
        self.cursor.execute('DELETE FROM card WHERE id=:id', {'id': self.account_id})
        self.connection.commit()
        print('The account has been closed!')

    def logout(self):
        self.logged_in = False
        self.account_id = None
        print('You have successfully logged out!')

    def command(self, command):
        if self.state == 'await_command':
            if self.logged_in:
                if command == '1':
                    print('Balance: {}'.format(self.balance()))
                elif command == '2':
                    print('Enter income:')
                    self.state = 'await_option_income'
                elif command == '3':
                    print('Transfer')
                    print('Enter card number:')
                    self.state = 'await_option_transfer_card'
                elif command == '4':
                    self.close_account()
                elif command == '5':
                    self.logout()
                else:
                    self.state = 'shutdown'
            else:
                if command == '1':
                    self.create_account()
                elif command == '2':
                    print('Enter your card number:')
                    self.state = 'await_option_login_card'
                else:
                    self.state = 'shutdown'
        elif self.state == 'await_option_income':
            self.add_income(command)
            self.state = 'await_command'
        elif self.state == 'await_option_transfer_card':
            if command[len(command) - 1] != find_checksum(command[:len(command) - 1]):
                print('Probably you made mistake in the card number. Please try again!')
                self.state = 'await_command'
            elif not self.card_exists(command):
                print('Such a card does not exist.')
                self.state = 'await_command'
            else:
                self.temp_card = command
                print('Enter how much money you want to transfer:')
                self.state = 'await_option_transfer_amount'
        elif self.state == 'await_option_transfer_amount':
            self.do_transfer(int(command))
            self.state = 'await_command'
            self.temp_card = None
        elif self.state == 'await_option_login_card':
            self.temp_card = command
            print('Enter your PIN:')
            self.state = 'await_option_login_pin'
        elif self.state == 'await_option_login_pin':
            self.login(command)
            self.temp_card = None
            self.state = 'await_command'
        else:
            self.state = 'shutdown'


# Initialize the BankSystem and allow the user to execute commands until the system enters the 'shutdown' state.
sys = BankSystem('card.s3db')
while sys.state != 'shutdown':
    # Prompt the user to enter their command.
    if sys.state == 'await_command':
        if sys.logged_in:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
        else:
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')

    # Execute the command
    sys.command(input())

# Print a final message before exiting the program.
print('Bye!')
