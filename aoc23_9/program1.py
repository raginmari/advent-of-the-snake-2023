import os
import re
import time
from typing import List
from functools import reduce

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzle_input = list(map(lambda x: x.strip(), file.readlines()))

def predict_next_number(numbers: List[int]) -> int:
    backtrack = []
    while not all(x == 0 for x in numbers):
        backtrack.append(numbers[-1])
        numbers = list(map(lambda t: t[1] - t[0], zip(numbers, numbers[1:])))

    prediction = reduce(lambda last, b: last + b, reversed(backtrack))

    return prediction

def solve(input: List[str]) -> int:
    result = 0

    for line in input:
        numbers = list(map(lambda x: int(x), re.findall(r"[-\d]+", line)))
        result += predict_next_number(numbers)

    return result

t0 = time.time()
solution = solve(puzzle_input)
print(f"solution took {(time.time() - t0):.3f} seconds to compute")
print(f"solution: {solution}")
