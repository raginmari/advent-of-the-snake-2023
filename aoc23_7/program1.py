import os
from typing import List
from enum import Enum

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# card labels: A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
label_map = {
    'A': 'Z', 
    'K': 'Y',
    'Q': 'X',
    'J': 'W',
    'T': 'V',
    '9': 'U',
    '8': 'T',
    '7': 'S',
    '6': 'R',
    '5': 'Q',
    '4': 'P',
    '3': 'O',
    '2': 'N',
}

class HandType(Enum):
    # values correspond to hand's strength
    HIGH_CARD           = 1
    ONE_PAIR            = 2
    TWO_PAIR            = 3
    THREE_OF_A_KIND     = 4
    FULL_HOUSE          = 5
    FOUR_OF_A_KIND      = 6
    FIVE_OF_A_KIND      = 7

class Play:
    def __init__(self, hand: str, bid: str):
        self.hand = hand
        self.bid = int(bid)
        self.hand_type: HandType = self._parse_hand_type(hand)
        # map card labels so that hands can be compared if hand types are equal
        self.comparable_hand = "".join(label_map[x] for x in hand)

    def _parse_hand_type(self, hand: str) -> HandType:
        labels = {}
        for c in hand:
            labels[c] = labels.get(c, 0) + 1

        unique_labels = len(labels.keys())
        highest_label_count = sorted(labels.values(), key=lambda x: -x)[0]
        if unique_labels == 1:
            return HandType.FIVE_OF_A_KIND
        elif unique_labels == 2 and highest_label_count == 4:
            return HandType.FOUR_OF_A_KIND
        elif unique_labels == 2 and highest_label_count == 3:
            return HandType.FULL_HOUSE
        elif unique_labels == 3 and highest_label_count == 3:
            return HandType.THREE_OF_A_KIND
        elif unique_labels == 3 and highest_label_count == 2:
            return HandType.TWO_PAIR
        elif unique_labels == 4 and highest_label_count == 2:
            return HandType.ONE_PAIR
        else:
            # according to the description, each hand has exactly one type, so this must be HIGH_CARD
            return HandType.HIGH_CARD
    
    def __eq__(self, other):
        if isinstance(other, Play):
            # for two Plays to be equal their hands must be equal
            return self.hand == other.hand
        raise NotImplemented

    def __lt__(self, other):
        if isinstance(other, Play):
            # if both hand types are equal, the ordering of the hands serves as tie breaker
            st, ot = self.hand_type.value, other.hand_type.value
            return st < ot or (self.comparable_hand < other.comparable_hand if st == ot else False)
        raise NotImplemented
    
    def __str__(self):
        return f"Play(hand={self.hand}, hand_type={self.hand_type}, bid={self.bid})"
    
with open("input.txt", "r") as file: # "context manager" similar to using statement in C#
    plays = list(map(lambda x: Play(*x.strip().split()), file.readlines()))
    
def solve(plays: List[Play]) -> int:
    return sum(x.bid * (i + 1) for i, x in enumerate(sorted(plays)))

print(f"solution: {solve(plays)}")

#############
### Tests ###
#############

def test_play_hand_type():
    assert Play("22222", 0).hand_type == HandType.FIVE_OF_A_KIND
    assert Play("22223", 0).hand_type == HandType.FOUR_OF_A_KIND
    assert Play("22233", 0).hand_type == HandType.FULL_HOUSE
    assert Play("22234", 0).hand_type == HandType.THREE_OF_A_KIND
    assert Play("22334", 0).hand_type == HandType.TWO_PAIR
    assert Play("22345", 0).hand_type == HandType.ONE_PAIR
    assert Play("23456", 0).hand_type == HandType.HIGH_CARD

# test_play_hand_type()
    
def test_play_hand_comparison():
    assert Play("33332", 0) > Play("2AAAA", 0)
    assert Play("77788", 0) < Play("77888", 0)
    assert Play("77788", 0) == Play("77788", 0)
    assert Play("77788", 0) != Play("77888", 0)
    
# test_play_hand_comparison()