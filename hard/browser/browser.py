from sys import argv
from os import mkdir, listdir
from requests import get, Response
from bs4 import BeautifulSoup
from colorama import Fore


# A function which is used to filter the list of tags returned by the BeautifulSoup HTML parser.
def filter_tags(tag):
    # Filter out tags not included in the following list.
    valid_tags = ['p', 'a', 'ul', 'ol', 'li']
    if tag.name not in valid_tags:
        return False

    # Filter out tags who contain a child that is also included in the list of valid tags.
    if any([c.name in valid_tags for c in tag.contents]):
        return False

    # Filter out any tags whose text contains "$('".
    if "$('" in tag.get_text():
        return False

    # Otherwise, return true.
    return True


# This function writes the contents of the specified requests.Response object to the specified file.
def write_webpage(res: Response, file: str):
    # Parse the contents of the Response object and open the specified file.
    soup = BeautifulSoup(res.content, 'html.parser')
    stream = open(file, 'w')

    # Find all of the tags in the BeautifulSoup object that satisfy the conditions of the filter_tags function.
    tags = soup.find_all(filter_tags)
    for tag in tags:
        # Filter any newline characters out of the tag's text and join it back into a string.
        txt = ''.join(filter(lambda x: x != '\n', tag.get_text()))

        # Write the text in a blue color if the current tag is a hyperlink, otherwise write it to the file normally.
        if tag.name == 'a':
            stream.write(Fore.BLUE + txt.strip() + '\n' + Fore.RESET)
        else:
            stream.write(txt.strip() + '\n')

    # Flush and close the filestream.
    stream.flush()
    stream.close()


# Ensure the user entered the correct number of command line arguments.
args = argv
if len(args) != 2:
    print('Usage: python browser.py [dir-for-files]')
    exit()

# Create folder to store webpages if it doesn't already exist.
try:
    mkdir(args[1])
except FileExistsError:
    pass

# Store the directory where pages will be saved.
file_dir = args[1]
history = []

# Loop until the user enters 'exit'.
line = input()
while line != 'exit':
    if line == 'back':
        # Retrieve the last web page that the user visited.
        temp = history.pop()
        page = open(history.pop(), 'r')
        history.append(temp)

        # Print each line from the file where the page is stored.
        for s in page.readlines():
            print(s, end='')
        page.close()

        # Get the user's next input and continue to the next iteration of the loop.
        line = input()
        continue

    # Begin building a relative file path for the location of the page's file.
    path = file_dir
    if not path.endswith('/'):
        path += '/'

    if '.' in line:
        # Build the URL of the website as well as the file path.
        url = ''
        if line.startswith('https://'):
            url = line
            path += line[8:line.rindex('.')]
        else:
            url = 'https://' + line
            path += line[:line.rindex('.')]

        # Request the web page.
        r = get(url)
        if not r:
            # If there was some sort of error, get the user's next input and continue to the next iteration of the loop.
            line = input()
            continue

        # Write the web page to its file.
        write_webpage(r, path)

        # Print the contents of the webpage file.
        page = open(path, 'r')
        for s in page.readlines():
            print(s, end='')
        page.close()
    else:
        # If the user did not input a url nor does it match any of the pages stored in the file directory, the input was
        # invalid so print an error message and continue to the next iteration of the loop.
        if line not in listdir(file_dir):
            print('Error: Incorrect url')
            line = input()
            continue

        # Build the path to the file where the page is stored.
        path += line

        # Print the contents of the webpage file.
        page = open(path)
        for s in page.readlines():
            print(s, end='')
        page.close()

    # Add the webpage file to the user's page history and await their next input.
    history.append(path)
    line = input()
