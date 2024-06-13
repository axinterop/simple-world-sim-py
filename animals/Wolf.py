from .Animal import Animal
from utils import *


class Wolf(Animal):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.WOLF

    def class_name(self):
        return "Wolf"
