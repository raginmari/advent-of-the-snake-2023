import os
import re
from typing import List, Tuple

# define typealiases
ListOfRaces = List[Tuple[int, int]]

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzleInput = list(map(lambda x: x.strip(), file.readlines()))

def solve(races: ListOfRaces) -> int:
    # t = time
    # d = distance to exceed
    # formula (t - x) * x > d
    result = 1
    for t, d in races:
        wins = [x for x in range(0, t + 1) if (t - x) * x > d]
        result *= len(wins)

    return result

number_pattern = r"\d+"
ts = [int(x) for x in re.findall(number_pattern, puzzleInput[0])]
ds = [int(x) for x in re.findall(number_pattern, puzzleInput[1])]
races = list(zip(ts, ds))

solution = solve(races)
print(f"solution: {solution}")
