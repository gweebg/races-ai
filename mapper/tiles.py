import pygame
import os


class Tile(pygame.sprite.Sprite):

    def __init__(self, image, x, y, spritesheet):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap:

    def __init__(self, filename, spritesheet):

        self.map_h = None
        self.map_w = None

        self.tile_size = 64
        self.start_x, self.start_y = 0, 0

        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)

        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))

        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    @staticmethod
    def read_map(filename):

        gen_map = []

        with open(filename) as data:
            lines = [line.replace(' ', '').strip() for line in data.readlines()]

        for line in lines:
            gen_map.append(line)

        return gen_map

    def load_tiles(self, filename):

        tiles = []
        our_map = self.read_map(filename)

        x, y = 0, 0
        for row in our_map:
            x = 0
            for tile in row:
                if tile == ' ':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size

                elif tile == 'X':
                    tiles.append(Tile(
                        './docs/grass-ico.jpg',
                        x * self.tile_size,
                        y * self.tile_size,
                        self.spritesheet))

                elif tile == '-':
                    tiles.append(Tile(
                        './docs/cobblestone-ico.png',
                        x * self.tile_size,
                        y * self.tile_size,
                        self.spritesheet))

                elif tile == 'P':
                    tiles.append(Tile(
                        './docs/redstone-block-ico.png',
                        x * self.tile_size,
                        y * self.tile_size,
                        self.spritesheet))

                elif tile == 'F':
                    tiles.append(Tile(
                        './docs/gold-block-ico.png',
                        x * self.tile_size,
                        y * self.tile_size,
                        self.spritesheet))

                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
