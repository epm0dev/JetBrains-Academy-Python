class CoffeeMachine:
    # Constructor that initializes a CoffeeMachine with default values.
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.coffee_beans = 120
        self.cups = 9
        self.money = 550
        self.state = 'await_command'

    # Determines if the coffee machine has enough resources to make the specified type of coffee and adjusts
    # attribute values accordingly.
    def buy(self, choice):
        # Change the CoffeeMachine's state so that it is now awaiting another command.
        self.state = 'await_command'

        # Check if the user chose to return to the main menu.
        if choice == 'back':
            return
        else:
            choice = int(choice)

        # Define the number of each resource is needed based upon the type of coffee the user selected.
        water_needed = 0
        milk_needed = 0
        coffee_beans_needed = 0
        cost = 0
        if choice == 1:  # espresso
            water_needed = 250
            coffee_beans_needed = 16
            cost = 4
        elif choice == 2:  # latte
            water_needed = 350
            milk_needed = 75
            coffee_beans_needed = 20
            cost = 7
        elif choice == 3:  # cappuccino
            water_needed = 200
            milk_needed = 100
            coffee_beans_needed = 12
            cost = 6

        # Check that there is enough of each resource to make the coffee, then make it and adjust attribute values.
        if self.water - water_needed < 0:
            print('Sorry, not enough water!')
        elif self.milk - milk_needed < 0:
            print('Sorry, not enough milk!')
        elif self.coffee_beans - coffee_beans_needed < 0:
            print('Sorry, not enough coffee beans!')
        elif self.cups < 1:
            print('Sorry, not enough disposable cups!')
        else:
            print('I have enough resources, making you a coffee!')
            self.water -= water_needed
            self.milk -= milk_needed
            self.coffee_beans -= coffee_beans_needed
            self.cups -= 1
            self.money += cost

    # Adjusts an attribute corresponding to the CoffeeMachine's current state by the specified amount.
    def fill(self, amount):
        if self.state == 'await_amt_water':
            self.water += int(amount)
            self.state = 'await_amt_milk'
            print('Write how many ml of milk do you want to add:')
        elif self.state == 'await_amt_milk':
            self.milk += int(amount)
            self.state = 'await_amt_coffee_beans'
            print('Write how many grams of coffee beans do you want to add:')
        elif self.state == 'await_amt_coffee_beans':
            self.coffee_beans += int(amount)
            self.state = 'await_amt_cups'
            print('Write how many disposable cups of coffee do you want to add:')
        elif self.state == 'await_amt_cups':
            self.cups += int(amount)
            self.state = 'await_command'

    # Prints a message and reduces the CoffeeMachine's money attribute to 0.
    def take(self):
        print('I gave you ${}'.format(self.money))
        self.money = 0

    # Prints the CoffeeMachine's attribute's values.
    def remaining(self):
        print('The coffee machine has:')
        print('{} of water'.format(self.water))
        print('{} of milk'.format(self.milk))
        print('{} of coffee beans'.format(self.coffee_beans))
        print('{} of disposable cups'.format(self.cups))
        print('{} of money'.format(self.money))

    # Handles all incoming commands based on the current state of the CoffeeMachine.
    def command(self, command):
        if self.state == 'await_command':
            if command == 'buy':
                self.state = 'await_buy_choice'
                print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
            elif command == 'fill':
                self.state = 'await_amt_water'
                print('Write how many ml of water do you want to add:')
            elif command == 'take':
                self.take()
            elif command == 'remaining':
                self.remaining()
            elif command == 'exit':
                self.state = 'shutdown'
        elif self.state == 'await_buy_choice':
            self.buy(command)
        elif self.state.startswith('await_amt_'):
            self.fill(command)


# Create a CoffeeMachine instance and loop until it reaches the 'shutdown' state.
machine = CoffeeMachine()
while machine.state != 'shutdown':
    if machine.state == 'await_command':
        print('Write action (buy, fill, take, remaining, exit):')
    machine.command(input())
