from typing import List


# Define variables containing various metacharacters and characters.
anchor_start = '^'
anchor_end = '$'
wildcard = '.'
rep_chars = '?*+'
b_slash = '\\'


# Return true if the literal character at the current index in the regex string equals to that of the input string.
def match_literal(reg_str: str, reg_idx: List[int], inp_str: str, inp_idx: List[int]) -> bool:
    if reg_str[reg_idx[0]] == b_slash:
        # Handle an escape sequence.
        reg_idx[0] += 1
        if reg_idx[0] < len(reg_str) and reg_str[reg_idx[0]] == b_slash:
            # Handle an escaped backslash.
            reg_idx[0] += 1
            inp_idx[0] += 1
            return True
        else:
            # Handle all other escaped characters.
            return match_literal(reg_str, reg_idx, inp_str, inp_idx)
    elif reg_str[reg_idx[0]] == inp_str[inp_idx[0]] or reg_str[reg_idx[0]] == wildcard:
        # Handle matching literal characters at the current indexes in the regex and input strings.
        reg_idx[0] += 1
        inp_idx[0] += 1
        return True

    # If there was no match, return false.
    return False


# Move the current index in the input string past characters in the input string until either the end of that string is
# reached, or a match is found with the next character in the regex string.
def repeat_wildcard(reg_str: str, reg_idx: List[int], inp_str: str, inp_idx: List[int]):
    # Move the current index in the regex string past the literal character and metacharacter.
    reg_idx[0] += 2

    if reg_idx[0] < len(reg_str):
        # Handle incrementing the input string index when the repetition pattern was not the end of the regex string.
        while inp_idx[0] < len(inp_str) and inp_str[inp_idx[0]] != reg_str[reg_idx[0]]:
            inp_idx[0] += 1
    else:
        # Handle incrementing the input string index when the repetition pattern was the end of the regex string.
        while inp_idx[0] < len(inp_str):
            inp_idx[0] += 1


# Return true if the repetition pattern at the current and next index in the regex string match a sequence of characters
# starting at the current index in the input string.
def match_repetition(reg_str: str, reg_idx: List[int], inp_str: str, inp_idx: List[int]) -> bool:
    # Store the repeated character and the metacharacter corresponding to the type of repetition.
    char = reg_str[reg_idx[0]]
    meta = reg_str[reg_idx[0] + 1]

    if meta == '?':
        # Handle the '?' repetition pattern which matches zero or one occurrences of the repeated character.
        if inp_str[inp_idx[0]] == char or char == wildcard:
            # If the repeated character is a match at the current index in the input string, move the index in the regex
            # string past the repetition pattern and the index in the input string past the current character.
            reg_idx[0] += 2
            inp_idx[0] += 1
        else:
            # If the repeated character is not a match at the current index in the input string, move the index in the
            # regex string past the repetition pattern.
            reg_idx[0] += 2
    elif meta == '*':
        # Handle the '*' repetition pattern which matches zero or more occurrences of the repeated character.
        if inp_str[inp_idx[0]] == char:
            # If the repeated character matches a literal character at the current index in the input string, move the
            # index in the regex string past the repetition pattern and the index in the input string past each
            # consecutive occurrence of the character.
            reg_idx[0] += 2
            while inp_str[inp_idx[0]] == char:
                inp_idx[0] += 1
        elif char == wildcard:
            # If the repeated character is a wildcard, move the index in the regex string past the repetition pattern
            # and the index in the input string past until its end is reached or a subsequent match is found in the
            # regex string.
            repeat_wildcard(reg_str, reg_idx, inp_str, inp_idx)
        else:
            # If the repeated character doesn't match the character at the current index in the input string, move the
            # index in the regex string past the repetition pattern.
            reg_idx[0] += 2
    elif meta == '+':
        # Handle the '+' repetition pattern which matches one or more occurrences of the repeated character.
        if inp_str[inp_idx[0]] == char:
            # If the repeated character matches a literal character at the current index in the input string, move the
            # index in the regex string past the repetition pattern and the index in the input string past each
            # consecutive occurrence of the character.
            reg_idx[0] += 2
            while inp_str[inp_idx[0]] == char:
                inp_idx[0] += 1
        elif char == wildcard:
            # If the repeated character is a wildcard, move the index in the regex string past the repetition pattern
            # and the index in the input string past until its end is reached or a subsequent match is found in the
            # regex string.
            repeat_wildcard(reg_str, reg_idx, inp_str, inp_idx)
        else:
            # If the repeated character doesn't match the character at the current index in the input string, the
            # pattern does not match so return false.
            return False

    # Finally, return true when the repetition pattern was determined to be a match.
    return True


