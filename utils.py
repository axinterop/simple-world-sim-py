from enum import Enum
from dataclasses import dataclass


@dataclass
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class OrganismType(Enum):
    # Animals
    WOLF = 1,
    SHEEP = 2,
    FOX = 3,
    TURTLE = 4,
    ANTILOPE = 5,
    CYBERSHEEP = 6,
    # Plants
    GRASS = 7,
    SONCHUS = 8,
    GUARANA = 9,
    BELLADONNA = 10,
    H_SOSNOWSKYI = 11,
    # Player
    HUMAN = 12


class CollisionStatus(Enum):
    BREED = 1,
    KILL = 2,
    DIE = 3,
    STAY = 4,
    BLOCK_ATTACK = 5,
    ESCAPE = 6,
    AVOID_DEATH = 7,
    BOOST_EATING = 8,
    KILL_EATING = 9,
    EATED = 10,
    UNDEFINED = 11
