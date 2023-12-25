import os
import re
import time

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzleInput = list(map(lambda x: x.strip(), file.readlines()))

def solve(t: int, d: int) -> int:
    # t = time
    # d = distance to exceed
    # formula (t - x) * x > d
    first_win = next(x for x in range(0, t + 1) if (t - x) * x > d)
    last_win = next(x for x in range(t, -1, -1) if (t - x) * x > d)
    return last_win - first_win + 1

number_pattern = r"[\d ]+"
ts = [int("".join(x.split())) for x in re.findall(number_pattern, puzzleInput[0])]
ds = [int("".join(x.split())) for x in re.findall(number_pattern, puzzleInput[1])]
assert len(ts) == 1 and len(ds) == 1

t0 = time.time()
solution = solve(ts[0], ds[0])
# takes ~2.9 seconds on my machine with the original method implemented for star 1
# takes ~0.8 seconds on my machine with the improved method that finds the first and last winning ms values
print(f"time spent to find solution: {time.time() - t0} seconds")
print(f"solution: {solution}")
