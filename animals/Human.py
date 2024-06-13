
from .Animal import Animal
from utils import *


class Human(Animal):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)
        self.type = OrganismType.HUMAN
        self.immortal = False
        self.immortality_turns = 0
        self.immortality_cooldown = 0

    def action(self, world):
        if self.immortality_cooldown > 0:
            self.immortality_cooldown -= 1

        if self.immortality_turns > 0:
            self.immortality_turns -= 1
            if self.immortality_turns == 0:
                self.immortal = False
                self.immortality_cooldown = 5
                world.wlistener.record_event("Human immortality has ended.")

        if world.human_input:
            if world.human_input == "q" and self.immortality_cooldown == 0:
                self.immortal = True
                self.immortality_turns = 5
                world.wlistener.record_event(
                    "Human is now immortal for 5 turns.")
                world.human_input = None

        if world.human_input:
            if world.human_input == "w":
                self.set_pos((self.pos[0], self.pos[1] - 1))
            elif world.human_input == "s":
                self.set_pos((self.pos[0], self.pos[1] + 1))
            elif world.human_input == "a":
                self.set_pos((self.pos[0] - 1, self.pos[1]))
            elif world.human_input == "d":
                self.set_pos((self.pos[0] + 1, self.pos[1]))
            world.human_input = None  # Reset the input
        else:
            self.set_pos(world.get_random_pos_nearby(self.pos))

    def die(self):
        if not self.immortal:
            super().die()

    def class_name(self):
        return "Human"
