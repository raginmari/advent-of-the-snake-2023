import os
import re
from typing import List, Tuple # used to declare parameter and return types

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    puzzleInput = list(map(lambda x: x.strip(), file.readlines()))

seeds_pattern = re.compile(r"seeds: ([\d ]+)")
map_head_pattern = re.compile(r"^(\w+)-to-(\w+) map")
map_item_pattern = re.compile(r"(\d+) (\d+) (\d+)")

# forward declaration because why not?
class MapItem:
    pass

class Map:
    def __init__(self, src_name: str, dst_name: str):
        self.src_name = src_name
        self.dst_name = dst_name
        self.map_items: List[MapItem] = []

    def __str__(self):
        return f"Map from {self.src_name} to {self.dst_name} with {len(self.map_items)} mappings"

    def add_map_item(self, map: MapItem):
        self.map_items.append(map)

class MapItem:
    def __init__(self, mapped_range: range, offset: int):
        self.mapped_range = mapped_range
        self.offset = offset

    def __str__(self):
        return f"MapItem mapping from {self.mapped_range} by {self.offset}"
    
    def can_map(self, value):
        return value in self.mapped_range
    
    def map(self, value):
        return value + self.offset if self.can_map(value) else value

def solve(almanac: list):
    seeds, maps = [], []
    
    # parse input to find seeds and build maps
    for line in almanac:
        if not seeds and (seeds_match := seeds_pattern.match(line)):
            seed_values = list(map(lambda x: int(x), seeds_match.group(1).split()))
            seed_value_pairs = [(seed_values[i], seed_values[i + 1]) for i in range(0, len(seed_values), 2)]
            seeds = list(map(lambda x: range(x[0], x[0] + x[1]), seed_value_pairs))
        
        elif map_head_match := map_head_pattern.match(line):
            # create another map; that last map in the list is the "current map" to which map items are added
            src = map_head_match.group(1)
            dst = map_head_match.group(2)
            maps.append(Map(src, dst))
            
        elif map_item_match := map_item_pattern.match(line):
            assert maps # must not be empty
            current_map = maps[-1]
            
            # create another map item for the current map
            params = list(map(lambda x: int(x), map_item_match.groups()))
            map_item = create_map_item(*params)

            current_map.add_map_item(map_item)
            
    # map all seeds and return minimum location
    final_ranges = []
    for seed_range in seeds:
        final_ranges.extend(map_seed_range2(seed_range, maps))
        
    locations = map(lambda x: x.start, final_ranges)
    result = min(locations)
    
    return result

def create_map_item(dst_start, src_start, length):
    mapped_range = range(src_start, src_start + length)
    return MapItem(mapped_range, dst_start - src_start)

def intersect_range(a: range, b: range) -> range | None:
    if a.stop <= b.start or b.stop <= a.start:
        return None # empty
    return range(max(a.start, b.start), min(a.stop, b.stop))

def split_range(split: range, splitting: range) -> Tuple[range | None, range | None]:
    assert splitting.start >= split.start and splitting.stop <= split.stop
    head = range(split.start, splitting.start) if split.start != splitting.start else None
    tail = range(splitting.stop, split.stop) if splitting.stop != split.stop else None
    return (head, tail)

def map_seed_range2(seeds: range, maps: List[Map]):
    for_next_map = [ seeds ]
    for map in maps:
        to_map = for_next_map.copy()
        for_next_map = []
        mapped = []
        while to_map:
            
            # TODO popping the first element is inefficient (depending on the collection size)
            next = to_map.pop(0)

            for map_item in map.map_items:
                ix = intersect_range(next, map_item.mapped_range)
                if ix:
                    next_mapped = range(ix.start + map_item.offset, ix.stop + map_item.offset)
                    mapped.append(next_mapped)

                    head, tail = split_range(next, ix)
                    if head: to_map.append(head)
                    if tail: to_map.append(tail)

                    # indicate that element was mapped by None-ing it
                    # TODO find a better solution
                    next = None

                    break

            # this range was not mapped but must move on to the next round
            if next: mapped.append(next)

        # all mapped ranges move on to the next round
        for_next_map = mapped.copy()
    
    return for_next_map

solution = solve(puzzleInput)
print(f"solution: {solution}")

#############
### Tests ###
#############

def test_intersect_range():
    # test empty intersection
    assert intersect_range(range(0, 3), range(3, 6)) is None
    assert intersect_range(range(0, 3), range(4, 6)) is None
    assert intersect_range(range(3, 6), range(0, 3)) is None
    assert intersect_range(range(4, 6), range(0, 3)) is None
    
    # test intersection when ranges are equal
    assert intersect_range(range(0, 3), range(0, 3)) == range(0, 3)
    
    # test intersection when one range contains the other
    assert intersect_range(range(0, 5), range(1, 4)) == range(1, 4)
    assert intersect_range(range(1, 4), range(0, 5)) == range(1, 4)
    
    # test regular intersection
    assert intersect_range(range(0, 5), range(2, 7)) == range(2, 5)
    assert intersect_range(range(2, 7), range(0, 5)) == range(2, 5)
    
def test_split_range():
    # test splitting when ranges are equal
    assert split_range(range(0, 5), range(0, 5)) == (None, None)

    # test splitting at front of given range
    assert split_range(range(0, 5), range(0, 3)) == (None, range(3, 5))

    # test splitting at end of given range
    assert split_range(range(0, 5), range(3, 5)) == (range(0, 3), None)

    # test regular split
    assert split_range(range(0, 10), range(3, 7)) == (range(0, 3), range(7, 10))

# test_intersect_range()
# test_split_range()