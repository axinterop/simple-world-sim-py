from .Plant import Plant
from utils import OrganismType, CollisionStatus

from random import randint


class Grass(Plant):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.GRASS

    def action(self, world):
        if randint(1, 20) == 1:
            world.create_plant_offspring(self)
            self.chunk.seeded_this_turn = True

    def collision(self, other):
        return CollisionStatus.STAY

    def class_name(self):
        return "Grass"
