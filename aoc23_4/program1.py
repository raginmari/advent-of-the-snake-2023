import os
import re
from collections import namedtuple

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzleInput = list(map(lambda x: x.strip(), file.readlines()))

card_pattern = re.compile(r":([^|]+)\|(.+)"); # matches the two groups of numbers of each card
Card = namedtuple("Card", ["winning_numbers", "numbers"])

def solve(raw_cards: list):
    score = 0

    for card in [parse_card(x) for x in raw_cards]:
        my_winning_numbers_count = len(set(card.winning_numbers) & set(card.numbers))
        score += 2 ** (my_winning_numbers_count - 1) if my_winning_numbers_count > 0 else 0

    return score

def parse_card(raw_card):
    match = card_pattern.search(raw_card)
    winning_numbers, numbers = map(lambda x: x.strip().split(), match.groups())

    return Card(winning_numbers, numbers)

solution = solve(puzzleInput)
print(f"Die Lösung ist {solution}")
