import os

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager"
    puzzleInput = file.readlines()

def solve(puzzleInput) -> int:
    solution = 0
    for line in puzzleInput:
        digits = ''.join(filter(lambda c: c.isdigit(), line))
        calibrationValue = int(digits[0] + digits[-1])
        solution += calibrationValue
    return solution

solution = solve(puzzleInput)
print(f"Die Lösung ist {solution}")
