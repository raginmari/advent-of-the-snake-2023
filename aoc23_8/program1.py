import os
import re
import time
from typing import List, Tuple
from itertools import cycle

# match AAA = (BBB, CCC)
node_pattern = r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)"

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Node:
    def __init__(self, name: str, children: Tuple[str, str]):
        self.name = name
        self.children = children

    def __str__(self) -> str:
        return f"Node(name={self.name}, children={self.children})"

def parse_node(raw_node: str) -> Node:
    matched_node = re.match(node_pattern, raw_node)
    return Node(matched_node.groups()[0], matched_node.groups()[1::])

def parse_puzzle_input(input: str) -> Tuple[str, List[Node]]:
    guide = input[0]
    nodes = list(map(lambda x: parse_node(x), input[2::]))
    return (guide, nodes)
    
def solve(input: List[str]) -> int:
    guide, nodes = parse_puzzle_input(input)
    # repeat the guide indefinitely
    repeating_guide = cycle(guide)
    
    # start at "AAA"
    current_node = next(x for x in nodes if x.name == "AAA")
    assert current_node
    
    steps_taken = 0
    # nodes might be visited multiple times; build a lookup table as we go
    lut = {}

    while True:
        step = next(repeating_guide)
        steps_taken += 1

        next_node_name = current_node.children[0 if step == 'L' else 1]
        if next_node_name == "ZZZ": return steps_taken
        
        current_node = lut.setdefault(next_node_name, next(x for x in nodes if x.name == next_node_name))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzle_input = list(map(lambda x: x.strip(), file.readlines()))

t0 = time.time()
solution = solve(puzzle_input)
print(f"solution took {(time.time() - t0):.3f} seconds to compute")
print(f"solution: {solution}")
