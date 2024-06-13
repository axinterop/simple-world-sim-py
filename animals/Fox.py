
from .Animal import Animal
from utils import *


class Fox(Animal):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.FOX

    def action(self, world):
        enemy_avoided = False
        potentialPos = world.get_random_pos_nearby(self.pos)
        for other_o in world.organisms:
            while potentialPos == other_o.pos and self.strength < other_o.strength:
                potentialPos = world.get_random_pos_nearby(self.pos)
                enemy_avoided = True
        if enemy_avoided:
            pass
        self.set_pos(potentialPos)

    def class_name(self):
        return "Fox"
