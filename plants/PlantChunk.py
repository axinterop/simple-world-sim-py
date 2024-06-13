from random import randint


class PlantChunk:
    free_id = 0

    def __init__(self):
        self.id = PlantChunk.free_id
        PlantChunk.free_id += 1
        self.seeded_this_turn = False
        self.plants_id = []

    def add_plant_id(self, value):
        self.plants_id.append(value)

    def is_empty(self):
        return self.size() == 0

    def size(self):
        return len(self.plants_id)

    def get_random_plant_id(self):
        return self.plants_id[randint(0, self.size() - 1)]
