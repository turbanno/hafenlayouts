import pygame
import sys
from pygame.locals import *
from constants import *
from tools import tiles_to_numpy_array_representation
import math

def draw_map(maps, draw_with_border = True):
    map_index = 0

    def next_map(map):
        map_tiles = tiles_to_numpy_array_representation(map.tiles)

        scaling = 2
        largest_dimenstion = max([map_tiles.shape[0], map_tiles.shape[1]])
        window_height = int(500 * scaling)
        window_width = int(500 * scaling)
        tile_height = math.ceil((window_height / largest_dimenstion))
        tile_widht = math.ceil((window_width / largest_dimenstion))
        pygame.init()

        display = pygame.display.set_mode((window_height, window_width), 0, 32)
        display.fill(BACKGROUND)
        for row in range(map_tiles.shape[0]):
            y = row * (window_height / largest_dimenstion)
            for column in range(map_tiles.shape[1]):

                color = color_decoding[map_tiles[row][column]]
                if map_tiles[row][column] != "H":
                    x = column * (window_width / largest_dimenstion)
                    pygame.draw.rect(display, color, (x, y, tile_widht, tile_height))
                    if draw_with_border:
                        for i in range(4):
                            pygame.draw.rect(display, BLACK, (x - i, y - i, window_height, window_width), 1)

        for building in map.building_list:

            y = building.position.y * (window_height / largest_dimenstion)
            x = building.position.x * (window_width / largest_dimenstion)
            color = color_decoding[building_decoding[building.building_type]]
            width = tile_widht * building.size_y
            height = tile_height * building.size_x
            pygame.draw.rect(display, color, (y, x, width, height))
            if draw_with_border:
                for i in range(4):
                    pygame.draw.rect(display, BLACK, (y - i, x - i, width, height), 1)

    while True:
        if map_index == 0:
            next_map(maps[0])
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if map_index < len(maps)-1:
                    map_index += 1
                    next_map(maps[map_index])
                else:
                    map_index = 0
                    next_map(maps[map_index])
        pygame.display.update()
