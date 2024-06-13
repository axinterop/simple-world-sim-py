
from .Animal import Animal
from utils import CollisionStatus, OrganismType


class Antilope(Animal):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.ANTILOPE

    def action(self, world):
        self.set_pos(world.get_random_pos_nearby(self.pos, 2))

    def class_name(self):
        return "Antilope"
