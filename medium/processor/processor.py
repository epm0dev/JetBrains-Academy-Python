from math import pow


def dot_product(row, col):  # calculate dot product of two vectors
    product_sum = 0
    for n in range(len(row)):
        product_sum += row[n] * col[n]
    return product_sum


def minor(matrix, i, j):  # calculate the minor of element i,j; used to calculate determinant and inverse
    rows = []
    for r in range(len(matrix)):
        if r != i - 1:
            row = []
            for c in range(len(matrix[r])):
                if c != j - 1:
                    row.append(matrix[r][c])
            rows.append(row)
    return rows


def calc_determinant(matrix):  # recursively calculate a matrix's determinant
    if not matrix:
        return 0
    elif len(matrix) == 1 and len(matrix[0]) == 1:
        return matrix[0][0]
    elif len(matrix) == 2 and len(matrix[0]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        expanded_sum = 0.0
        for c in range(len(matrix[0])):
            expanded_sum += matrix[0][c] * pow(-1, c + 2) * calc_determinant(minor(matrix, 1, c + 1))
        return expanded_sum


class Matrix:
    def __init__(self, n_rows, n_cols, rows):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cells = []
        self.set_cells(rows)

    def __str__(self):
        out = ''
        for i in range(self.n_rows):
            out += ' '.join([str(n) for n in self.cells[i]]) + '\n'
        return out

    def get_row(self, r):
        return self.cells[r]

    def get_col(self, c):
        col = []
        for i in range(self.n_rows):
            col.append(self.cells[i][c])
        return col

    def set_cells(self, rows):
        self.cells.clear()
        for row in rows:
            self.cells.append([float(i) for i in row])

    def swap_dimensions(self):
        temp = self.n_cols
        self.n_cols = self.n_rows
        self.n_rows = temp

    def add_matrix(self, other):
        if self.n_rows != other.n_rows or self.n_cols != other.n_cols:
            return False
        else:
            for i in range(self.n_rows):
                for j in range(self.n_cols):
                    self.cells[i][j] += other.cells[i][j]
            return True

    def mult_scalar(self, scalar):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                self.cells[i][j] *= scalar

    def mult_matrix(self, other):
        if self.n_cols != other.n_rows:
            return False
        else:
            self.n_cols = other.n_cols

            rows = []
            for i in range(self.n_rows):
                row = []
                for j in range(self.n_cols):
                    row.append(dot_product(self.get_row(i), other.get_col(j)))
                rows.append(row)
            self.set_cells(rows)
            return True

    def transpose(self, t_type):
        if t_type == 'main':
            # Transpose the Matrix along the main diagonal.
            new_cells = []
            for c in range(self.n_cols):
                new_cells.append(self.get_col(c))
            self.set_cells(new_cells)
            self.swap_dimensions()
        elif t_type == 'side':
            # Transpose the Matrix along the side diagonal.
            new_cells = []
            for c in range(self.n_cols):
                new_row = self.get_col(self.n_cols - c - 1)
                new_row.reverse()
                new_cells.append(new_row)
            self.set_cells(new_cells)
            self.swap_dimensions()
        elif t_type == 'vertical':
            # Transpose the Matrix along the vertical (i.e. reverse each row).
            for r in self.cells:
                r.reverse()
        elif t_type == 'horizontal':
            # Transpose the Matrix along the horizontal (i.e. reverse each column).
            for r in range(int((self.n_rows + self.n_rows % 2) / 2)):
                swap = self.cells[r]
                self.cells[r] = self.cells[self.n_rows - r - 1]
                self.cells[self.n_rows - r - 1] = swap
        else:
            return False
        return True

    def determinant(self):
        return calc_determinant(self.cells)

    def inverse(self):
        if 2 < self.n_rows == self.n_cols > 2:
            # Find the matrix's cofactors.
            cofactors = []
            for i in range(self.n_rows):
                row = []
                for j in range(self.n_cols):
                    row.append(pow(-1, i + j) * calc_determinant(minor(self.cells, i + 1, j + 1)))
                cofactors.append(row)

            # Calculate the determinant of the matrix, transpose its cofactors, then calculate the inverse.
            determinant = self.determinant()
            self.set_cells(cofactors)
            self.transpose('main')
            self.mult_scalar(1 / determinant)
        else:
            return False
        return True


def read_matrix(ordinal=''):
    print('Enter size of ', ordinal, 'matrix: ', sep='')
    rows, cols = [int(n) for n in input().split()]

    print('Enter ', ordinal, 'matrix', sep='')
    lines = []
    for i in range(rows):
        lines.append(input().split())
    return Matrix(rows, cols, lines)


def result(out):
    print('The result is:')
    print(out)


# A Finite State Machine which stores the program's current state and handles its transition between states.
class MenuFSM:
    def __init__(self):
        self.state = 'init'
        self.set_state('await_command')

    def set_state(self, state):
        if state == 'await_command':
            print('1. Add matrices\n'
                  '2. Multiply matrix by a constant\n'
                  '3. Multiply matrices\n'
                  '4. Transpose matrix\n'
                  '5. Calculate a determinant\n'
                  '6. Inverse matrix\n'
                  '0. Exit\n'
                  'Your choice: ')
        elif state == 'await_option_transpose':
            print('1. Main diagonal\n'
                  '2. Side diagonal\n'
                  '3. Vertical line\n'
                  '4. Horizontal line\n'
                  'Your choice: ')
        self.state = state

    def command(self, cmd):
        if self.state == 'await_command':
            if cmd == '1':
                m1 = read_matrix('first ')
                m2 = read_matrix('second ')
                if m1.add_matrix(m2):
                    result(m1)
                else:
                    print('The operation cannot be performed.')
            elif cmd == '2':
                mat = read_matrix()
                print('Enter constant: ')
                mat.mult_scalar(float(input()))
                result(mat)
            elif cmd == '3':
                m1 = read_matrix('first ')
                m2 = read_matrix('second ')
                if m1.mult_matrix(m2):
                    result(m1)
                else:
                    print('The operation cannot be performed.')
            elif cmd == '4':
                self.set_state('await_option_transpose')
            elif cmd == '5':
                mat = read_matrix()
                result(mat.determinant())
            elif cmd == '6':
                mat = read_matrix()
                if mat.inverse():
                    result(mat)
                else:
                    print("This matrix doesn't have an inverse.")
            else:
                self.state = 'exit'
        elif self.state == 'await_option_transpose':
            if cmd == '1':
                along = 'main'
            elif cmd == '2':
                along = 'side'
            elif cmd == '3':
                along = 'vertical'
            elif cmd == '4':
                along = 'horizontal'
            else:
                self.set_state('exit')
                return

            mat = read_matrix()
            mat.transpose(along)
            result(mat)
            self.set_state('await_command')
        else:
            self.set_state('exit')


# The main program loop which iterates until the MenuFSM has a state of 'exit'.
menu = MenuFSM()
while menu.state != 'exit':
    menu.command(input())
