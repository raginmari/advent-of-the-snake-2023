import os
from math import prod
from collections import namedtuple
from itertools import product

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzleInput = list(map(lambda x: x.strip(), file.readlines()))

def solve(schematic: list) -> int:
    # stores x and y coordinates of first digit as well as actual number as string
    Number = namedtuple("Number", ["x", "y", "value"])
    num = None

    gears = {}
    for y, line in enumerate(schematic):
        for x, c in enumerate(line):
            if c.isdigit():
                # read number one digit at a time
                num = Number(num.x, num.y, num.value + c) if num else Number(x, y, c)
            else:
                if num:
                    # evaluate number and reset
                    for nx, ny in generate_neighbors(*num, schematic):
                        if schematic[ny][nx] == "*":
                            gear = gears.setdefault((nx, ny), [])
                            gear.append(int(num.value))
                            
                    num = None

    # sum up all gear ratios
    result = sum(prod(gear) for gear in gears.values() if len(gear) == 2)
    
    return result

def generate_neighbors(x, y, number, schematic):
    dx = len(number)
    max_x = len(schematic[0]) - 1
    max_y = len(schematic   ) - 1
    x0 = max(0, x - 1)
    y0 = max(0, y - 1)
    x1 = min(max_x, x + dx)
    y1 = min(max_y, y + 1)
    
    # use product() from itertools module instead of nested loops
    for nx, ny in product(range(x0, x1 + 1), range(y0, y1 + 1)):
        if ny != y or nx not in range(x, x + dx):
            yield (nx, ny)

solution = solve(puzzleInput)
print(f"Die Lösung ist {solution}")
