
from .Plant import Plant
from utils import OrganismType, CollisionStatus

from random import randint


class Guarana(Plant):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.GUARANA

    def action(self, world):
        if not self.chunk:
            return
        if randint(1, 40) == 1:
            world.create_plant_offspring(self)
            self.chunk.seeded_this_turn = True

    def collision(self, other):
        other.strength += 3
        self.die()
        return CollisionStatus.BOOST_EATING

    def class_name(self):
        return "Guarana"
