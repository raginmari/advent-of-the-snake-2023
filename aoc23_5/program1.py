import os
import re

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
    def __init__(self, src_name, dst_name):
        self.src_name = src_name
        self.dst_name = dst_name
        self.map_items = []

    def __str__(self):
        return f"Map from {self.src_name} to {self.dst_name} with {len(self.map_items)} mappings"

    def add_map_item(self, map: MapItem):
        self.map_items.append(map)

class MapItem:
    def __init__(self, mapped_range, offset):
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
            seeds = list(map(lambda x: int(x), seeds_match.group(1).split()))
        
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
    locations = list(map(lambda x: map_seed(x, maps), seeds))
    result = min(locations)
    
    return result

def create_map_item(dst_start, src_start, length):
    mapped_range = range(src_start, src_start + length)
    offset = dst_start - src_start
    
    return MapItem(mapped_range, offset)

def map_seed(seed, maps):
    v = seed
    for m in maps:
        # find first mapper that can map v; may be None in which case v is not mapped
        if mapper := next((x for x in m.map_items if x.can_map(v)), None):
            v = mapper.map(v)
            
    return v


solution = solve(puzzleInput)
print(f"solution: {solution}")
