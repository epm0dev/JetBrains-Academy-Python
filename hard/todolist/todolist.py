from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, create_engine
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import List


# Create a base class for an SQLAlchemy table.
Base = declarative_base()


# An SQLAlchemy table which contains tasks, their id and their deadline.
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return str(self.id) + '. ' + self.task


# A function which prints the specified list of tasks using the specified lambda expression to convert them to strings.
def print_tasks(header: str, tasks: List[Task], task_str, on_empty: str):
    # Print the specified header string.
    print(header)

    # If the list is not empty, print its contents. Otherwise, print the specified message to print for empty lists.
    if len(tasks) > 0:
        for i in range(len(tasks)):
            print(str(i + 1) + '. ' + task_str(tasks[i]))
        print()
    else:
        print(on_empty)


class Menu:
    # Define the various states that the menu can be in during program execution.
    class State(Enum):
        AWAIT_COMMAND = auto()
        AWAIT_TASK = auto()
        AWAIT_DEADLINE = auto()
        EXIT = auto()

    def __init__(self):
        # Initialize an SQLAlchemy engine to handle the task database.
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)

        # Create a session with the database.
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create an attribute to temporarily store a new row in the database while more information is needed.
        self.new_row = None

        # Set the menu's state to AWAIT_COMMAND and store an integer representing the last command entered by the user.
        self.__setstate__(self.State.AWAIT_COMMAND)
        self.last_command = -1

    def __setstate__(self, state: State):
        # Depending on the Menu's new state, print a variety of prompts for the user.
        if state == self.State.AWAIT_COMMAND:
            print("1) Today's tasks")
            print("2) Week's tasks")
            print("3) All tasks")
            print('4) Missed tasks')
            print('5) Add task')
            print('6) Delete task')
            print('0) Exit')
        elif state == self.State.AWAIT_TASK:
            print('Enter task')
        elif state == self.State.AWAIT_DEADLINE:
            print('Enter deadline')
        elif state == self.State.EXIT:
            print('Bye!')

        # Set the state attribute to the specified value.
        self.state = state

    # This method processes every user command.
    def command(self, cmd: str):
        if self.state == self.State.AWAIT_COMMAND:
            # Print an empty line of padding and store the current date.
            print()
            today = datetime.today()

            # Handle each supported command according to the user's input.
            if cmd == '1':
                # List today's tasks.
                tasks = self.session.query(Task).filter(Task.deadline == today.date()).all()
                print_tasks(today.strftime('Today %d %b:'), tasks, lambda x: x.task, 'Nothing to do!\n')
                self.__setstate__(self.State.AWAIT_COMMAND)
            elif cmd == '2':
                # List the next 7 day's tasks.
                for i in range(7):
                    tasks = self.session.query(Task).filter(Task.deadline == today.date()).all()
                    print_tasks(today.strftime('%A %d %b:'), tasks, lambda x: x.task, 'Nothing to do!\n')
                    today += timedelta(days=1)
                self.__setstate__(self.State.AWAIT_COMMAND)
            elif cmd == '3':
                # List all tasks in the database.
                tasks = self.session.query(Task).order_by(Task.deadline).all()
                print_tasks('All tasks:', tasks, lambda x: x.task + '. ' + x.deadline.strftime('%d %b'),
                            'Nothing to do!\n')
                self.__setstate__(self.State.AWAIT_COMMAND)
            elif cmd == '4':
                # List all missed tasks (those whose deadline falls before today's date).
                tasks = self.session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()
                print_tasks('Missed tasks:', tasks, lambda x: x.task + '. ' + x.deadline.strftime('%d %b'),
                            'Nothing is missed!\n')
                self.__setstate__(self.State.AWAIT_COMMAND)
            elif cmd == '5':
                # Await input for a new task's task field.
                self.__setstate__(self.State.AWAIT_TASK)
            elif cmd == '6':
                # List all missed tasks (those whose deadline falls before today's date).
                tasks = self.session.query(Task).order_by(Task.deadline).all()
                if len(tasks) > 0:
                    print_tasks('Choose the number of the task you want to delete:', tasks,
                                lambda x: x.task + '. ' + x.deadline.strftime('%d %b'), '')

                    # Allow the user to choose a task to remove from the list and delete it from the database.
                    choice = input()
                    if choice.isdigit():
                        self.session.delete(tasks[int(choice) - 1])
                        self.session.commit()
                        print('The task has been deleted!\n')
                else:
                    print('Nothing is missed!\n')
                self.__setstate__(self.State.AWAIT_COMMAND)
            elif cmd == '0':
                # Complete execution of the program.
                self.__setstate__(self.State.EXIT)
            else:
                # An invalid command was entered, await a new one.
                self.__setstate__(self.State.AWAIT_COMMAND)
                print()
        elif self.state == self.State.AWAIT_TASK:
            # Create a new row with the specified task description, then await user input of its deadline.
            self.new_row = Task(task=cmd)
            self.__setstate__(self.State.AWAIT_DEADLINE)
        elif self.state == self.State.AWAIT_DEADLINE:
            # Set the deadline field of the new row and add it to database.
            try:
                self.new_row.deadline = datetime.strptime(cmd, '%Y-%m-%d')
                self.session.add(self.new_row)
                self.session.commit()
                print('The task has been added!\n')
                self.new_row = None  # no longer needed.
                self.__setstate__(self.State.AWAIT_COMMAND)
            except ValueError:
                self.__setstate__(self.State.AWAIT_DEADLINE)


# Create a Menu object and read commands from the user until the Menu's state is Menu.State.Exit.
menu = Menu()
while menu.state != menu.State.EXIT:
    menu.command(input())
