import os

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager"
    puzzleInput = map(lambda x: x.strip(), file.readlines())

def solve(puzzleInput: list) -> int:
    # keep spelled out digits sorted by value
    spelled_out_digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    reversed_spelled_out_digits = list(map(lambda x: x[::-1], spelled_out_digits)) # reverse once
    solution = 0

    for line in puzzleInput:
        reversed_line = line[::-1]
        calibrationValue = first_digit_from(line, spelled_out_digits) + first_digit_from(reversed_line, reversed_spelled_out_digits)
        solution += int(calibrationValue)

    return solution

def first_digit_from(text, spelled_out_digits):
    for i, c in enumerate(text):
        if c.isdigit():
            return c
        
        for j, w in enumerate(spelled_out_digits):
            if text[i:].startswith(w):
                return str(j + 1)
            
    return ""

"""
# Falsch: aus dem subreddit: The right calibration values for string "eighthree" is 83 and for "sevenine" is 79.
def replace_spelled_out_digits(text: str) -> str:
    sod = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    result = ''
    while len(text) > 0:
        skip=1
        for i, word in enumerate(sod):
            if text.startswith(word):
                result += str(i + 1)
                skip = len(word)
                break
        
        if skip == 1:
            result += text[0]

        text = text[skip:]
        
    return result
"""

solution = solve(puzzleInput)
print(f"Die Lösung ist {solution}")
