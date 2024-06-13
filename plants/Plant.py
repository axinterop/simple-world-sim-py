from Organism import Organism
from .PlantChunk import PlantChunk


class Plant(Organism):
    def __init__(self, s, i, a, pos):
        super().__init__(s, i, a, pos)
        self.chunk = None

    def set_chunk(self, chunk: PlantChunk):
        self.chunk = chunk
