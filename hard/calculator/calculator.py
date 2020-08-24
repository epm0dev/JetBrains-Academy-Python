import itertools
from collections import deque
from typing import Deque, Union


class Parser:
    # A special terminating character, used to mark the end of the symbols deque.
    term = '%endl%'

    # The various valid letters and operators that are able to be used for variable names and calculations respectively.
    valid_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    valid_operators = '+-*/^'

    def __init__(self):
        # Create an empty deque to store expressions in.
        self.symbols = deque()

        # Store the values of user-specified variables in a dictionary.
        self.variables = {}

    def command(self, cmd: str):
        # Ignore empty lines.
        if len(cmd) == 0:
            return

        # If the specified string starts with a '/', process it as a command. Otherwise, parse it as an expression.
        if cmd[0] == '/':
            if cmd == '/help':
                print(' Smart Calculator Help Page: ')
                print('-----------------------------')
                print('Supported Expressions:       ')
                print('> Assignment/Declaration     ')
                print(' -> n = 3, m = n, etc.       ')
                print('> Arithmetic                 ')
                print(' -> +, -, *, /, ^, (...)     ')
                print('> Print Variable             ')
                print(' -> variable_name            ')
                print('-----------------------------')
                print('Supported commands:          ')
                print(' -> /help - Print this help  ')
                print('            page.            ')
                print(' -> /exit - Exit the program.')
            elif cmd == '/exit':
                print('Bye!')
                exit()
            else:
                print('Unknown command')
        else:
            self.parse(cmd)

    def parse(self, expression: str):
        # Split the current expression character-wise, ignoring whitespace, and store it in a deque attribute.
        self.symbols = deque(filter(lambda c: c != ' ', expression))

        # Append the special Parser terminating string.
        self.symbols.append(Parser.term)

        # If the specified expression contains an equal sign, attempt to parse it as an assignment.
        if '=' in expression:
            try:
                self.parse_assignment()
            except ValueError as e:
                print(e)
            except NameError as e:
                print(e)
            except SyntaxError as e:
                print(e)
            finally:
                return

        # If the specified expression contains any of the valid operators, attempt to parse it as an expression.
        if any([o in self.symbols for o in Parser.valid_operators]):
            # Parse and evaluate the expression.
            try:
                self.parse_expression()
                print(self.evaluate())
            except SyntaxError:
                print('Invalid expression')
            return

        # Otherwise, attempt to parse the expression as a lone identifier of which to print the value.
        try:
            var_id = self.parse_identifier(0, len(self.symbols) - 1)
        except NameError as e:
            print(e)
        else:
            if var_id not in self.variables.keys():
                print('Unknown variable')
            else:
                print(self.variables[var_id])

    def parse_expression(self):
        # Parse symbols and rotate the deque until its first element is the special terminating string.
        while self.symbols[0] != self.term:
            if self.symbols[0] in '()':
                # If the current symbol is a left or right parenthesis, skip over it.
                pass
            elif self.symbols[0] in self.valid_operators:
                # Handle the parsing of the operators in the list of valid operators.
                self.parse_operator()
            elif self.symbols[0].isdigit():
                # Handle the parsing of a number.
                self.parse_digit()
            elif self.symbols[0] in self.valid_letters:
                # Handle the parsing of a variable identifier. Count the number of symbols until the next operator.
                length = 0
                while self.symbols[0 + length] not in self.valid_operators and self.symbols[0 + length] != self.term:
                    length += 1

                # Check if the symbols from the current index up to the next operator form a valid identifier.
                var_id = self.parse_identifier(0, length)
                if var_id not in self.variables.keys():
                    raise ValueError('Unknown variable')
                else:
                    # Remove the range of characters from the deque, then append the variable identifier to its front.
                    for i in range(length):
                        self.symbols.popleft()
                    self.symbols.appendleft(var_id)
            else:
                # The expression entered was invalid.
                raise ValueError('Invalid expression')

            # Rotate the deque left, past the current element
            self.symbols.rotate(-1)

    def parse_operator(self):
        if self.symbols[0] == '+':
            # If the current symbol is a plus sign, remove all consecutive occurrences of it and add one back to the
            # deque.
            while self.symbols[0] == '+':
                self.symbols.popleft()
            self.symbols.appendleft('+')
        elif self.symbols[0] == '-':
            # If the current symbol is a minus sign, remove all consecutive occurrences of it and add the cumulative
            # sign back to the deque.
            count = 0
            while self.symbols[0] == '-':
                self.symbols.popleft()
                count += 1
            if count % 2 == 0:
                self.symbols.appendleft('+')
            else:
                self.symbols.appendleft('-')

        # If there are any operators directly following the current one, the syntax is invalid.
        if self.symbols[1] in self.valid_operators:
            raise SyntaxError('Invalid expression')

    def parse_digit(self):
        # Store a list of all consecutive digits following the current element and iterate until a non-digit is found.
        digits = []
        while self.symbols[0].isdigit():
            # Append the current element to the list of digits.
            digits.append(self.symbols[0])

            # Remove the left-most element from the deque.
            self.symbols.popleft()

        # Join the digits into one string and append it to the start of the deque.
        self.symbols.appendleft(''.join(digits))

    def parse_assignment(self):
        # Ensure that there is exactly one equal sign present in the expression.
        if self.symbols.count('=') > 1:
            raise SyntaxError('Invalid assignment')

        # Parse the identifier of the variable being assigned to.
        eq = self.symbols.index('=')
        dest_var = self.parse_identifier(0, eq)

        # Try to parse another variable identifier following the equals sign.
        try:
            src_var = self.parse_identifier(eq + 1, len(self.symbols) - 1)
        except NameError:
            # Check for an integer value. If this conversion raises an exception, the assignment is invalid.
            try:
                value = int(''.join(itertools.islice(self.symbols, eq + 1, len(self.symbols) - 1)))
            except ValueError:
                raise SyntaxError('Invalid assignment')
            else:
                # Assign the integer value to the variable.
                self.variables[dest_var] = value
        else:
            # If no error occurred, check that the second variable exists in the variables dictionary.
            if src_var not in self.variables.keys():
                raise ValueError('Unknown variable')

            # Assign the value of the second variable to that of the first.
            self.variables[dest_var] = self.variables[src_var]

    def parse_identifier(self, start: int, stop: int) -> str:
        # The variable is not being assigned a value.
        identifier = ''.join(itertools.islice(self.symbols, start, stop))

        # Ensure that all of the characters in the identifier are valid.
        for c in identifier:
            if c not in Parser.valid_letters:
                raise NameError('Invalid identifier')

        # Return the variable's identifier.
        return identifier

    def evaluate(self):
        # Raise an exception if the expression ends with an operator.
        if self.symbols[-1] in self.valid_operators:
            raise SyntaxError('Invalid expression')

        # Rotate the deque one element to the left from the end string, back to the first symbol of the expression.
        self.symbols.rotate(-1)

        # Convert the expression stored in symbols from infix to postfix notation.
        expression = self.postfix()

        # Evaluate the converted postfix expression.
        stack = deque()

        # TODO
        expression.appendleft(0)

        # Iterate through the postfix expression from left to right.
        expression.append(self.term)
        while expression[0] != self.term:
            if isinstance(expression[0], int):
                # If the incoming element is a number, push it to the stack.
                stack.append(expression[0])
            elif expression[0] in self.valid_operators:
                # If the incoming element is an operator, pop two values from the top of the stack, carry out the
                # operation on them, and push the result onto the stack.
                op1 = stack.pop()
                op2 = stack.pop()
                if expression[0] == '+':
                    stack.append(op2 + op1)
                elif expression[0] == '-':
                    stack.append(op2 - op1)
                elif expression[0] == '*':
                    stack.append(op2 * op1)
                elif expression[0] == '/':
                    stack.append(op2 // op1)
                elif expression[0] == '^':
                    stack.append(op2 ** op1)

            # Rotate the expression deque past the current element.
            expression.rotate(-1)

        # Return the result of the expression.
        return stack[-1]

    def postfix(self) -> Deque[Union[str, int]]:
        # Create a new deque to store the new expression in postfix notation.
        exp = deque()

        # Create a new deque to act as a stack and temporarily store operators for reordering.
        ops = deque()

        # Rotate through symbols until the special terminating character is found.
        while self.symbols[0] != self.term:
            if self.symbols[0] in self.valid_operators or self.symbols[0] in '()':
                # If the current symbol is an operator...
                if len(ops) == 0 or ops[-1] == '(':
                    # If the operator stack is empty or has a left parenthesis at the end, append the operator to it.
                    ops.append(self.symbols[0])
                elif self.symbols[0] == '(':
                    # If the symbol is a left parenthesis, push it to the operator stack.
                    ops.append(self.symbols[0])
                elif self.symbols[0] == ')':
                    # If the symbol is a right parenthesis, pop operators from the stack and add them to the resulting
                    # expression until a left parenthesis is found.
                    while len(ops) > 0 and ops[-1] != '(':
                        exp.append(ops.pop())

                    # If there are no more operators on the stack, there was no matching left parenthesis which means
                    # the expression has unbalanced brackets.
                    if len(ops) == 0:
                        raise SyntaxError('Unbalanced brackets')

                    # Pop the left parenthesis from the stack to discard it.
                    ops.pop()
                elif self.precedence(ops[-1]) > 0:
                    # If the new operator has higher precedence than the top of the stack, push it to the stack.
                    ops.append(self.symbols[0])
                elif self.precedence(ops[-1]) <= 0:
                    # If the new operator doesn't have higher precedence, pop operators from the stack and add them to
                    # the resulting expression until an operator with smaller precedence or a left parenthesis is found.
                    while len(ops) > 0 and self.precedence(ops[-1]) <= 0 and ops[-1] != '(':
                        exp.append(ops.pop())

                    # Now add the incoming operator to the stack.
                    ops.append(self.symbols[0])
            elif self.symbols[0].isdigit():
                # If the current symbol consists only of digits, convert it to an integer and append it to the result.
                exp.append(int(self.symbols[0]))
            else:
                # Otherwise, it is a variable, so append it's value to the result.
                exp.append(int(self.variables[self.symbols[0]]))

            # Rotate the deque past the current element
            self.symbols.rotate(-1)

        # Pop any remaining operators from the stack and add them to the resulting expression until it is empty.
        while len(ops) > 0 and ops[-1] != '(':
            exp.append(ops.pop())

        # If the operator stack still contains a parenthesis, there was no matching right parenthesis meaning the
        # expression has unbalanced brackets.
        if len(ops) > 0 and '(' in ops:
            raise SyntaxError('Unbalanced brackets')

        # Return the postfix representation of the expression.
        return exp

    # Returns an integer value which represents whether the operator at the front of the symbols deque has higher (1),
    # lower (-1), or equal (0) precedence than or to the specified operator.
    def precedence(self, top: str) -> int:
        if top in '+-':
            if self.symbols[0] in '+-':
                return 0
            else:
                return 1
        elif top in '*/':
            if self.symbols[0] in '*/':
                return 0
            elif self.symbols[0] in '+-':
                return -1
            else:
                return 1
        elif top == '^':
            if self.symbols[0] == '^':
                return 0
            else:
                return -1


# Create a Parser object to handle user input until it exits the program when the user enters the '/exit' command.
parser = Parser()
while True:
    parser.command(input())
