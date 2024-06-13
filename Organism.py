from utils import *

from abc import ABC, abstractmethod
from typing import Tuple


class Organism(ABC):
    free_id = 0

    def __init__(self, strength: int, initiative: int, age: int, pos: Tuple[int, int]):
        self.id = Organism.free_id
        Organism.free_id += 1
        self.type = None
        self.strength = strength
        self.initiative = initiative
        self.age = age
        self.prev_pos = None
        self.pos = pos
        self.breed_pause = 0
        self.has_free_pos_nearby = True
        self.can_make_turn = False

    def get_type(self):
        return self.type

    def get_older(self):
        self.age += 1

    def die(self):
        self.age = -1

    def is_dead(self) -> bool:
        return self.age == -1

    def set_pos(self, new_pos: Tuple[int, int]):
        self.prev_pos = self.pos
        self.pos = new_pos

    def get_pos(self):
        return self.pos

    def revert_pos(self):
        self.pos = self.prev_pos

    def breed_decrease_pause(self):
        if self.breed_pause > 0:
            self.breed_pause -= 1

    def breed_set_pause(self, value: int):
        self.breed_pause = value

    def can_breed(self) -> bool:
        return self.breed_pause == 0

    def after_turn(self, world):
        self.get_older()
        self.breed_decrease_pause()

    @abstractmethod
    def action(self, world):
        pass

    @abstractmethod
    def collision(self, other):
        pass

    @abstractmethod
    def class_name(self) -> str:
        pass

    def class_info(self) -> str:
        return f"{self.class_name()}[{self.id}]{{{self.strength},{self.initiative}}}"
