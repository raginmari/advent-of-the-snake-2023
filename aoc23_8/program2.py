import os
import re
import time
import math
from functools import reduce
from itertools import cycle
from typing import List, Tuple

# match AAA = (BBB, CCC)
node_pattern = r"(\w{3}) = \((\w{3}), (\w{3})\)"

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

def walk_path(node, nodes_by_name, guide):
    steps_taken = 0

    while True:
        steps_taken += 1

        next_node_name = node.children[next(guide)]
        if next_node_name.endswith("Z"): return steps_taken
        
        node = nodes_by_name.get(next_node_name)

def solve(input: List[str]) -> int:
    guide, nodes = parse_puzzle_input(input)
    
    # repeat the guide indefinitely
    guide_indexes = [0 if x == 'L' else 1 for x in guide]
    repeating_guide = cycle(guide_indexes)

    # build a lookup table to access nodes by name
    nodes_by_name = {x.name: x for x in nodes}

    starting_nodes = [x for x in nodes if x.name.endswith("A")]
    path_lengths = [walk_path(x, nodes_by_name, repeating_guide) for x in starting_nodes]
    result = reduce(math.lcm, path_lengths)

    return result
    
with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzle_input = list(map(lambda x: x.strip(), file.readlines()))

t0 = time.time()
solution = solve(puzzle_input)
print(f"solution took {(time.time() - t0):.3f} seconds to compute")
print(f"solution: {solution}")
