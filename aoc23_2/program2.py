import os
from functools import reduce

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzleInput = map(lambda x: x.strip(), file.readlines())
    
def solve(puzzleInput: list) -> int:
    sum_of_powers = 0
    for i, game in enumerate(puzzleInput):
        required_rgb = {}
        reaches_index = game.index(':') + 2 # skip colon and following space
        reaches = game[reaches_index:].split("; ")

        for reach in reaches:
            for draw in reach.split(", "):
                count, color = draw.split()
                required_rgb[color] = max(required_rgb.get(color, 0), int(count))
                
        power = reduce(lambda x, y: x * y, required_rgb.values())
        sum_of_powers += power
        
    return sum_of_powers

solution = solve(puzzleInput)
print(f"Die Lösung ist {solution}")
