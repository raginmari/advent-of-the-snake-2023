import os
import re
import time
from collections import namedtuple

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzleInput = list(map(lambda x: x.strip(), file.readlines()))

card_pattern = re.compile(r"(\d+):([^|]+)\|(.+)"); # matches the two groups of numbers of each card
Card = namedtuple("Card", ["number", "wins"])

def solve(raw_cards: list):
    unique_cards = [parse_card(x) for x in raw_cards]
    cards = unique_cards[::-1] # shallow copy and invert to pop() in the original order

    total_scratchcards = 0
    
    while cards:
        card = cards.pop()
        total_scratchcards += 1

        i, j = card.number, card.number + card.wins
        cards += unique_cards[i:j] # seems to be a little faster than extend() in this case
        
    return total_scratchcards

def parse_card(raw_card):
    match = card_pattern.search(raw_card)

    card_number = int(match.group(1))
    winning_numbers, numbers = map(lambda x: x.strip().split(), match.groups()[1:])
    wins = len(set(winning_numbers) & set(numbers))

    return Card(card_number, wins)

start_time = time.time()

solution = solve(puzzleInput)

total_time = time.time() - start_time
print(f"execution took a total of {total_time} seconds")

print(f"solution: {solution}")
