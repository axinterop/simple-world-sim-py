from .Animal import Animal
from utils import *
from random import randint


class Turtle(Animal):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.TURTLE

    def action(self, world):
        if randint(0, 4) == 0:
            super().action(world)

    def class_name(self):
        return "Turtle"
