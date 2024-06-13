
from .Animal import Animal
from utils import *


class Sheep(Animal):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.SHEEP

    def class_name(self):
        return "Sheep"
