import copy

import numpy

from constants import *
import numpy as np


class Position:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def __repr__(self):
        return f"position {self.x}-{self.y}"

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y


class Mapsize:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def __repr__(self):
        return f"mapsize {self.x}-{self.y}"


class Tile:
    # invalid(hill or outside), land, water, river # evtl special-slot?
    # 0, 1, 2, 3,
    def __init__(self, pos, tile_type):
        self.position = pos
        self.tile_type = tile_type
        self.ground = map_decoding[tile_type]
        self.representation = map_decoding[tile_type]
        self.building_on_it = None
        self.neighbors = []

    def set_building(self, building):
        self.building_on_it = building
        self.representation = building_decoding[building.building_type]
        print(f"changed representation to {self.representation}")

    def __repr__(self):
        # return f"Tile at {self.position} - icon {self.representation} -building: {self.building_on_it} - neighbors: {[el.position for el in self.neighbors]} neighbor icons: {[el.representation for el in self.neighbors]}"
        # return f"Tile at {self.position} - icon {self.representation} -building: {self.building_on_it}"
        return f"Tile at {self.position}"

    def __lt__(self, other):
        return self.position.x < other.position.x or self.position.y < other.position.y

    def is_buildable(self, type_of_ground):
        if self.building_on_it is None and self.ground == map_decoding[type_of_ground]:
            return True
        else:
            return False

    def update_icon(self):
        self.representation = self.building_on_it.representation


class Map:
    def __init__(self, tile_map):
        self.tiles = tile_map
        self.building_list = []
        self.mapsize = Mapsize(len(tile_map), len(tile_map[0]))
        # self.streets = self.build_streets()

    def get_possible_build_tiles(self, building_size, ground_type):  # TODO?
        tiles = []
        for tile in self.tiles.flatten():
            if tile.is_buildable("land") and self.is_buildable_area(tile.position, building_size, ground_type):
                tiles.append(tile)

        return np.array(tiles, dtype=Tile)

    def get_possible_build_positions(self, building_size, ground_type):
        positions = []
        for tile in self.tiles.flatten():
            if tile.is_buildable("land") and self.is_buildable_area(tile.position, building_size, ground_type):
                positions.append(tile.position)

        return np.array(positions, dtype=Position)

    def is_buildable_area(self, start_position, building_size, ground_type):
        end_position = Position(start_position.x + building_size[0] - 1, start_position.y + building_size[1] - 1)
        # print(f"start position {start_position}")
        if self.mapsize.x > end_position.x and self.mapsize.y > end_position.y:
            # print(f"end position {end_position} is valid")
            # for x in range(start_position.x, end_position.x): #ptimization by replacing this with get_tiles_in_area?
            #    for y in range(start_position.y, end_position.y):
            for tile in self.tiles[start_position.x:end_position.x + 1, start_position.y:end_position.y + 1].flatten():
                if not tile.is_buildable(ground_type):
                    return False
            return True
        else:
            # print(f"end position {end_position} is not valid")
            return False

    # start_position is top left from end_position
    def get_tiles_in_area(self, start_position, end_position):
        start_position = normalize_invalid_position(start_position, self.mapsize)
        end_position = normalize_invalid_position(end_position, self.mapsize)
        tiles_in_area = self.tiles[start_position.x:end_position.x + 1, start_position.y:end_position.y + 1].flatten()
        return tiles_in_area

    def get_positions_in_area(self, start_position, end_position):
        start_position = normalize_invalid_position(start_position, self.mapsize)
        end_position = normalize_invalid_position(end_position, self.mapsize)
        positions_in_area = self.tiles[start_position.x:end_position.x + 1, start_position.y:end_position.y + 1].flatten()
        return np.array([tile.position for tile in positions_in_area])

    # returns an array containing the position of every tile with a specific char
    def get_positions_with_specific_char(self, char):
        positions = []
        for tile in self.tiles.flatten():
            # for x in range(0, self.mapsize.x):
            #    for y in range(0, self.mapsize.y):
            if tile.representation == char:
                positions.append(Position(tile.position.x, tile.position.y))
        return positions

    def get_empty_positions_with_neighbour_building(self):
        positions = []
        for tile in self.tiles.flatten():
            if tile.building_on_it == None and tile.tile_type == "land": # tile selbst unbebaut
                #print(tile.neighbors)
                has_neighbor = False
                for neigh in tile.neighbors:
                    if neigh.building_on_it != None: # wenn nachbar ein Gebäude drauf hat
                        has_neighbor = True
                if has_neighbor:
                    positions.append(Position(tile.position.x, tile.position.y))
        return positions

    def get_empty_tiles_with_neighbour_building(self):
        tiles = []
        for tile in self.tiles.flatten():
            if tile.building_on_it == None and tile.tile_type == "land": # tile selbst unbebaut
                has_neighbor = False
                for neigh in tile.neighbors:
                    if neigh.building_on_it != None: # wenn nachbar ein Gebäude drauf hat
                        has_neighbor = True
                if has_neighbor:
                    tiles.append(tile)
        return np.array(tiles, dtype=Tile)
        #return tiles

    def add_building(self, building):
        self.building_list.append(building)
        for x in range(0, self.building_list[-1].size_x):
            for y in range(0, self.building_list[-1].size_y):
                self.tiles[self.building_list[-1].position.x + x][
                    self.building_list[-1].position.y + y].building_on_it = self.building_list[-1]
                self.tiles[self.building_list[-1].position.x + x][self.building_list[-1].position.y + y].update_icon()

    def remove_building(self, building):
        #self.building_list.remove(building)
        for x in range(0, self.building_list[-1].size_x):
            for y in range(0, self.building_list[-1].size_y):
                self.tiles[self.building_list[-1].position.x + x][
                    self.building_list[-1].position.y + y].building_on_it = None
                self.tiles[self.building_list[-1].position.x + x][self.building_list[-1].position.y + y].representation = map_decoding[self.tiles[self.building_list[-1].position.x + x][self.building_list[-1].position.y + y].tile_type]
                #self.tiles[self.building_list[-1].position.x + x][self.building_list[-1].position.y + y].update_icon()
        del self.building_list[-1]


