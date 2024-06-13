from .Plant import Plant
from utils import OrganismType, CollisionStatus

from random import randint


class Sonchus(Plant):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.SONCHUS

    def action(self, world):
        for _ in range(3):
            if randint(1, 20) == 1:
                world.create_plant_offspring(self)
                self.chunk.seeded_this_turn = True
                break

    def collision(self, other):
        return CollisionStatus.STAY

    def class_name(self):
        return "Sonchus"