# Determine if the specified regex string matches the specified input string at any location.
def match_any(reg_str: str, inp_str: str) -> bool:
    # Check for matches at the start of slices of the input string starting at each index.
    for i in range(len(inp_str)):
        if match_start(reg_str, [0], inp_str[i:], [0]):
            # If a match was found in the input string starting at the current index, i, return true.
            return True

    # If no matches were found in the input string, return false.
    return False


# Determine if the specified regex string matches the specified input string starting at its first index.
def match_start(reg_str: str, reg_idx: List[int], inp_str: str, inp_idx: List[int]) -> bool:
    # Iterate until the entire regex string has been successfully matched.
    while reg_idx[0] < len(reg_str):
        if inp_idx[0] >= len(inp_str):
            # If the entire regex string has not been matched, but the end of the input string has been reached, return
            # false.
            return False
        elif reg_idx[0] < len(reg_str) - 1 and reg_str[reg_idx[0]] != b_slash and reg_str[reg_idx[0] + 1] in rep_chars:
            # If the character at the current index in the regex string is not a backslash and the character immediately
            # following it is a repetition metacharacter, check if the repetition pattern matches the input string.
            if not match_repetition(reg_str, reg_idx, inp_str, inp_idx):
                # If the repetition pattern does not match the input string, return false.
                return False
        elif not match_literal(reg_str, reg_idx, inp_str, inp_idx):
            # If the character at the current index in the regex string does not match that of the input string, return
            # false.
            return False

    # If the entire regex string was matched, return true.
    return True


# Determine if the specified regex string matches the specified input string ending at its last index.
def match_end(reg_str: str, inp_str: str) -> bool:
    # Check for matches at the start of slices of the input string starting at each index.
    for i in range(1, len(inp_str) + 1):
        if match_start(reg_str, [0], inp_str[i:], [0]):
            # If a match was found in the input string starting at the current index, i, return true.
            return True

    # If no matches were found in the input string, return false.
    return False


# Determine if the specified regex string matches the specified input string in its entirety.
def match_all(reg_str: str, reg_idx: List[int], inp_str: str, inp_idx: List[int]) -> bool:
    if match_start(reg_str, reg_idx, inp_str, inp_idx) and inp_idx[0] == len(inp_str):
        # If the regex string was a match and the current index in the input string is out of bounds, the regex string
        # was matched to the entire input string, so return true.
        return True
    else:
        # Otherwise, the regex string only partially matched the input string.
        return False


# Determine if the specified regex string matches the specified input string.
def regex(reg_str: str, inp_str: str) -> bool:
    # Handle base cases of regex matching.
    if reg_str == '':
        # An empty regex string matches all input strings.
        return True
    elif inp_str == '':
        # No regex string matches an empty input string.
        return False

    # Call another function to handle checking if the regex string is a match depending on the presence, or lack
    # thereof, of anchor metacharacters.
    if reg_str[0] == anchor_start and reg_str[-1] == anchor_end:
        # If both the start and end anchors are in the regex string, match a slice of the regex string, ignoring those
        # characters, with the specified input string.
        return match_all(reg_str[1:len(reg_str) - 1], [0], inp_str, [0])
    elif reg_str[0] == anchor_start:
        # If only the start anchor is in the regex string, match a slice of the regex string, ignoring that character,
        # with the specified input string.
        return match_start(reg_str[1:], [0], inp_str, [0])
    elif reg_str[-1] == anchor_end:
        # If only the end anchor is in the regex string, match a slice of the regex string, ignoring that character,
        # with the specified input string.
        return match_end(reg_str[:len(reg_str) - 1], inp_str)
    else:
        # If there aren't any anchor metacharacters in the regex string, match the entire regex string with the
        # specified input string.
        return match_any(reg_str, inp_str)


# Store the user's input, split at each occurrence of the '|' character, and print whether or not the specified regex
# string matches the specified input string.
inputs = input().split('|')
print(regex(inputs[0], inputs[1]))