def char_map_to_tile_map(char_map):
    tile_map = numpy.empty(shape=(len(char_map), len(char_map[0])), dtype=Tile)
    for x in range(0, len(char_map)):
        # tile_row = []
        for y in range(0, len(char_map[0])):
            tile_map[x, y] = Tile(Position(x, y), map_encoding[char_map[x][y]])
            # for ground_char, ground_name in constants.map_encoding.items():
            #    if char_map[x][y] == ground_char:
            #        #tile_row.append(Tile(Position(x, y), ground_name))
            #        tile_map[x,y] = Tile(Position(x, y), ground_name)
        # tile_map.append(tile_row)

    for x in range(0, len(char_map)):
        for y in range(0, len(char_map[0])):
            tile_map[x,y].neighbors = get_neighbour_tiles(Position(x, y), tile_map=tile_map)

    return tile_map


def tiles_to_numpy_array_representation(tile_map):
    arr = []
    for x in range(0, len(tile_map)):
        arr.append([tile.representation for tile in tile_map[x]])
    return np.array(arr)


# key add to tile map
# außerhalb der tiles wsl

# tile list ein dict?
# andererseits kann man dann kein [x] [y] machen
# über position key bestimmen?
# map.tiles[posx+"-"+posy]
# map.tiles[str(posx)+str(posy)]


def draw_map(pos_and_labels, mapsize):
    raw = []
    for x in range(0, mapsize.x):
        raw.append(["0" for el in range(0, mapsize.y)])
    for element in pos_and_labels:
        raw[element[0].x][element[0].y] = element[1]
    return raw


# if given 0-0: returns 0-1 and 1-0
def get_neighbour_positions(position, mapsize):
    adjacent_tiles = []
    if position.x + 1 <= mapsize.x - 1:
        adjacent_tiles.append(Position(position.x + 1, position.y))
    if position.x - 1 >= 0:
        adjacent_tiles.append(Position(position.x - 1, position.y))
    if position.y + 1 <= mapsize.y - 1:
        adjacent_tiles.append(Position(position.x, position.y + 1))
    if position.y - 1 >= 0:
        adjacent_tiles.append(Position(position.x, position.y - 1))
    return adjacent_tiles


def get_neighbour_tiles(position, tile_map):
    mapsize = Mapsize(len(tile_map), len(tile_map[0]))
    adjacent_tiles = []
    if position.x + 1 <= mapsize.x - 1:
        adjacent_tiles.append(tile_map[position.x + 1][position.y])
        # adjacent_tiles.append(Position(position.x + 1, position.y))
    if position.x - 1 >= 0:
        adjacent_tiles.append(tile_map[position.x - 1][position.y])
        # adjacent_tiles.append(Position(position.x - 1, position.y))
    if position.y + 1 <= mapsize.y - 1:
        adjacent_tiles.append(tile_map[position.x][position.y + 1])
        # adjacent_tiles.append(Position(position.x, position.y + 1))
    if position.y - 1 >= 0:
        adjacent_tiles.append(tile_map[position.x][position.y - 1])
        # adjacent_tiles.append(Position(position.x, position.y - 1))

    # print(len(adjacent_tiles))
    if len(adjacent_tiles) == 2 and False:
        #print(position)
        #print(f"following neibors:")
        for el in adjacent_tiles:
            print(el.position)
        # print(adjacent_tiles[0].position)
    # return []
    return adjacent_tiles


def display_map(map):
    print("###############")
    for x in range(0, len(map)):
        print("".join([tile.representation for tile in map[x]]), end="\n")
    print("###############")


def display_map_ground(map):
    print("###############")
    for x in range(0, len(map)):
        print("".join([tile.ground for tile in map[x]]), end="\n")
    print("###############")


def check_for_street(streets, position):
    for key, value in streets.items():
        if position == value["pos"]:
            return key
    return -1


def replace_street_icons(map, streets, value_type, condition, symbol):
    map = copy.deepcopy(map)
    for key, value in streets.items():
        if value[value_type] == condition:
            pos = value["pos"]
            map[pos.x][pos.y] = symbol
    return map


# accepts positions like [-1,2] and corrects them to [0, 2]
# also removes too large values when out of bounds
# tested this method for correctness
def normalize_invalid_position(position, mapsize):
    if position.x < 0:
        position.x = 0
    elif position.x > mapsize.x - 1:
        position.x = mapsize.x - 1  # maybe copy needed if mapsize changes
    if position.y < 0:
        position.y = 0
    elif position.y > mapsize.y - 1:
        position.y = mapsize.y - 1  # maybe copy needed if mapsize changes
    return position


def get_size_ground_of_building(building_type):
    size = get_size_of_building(building_type)
    ground_type = get_ground_of_building(building_type)
    return size, ground_type
