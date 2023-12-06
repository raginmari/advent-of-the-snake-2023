import os

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzleInput = list(map(lambda x: x.strip(), file.readlines()))

def solve(schematic: list) -> int:
    result = 0

    # stores x and y coordinates of first digit as well as actual number as string
    number = None

    for y, line in enumerate(schematic):
        for x, c in enumerate(line):
            if c.isdigit():
                # read number one digit at a time
                number = (number[0], number[1], number[2] + c) if number else (x, y, c)
            else:
                if number:
                    # evaluate number and reset
                    result += int(number[2]) if is_part(*number, schematic) else 0 # hint: * implicitly unpacks tuple
                    number = None
                
    return result

def is_part(x, y, number, schematic):
    return any(is_symbol(neighbor) for neighbor in generate_neighbors(x, y, number, schematic))

def is_symbol(x):
    return not x.isdigit() and not x == "."

def generate_neighbors(x0, y, number, schematic):
    w = len(schematic[0]) - 1
    # this returns coordinates multiple times if numbers have more than one digit
    for x in range(x0, x0 + len(number)):
        # i don't like all those checks here...
        if x > 0 and y > 0:
            yield schematic[y - 1][x - 1]
        if x > 0 and y < w:
            yield schematic[y + 1][x - 1]
        if x > 0:
            yield schematic[y    ][x - 1]
        if x < w and y > 0:
            yield schematic[y - 1][x + 1]
        if x < w and y < w:
            yield schematic[y + 1][x + 1]
        if x < w:
            yield schematic[y    ][x + 1]
        if y < w:
            yield schematic[y + 1][x    ]
        if y > 0:
            yield schematic[y - 1][x    ]
            
solution = solve(puzzleInput)
print(f"Die Lösung ist {solution}")
