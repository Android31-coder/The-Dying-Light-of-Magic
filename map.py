from pygame import *
from random import randint
from numpy import *
from PIL import Image

class Tile:
    def __init__(self, size, color):
        self.size = size
        self.tile = Surface((self.size, self.size))
        self.tile.fill(color)
        self.tag = 123

    def draw_tile(self, surface, coords):
        surface.blit(self.tile, coords)

class Map:
    def __init__(self, tile_size, image):
        self.tile_size = tile_size
        self.image = Image.open(image)
        self.pixels = self.image.load()
        self.width, self.height = self.image.size
        self.tiles = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.generate_map()

    def generate_map(self):
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[x][y] =  Tile(self.tile_size, self.pixels[x][y])

    def draw(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[x][y].draw_tile(surface, (x * self.tile_size, y * self.tile_size))