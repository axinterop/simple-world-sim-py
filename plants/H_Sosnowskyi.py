from .Plant import Plant
from utils import OrganismType, CollisionStatus

from random import randint


class H_Sosnowskyi(Plant):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.H_SOSNOWSKYI

    def action(self, world):
        if randint(1, 40) == 1:
            world.create_plant_offspring(self)
            self.chunk.seeded_this_turn = True

    def collision(self, other):
        if other.type == OrganismType.CYBERSHEEP:
            self.die()
            return CollisionStatus.EATED

        if other.strength < self.strength:
            self.die()
            other.die()
            return CollisionStatus.KILL_EATING
        return CollisionStatus.STAY

    def class_name(self):
        return "H_Sosnowskyi"
