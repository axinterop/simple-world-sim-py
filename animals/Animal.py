from Organism import Organism
from plants.Plant import Plant
from utils import OrganismType, CollisionStatus
from random import randint


class Animal(Organism):
    def __init__(self, s, i, a, p):
        super().__init__(s, i, a, p)

    def action(self, world):
        self.set_pos(world.get_random_pos_nearby(self.pos))

    def collision(self, other):
        if isinstance(other, Plant):
            return other.collision(self)

        if self.type == other.type:
            # Breeding is handled in World::ReactOnCollision() because it needs
            # World's fields. Not the best solution.
            if self.can_breed() and other.can_breed():
                self.revert_pos()
                return CollisionStatus.BREED

        elif self.strength >= other.strength:
            if self.is_attack_blocked(other):
                self.revert_pos()
                return CollisionStatus.BLOCK_ATTACK
            elif self.escaped_fight(other):
                return CollisionStatus.ESCAPE
            else:
                other.die()
                return CollisionStatus.KILL

        elif self.strength < other.strength:
            if self.avoided_death(other):
                self.revert_pos()
                return CollisionStatus.AVOID_DEATH
            else:
                self.die()
                return CollisionStatus.DIE

        self.revert_pos()
        return CollisionStatus.STAY

    def is_attack_blocked(self, other: Organism) -> bool:
        if self.strength >= other.strength:
            if other.type == OrganismType.TURTLE and self.strength < 5:
                return True
        return False

    def escaped_fight(self, other: Organism) -> bool:
        # `self` is an attacker
        if other.type == OrganismType.HUMAN:
            if other.immortal:
                return True
        if other.type == OrganismType.ANTILOPE:
            return bool(randint(0, 1))
        return False

    def avoided_death(self, other: Organism) -> bool:
        if self.type == OrganismType.HUMAN:
            if self.immortal:
                return True
        return False
