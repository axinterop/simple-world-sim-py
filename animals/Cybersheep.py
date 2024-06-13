from .Animal import Animal
from utils import *
from plants.H_Sosnowskyi import H_Sosnowskyi

import math


class Cybersheep(Animal):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.CYBERSHEEP

        self.r = 0

    def action(self, world):
        bs = [b for b in world.organisms if isinstance(
            b, H_Sosnowskyi) and not b.is_dead()]

        if not bs:
            super().action(world)
            return

        closest_h = min(bs, key=lambda o: self.distance_to(o))
        dx, dy = self.get_direction_vector(closest_h)
        dx, dy = self.normalize_vector(dx, dy)

        new_x = self.pos[0] + int(dx)
        new_y = self.pos[1] + int(dy)
        self.set_pos((new_x, new_y))

    def class_name(self):
        return "Cybersheep"

    def distance_to(self, other):
        dx = other.pos[0] - self.pos[0]
        dy = other.pos[1] - self.pos[1]
        return math.sqrt(dx**2 + dy**2)

    def get_direction_vector(self, other):
        dx = other.pos[0] - self.pos[0]
        dy = other.pos[1] - self.pos[1]
        return dx, dy

    def normalize_vector(self, dx, dy):
        if dx > 0:
            dx = 1
        elif dx < 0:
            dx = -1
        else:
            dx = 0

        if dy > 0:
            dy = 1
        elif dy < 0:
            dy = -1
        else:
            dy = 0

        return dx, dy
