from animals.Antilope import Antilope
from animals.Fox import Fox
from animals.Human import Human
from animals.Sheep import Sheep
from animals.Turtle import Turtle
from animals.Wolf import Wolf
from animals.Cybersheep import Cybersheep

from plants.Plant import Plant
from plants.PlantChunk import PlantChunk
from plants.Grass import Grass
from plants.Belladonna import Belladonna
from plants.Guarana import Guarana
from plants.Sonchus import Sonchus
from plants.H_Sosnowskyi import H_Sosnowskyi

from Organism import Organism
from WorldListener import WorldListener

from utils import OrganismType, CollisionStatus
import random
import functools


def organism_comparator(o1: Organism, o2: Organism):
    if o1.is_dead():
        return -1
    if o2.is_dead():
        return 1

    if o1.initiative == o2.initiative:
        return o1.age - o2.age
    return o1.initiative - o2.initiative


class World:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.organisms = []
        self.plant_chunks = []
        self.turn_num = 0
        self.wlistener = WorldListener()
        self.matrix = [[]]
        self.human_input = None
        self.init_organisms()
        self.update_matrix()

    def make_turn(self):
        self.organisms_cleanup()

        for this_o in self.organisms:
            if this_o.is_dead():
                continue

            this_o.action(self)

            for other_o in self.organisms:
                if this_o.id == other_o.id:
                    continue
                if other_o.is_dead():
                    continue
                if this_o.pos == other_o.pos:
                    self.react_on_collision(this_o, other_o)

            if not this_o.is_dead():
                this_o.after_turn(self)

        self.turn_num += 1
        self.update_matrix()

    def init_organisms(self):
        self.create_organism_at_random_pos(OrganismType.CYBERSHEEP)
        self.create_organism_at_random_pos(OrganismType.HUMAN)
        for _ in range(self.height * self.width // 100):
            self.create_organism_at_random_pos(OrganismType.ANTILOPE)
            self.create_organism_at_random_pos(OrganismType.FOX)
            self.create_organism_at_random_pos(OrganismType.SHEEP)
            self.create_organism_at_random_pos(OrganismType.TURTLE)
            self.create_organism_at_random_pos(OrganismType.WOLF)

            self.create_plant_chunk_at_random_pos(OrganismType.BELLADONNA)
            self.create_plant_chunk_at_random_pos(OrganismType.GRASS)
            self.create_plant_chunk_at_random_pos(OrganismType.GUARANA)
            self.create_plant_chunk_at_random_pos(OrganismType.H_SOSNOWSKYI)
            self.create_plant_chunk_at_random_pos(OrganismType.SONCHUS)

    def organisms_cleanup(self):
        for o in self.organisms:
            if o.is_dead():
                self.organisms.remove(o)
                if isinstance(o, Plant) and o.chunk:
                    o.chunk.plants_id.remove(o.id)
        for o in self.organisms:
            o.can_make_turn = True
        for ch in self.plant_chunks:
            ch.seeded_this_turn = False
        self.organisms.sort(key=functools.cmp_to_key(
            organism_comparator), reverse=True)

    def create_organism_at_pos(self, o_t: OrganismType, pos: tuple[int, int]):
        new_organism = None
        if o_t == OrganismType.ANTILOPE:
            new_organism = Antilope(4, 4, 0, pos)
        elif o_t == OrganismType.FOX:
            new_organism = Fox(3, 7, 0, pos)
        elif o_t == OrganismType.HUMAN:
            new_organism = Human(5, 4, 0, pos)
        elif o_t == OrganismType.SHEEP:
            new_organism = Sheep(4, 4, 0, pos)
        elif o_t == OrganismType.TURTLE:
            new_organism = Turtle(2, 1, 0, pos)
        elif o_t == OrganismType.WOLF:
            new_organism = Wolf(9, 5, 0, pos)
        elif o_t == OrganismType.CYBERSHEEP:
            new_organism = Cybersheep(11, 4, 0, pos)
        elif o_t == OrganismType.GRASS:
            new_organism = Grass(0, 0, 0, pos)
        elif o_t == OrganismType.BELLADONNA:
            new_organism = Belladonna(99, 0, 0, pos)
        elif o_t == OrganismType.GUARANA:
            new_organism = Guarana(0, 0, 0, pos)
        elif o_t == OrganismType.H_SOSNOWSKYI:
            new_organism = H_Sosnowskyi(10, 0, 0, pos)
        elif o_t == OrganismType.SONCHUS:
            new_organism = Sonchus(0, 0, 0, pos)

        if new_organism:
            self.organisms.append(new_organism)
            if self.turn_num == 0:
                self.wlistener.record_event(
                    f"{new_organism.class_info()} was created")
        return new_organism

    def create_organism_at_random_pos(self, o_t: OrganismType):
        pos = (random.randint(0, self.width - 1),
               random.randint(0, self.height - 1))
        while not self.is_pos_free(pos):
            pos = (random.randint(0, self.width - 1),
                   random.randint(0, self.height - 1))
        return self.create_organism_at_pos(o_t, pos)

    def create_offspring(self, p1: Organism, p2: Organism):
        if p1.get_type() != p2.get_type():
            return

        if p1.pos == p2.pos:
            new_pos = self.find_pos_near_parents(p1.prev_pos, p2.pos)
        else:
            new_pos = self.find_pos_near_parents(p1.pos, p2.pos)

        type = p1.get_type()
        self.create_organism_at_pos(type, new_pos)

    def create_plant_offspring(self, p1: Organism):
        if not p1.chunk:
            return
        if not isinstance(p1, Plant):
            return
        if p1.chunk.seeded_this_turn:
            return
        t = p1.type
        rand_id = p1.chunk.get_random_plant_id()
        for o in self.organisms:
            if o.id == rand_id:
                new_pos = self.get_free_pos_nearby(o.pos)
                if new_pos == o.pos:
                    return
                new_plant = self.create_organism_at_pos(t, new_pos)

                new_plant.set_chunk(p1.chunk)
                p1.chunk.add_plant_id(new_plant.id)
                break

    def create_plant_chunk_at_random_pos(self, o_t: OrganismType):
        plant_chunk = PlantChunk()
        plant = self.create_organism_at_random_pos(o_t)
        plant_chunk.add_plant_id(plant.id)
        self.plant_chunks.append(plant_chunk)
        plant.set_chunk(plant_chunk)

    def create_plant_chunk_at_pos(self, o_t: OrganismType, pos: tuple[int, int]):
        plant_chunk = PlantChunk()
        plant = self.create_organism_at_pos(o_t, pos)
        plant_chunk.add_plant_id(plant.id)
        self.plant_chunks.append(plant_chunk)
        plant.set_chunk(plant_chunk)

    def find_pos_near_parents(self, p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
        potential_pos = p2
        while potential_pos == p2:
            potential_pos = self.get_free_pos_nearby(p1)
        return potential_pos

    def react_on_collision(self, this_o: Organism, other_o: Organism):
        c_s = this_o.collision(other_o)

        if c_s == CollisionStatus.BREED:
            self.create_offspring(this_o, other_o)
            this_o.breed_set_pause(20)
            other_o.breed_set_pause(20)

        if c_s == CollisionStatus.ESCAPE:
            other_o.set_pos(self.get_free_pos_nearby(other_o.get_pos()))

        self.wlistener.record_collision(c_s, this_o, other_o)

    def print(self):
        self.matrix = [[" " for column in range(
            self.width)] for row in range(self.height)]
        for o in self.organisms[::-1]:
            if not o.is_dead():
                self.matrix[o.pos[0]][o.pos[1]] = str(o.class_name()[0])

        for row in self.matrix:
            for cell in row:
                print(f"{cell:2}", end=" ")
            print("|", end="")
            print()

    def update_matrix(self):
        self.matrix = [[" " for _ in range(
            self.width)] for _ in range(self.height)]
        for o in self.organisms[::-1]:
            if not o.is_dead():
                self.matrix[o.pos[1]][o.pos[0]] = o.type

    def within_worldarea(self, pos: tuple[int, int]):
        if pos[0] >= 0 and pos[0] < self.width and pos[1] >= 0 and pos[1] < self.height:
            return True
        return False

    def get_nearby_pos(self, pos, k: int = 1, check_free: bool = False):
        dx = [-1, 1, 0, 0, -1, -1, 1, 1]
        dy = [0, 0, -1, 1, -1, 1, -1, 1]
        directions = list(range(8))

        random.shuffle(directions)

        for _ in range(8):
            direction = directions.pop(0)
            potential_pos = (pos[0] + dx[direction] * k,
                             pos[1] + dy[direction] * k)

            if self.within_worldarea(potential_pos):
                if not check_free or self.is_pos_free(potential_pos):
                    return potential_pos

        return pos

    def get_random_pos_nearby(self, pos, k: int = 1):
        return self.get_nearby_pos(pos, k)

    def get_free_pos_nearby(self, pos, k: int = 1):
        return self.get_nearby_pos(pos, k, check_free=True)

    def is_pos_free(self, pos):
        for organism in self.organisms:
            if organism.pos == pos:
                return False
        return True

    def get_organism_by_type(self, organism_type):
        if organism_type == OrganismType.WOLF:
            return Wolf
        elif organism_type == OrganismType.SHEEP:
            return Sheep
        elif organism_type == OrganismType.FOX:
            return Fox
        elif organism_type == OrganismType.TURTLE:
            return Turtle
        elif organism_type == OrganismType.ANTILOPE:
            return Antilope
        elif organism_type == OrganismType.CYBERSHEEP:
            return Cybersheep
        elif organism_type == OrganismType.HUMAN:
            return Human
        elif organism_type == OrganismType.GRASS:
            return Grass
        elif organism_type == OrganismType.SONCHUS:
            return Sonchus
        elif organism_type == OrganismType.GUARANA:
            return Guarana
        elif organism_type == OrganismType.BELLADONNA:
            return Belladonna
        elif organism_type == OrganismType.H_SOSNOWSKYI:
            return H_Sosnowskyi
        else:
            return None
