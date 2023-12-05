import os
import re

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager"
    puzzleInput = map(lambda x: x.strip(), file.readlines())

def solve(puzzleInput: list) -> int:
    sum = 0
    for i, line in enumerate(puzzleInput):
        id = int(re.search(r"^Game (\d+)", line).group(1))

        reaches_index = line.index(':') + 2 # skip colon and following space
        reaches = line[reaches_index:].split("; ")
        
        all_draws = []
        for reach in reaches:
            all_draws.extend(reach.split(", "))

        # less readable but shorter with a nested list comprehension:
        # all_draws = [draw for reach in reaches for draw in reach.split(", ")]

        if all(is_possible_draw(all_draws)):
            sum += id
            
    return sum

limits = {"red": 12, "green": 13, "blue": 14}

# generator function
def is_possible_draw(draws):
    for draw in draws:
        count, color = draw.split()
        if int(count) <= limits[color]:
            yield True
        else:
            yield False

solution = solve(puzzleInput)
print(f"Die Lösung ist {solution}")
