from maps import load_map
from tools import Position, Map, char_map_to_tile_map, get_size_ground_of_building
from buildings import Building

from interface import draw_map
from datetime import datetime

import random


def run():
    map_string = int(input("1 für kleinen Strand, 2 für großen Strand:\n"))
    if map_string == 1:
        map = load_map("kleiner_strand_baseline")
        get_stats_of_map(map)
    elif map_string == 2:
        map = load_map("großer_strand")
        get_stats_of_map(map)


# get a valid map and returns number of inhabitants etc
# origin top left - x downwards, y to the left https://support.wolfram.com/25330?src=mathematica
# index starts at 0

# places given building amount times on the map - if -1 is given, as many as possible will be placed
def place_random_buildings(map, building_type, amount, shuffle=True):
    total_built_buildings = 0
    size, ground_type = get_size_ground_of_building(building_type)
    for x in range(amount):
        if random.getrandbits(1):
            size = [size[1], size[0]]
        possible_tiles = map.get_possible_build_tiles(building_size=size, ground_type=ground_type)
        if shuffle:
            random.shuffle(possible_tiles)

        if len(possible_tiles) > 0:
            chosen_position = possible_tiles[0].position
            map.add_building(Building(chosen_position, building_type, size))
            amount -= 1
            total_built_buildings += 1
        else:
            return total_built_buildings


def place_random_buildings_with_iterative_reduction(map, building_type, amount):
    total_built_buildings = 0
    original_size, ground_type = get_size_ground_of_building(building_type)
    original_size = [original_size[0], original_size[1]]
    rotated_size = [original_size[1], original_size[0]]

    sizes = [original_size, rotated_size]

    for x in range(amount):

        possible_positions_1 = map.get_possible_build_positions(building_size=original_size, ground_type=ground_type)
        possible_positions_2 = map.get_possible_build_positions(building_size=rotated_size, ground_type=ground_type)
        random.shuffle(possible_positions_1)
        random.shuffle(possible_positions_2)
        possible_position_arrays = [possible_positions_1, possible_positions_2]
        adjacent_positions = map.get_empty_positions_with_neighbour_building()
        currently_chosen_rotation = random.getrandbits(1)
        built_building = False

        if len(possible_position_arrays[currently_chosen_rotation]) > 0:
            best_pos = None
            best_score = 0
            for test_position in possible_position_arrays[currently_chosen_rotation]:
                newly_occupied_positions = map.get_positions_in_area(test_position,
                                                                     Position(test_position.x +
                                                                              sizes[currently_chosen_rotation][0] - 1,
                                                                              test_position.y +
                                                                              sizes[currently_chosen_rotation][1] - 1))
                intersection_positions = [value for value in newly_occupied_positions if value in adjacent_positions]

                if len(intersection_positions) > 0:  # found position borders existing buildings
                    map.add_building(Building(test_position, building_type,
                                              sizes[currently_chosen_rotation]))

                    tmp_max_pos1 = len(
                        map.get_possible_build_positions(building_size=original_size, ground_type=ground_type))
                    tmp_max_pos2 = len(
                        map.get_possible_build_positions(building_size=rotated_size, ground_type=ground_type))
                    map.remove_building(Building(test_position, building_type,
                                                 sizes[currently_chosen_rotation]))
                    score = tmp_max_pos1 + tmp_max_pos2
                    if score >= best_score:
                        best_score = score
                        best_pos = test_position
            if best_pos is not None:
                map.add_building(Building(best_pos, building_type,
                                          sizes[currently_chosen_rotation]))

                amount -= 1
                total_built_buildings += 1
                built_building = True

        if not built_building:
            currently_chosen_rotation = 1 - currently_chosen_rotation
            if len(possible_position_arrays[currently_chosen_rotation]) > 0:
                for test_position in possible_position_arrays[currently_chosen_rotation]:
                    newly_occupied_positions = map.get_positions_in_area(test_position,
                                                                         Position(test_position.x +
                                                                                  sizes[currently_chosen_rotation][
                                                                                      0] - 1,
                                                                                  test_position.y +
                                                                                  sizes[currently_chosen_rotation][
                                                                                      1] - 1))
                    intersection_positions = [value for value in newly_occupied_positions if
                                              value in adjacent_positions]
                    if len(intersection_positions) > 0:
                        map.add_building(Building(test_position, building_type,
                                                  sizes[currently_chosen_rotation]))

                        amount -= 1
                        total_built_buildings += 1
                        built_building = True
                        break
        if not built_building:
            if len(possible_position_arrays[1]) > 0 or len(possible_position_arrays[1]) > 0:
                place_random_buildings(map, building_type, 1, shuffle=True)
            else:
                return total_built_buildings

    print(f"reached target building amount")
    return total_built_buildings


def get_stats_of_map(tiles):
    iterations = int(input("Anzahl Durchgänge:\n"))
    best = 0
    best_maps = []
    start_time = datetime.now()
    for iteration in range(0, iterations):
        tile_map = char_map_to_tile_map(tiles)
        map = Map(tile_map)
        building_type = "storage_module"

        place_random_buildings(map, building_type, 1, shuffle=True)
        num = place_random_buildings_with_iterative_reduction(map, building_type, 80)
        num += 1
        print(f"{(iteration / iterations)*100}%")
        if num > best:
            best = num
            best_maps = []
        if num == best:
            best_maps.append(map)
    print(f"bestes: {best}")
    print(f"wie oft bestes gefunden: {len(best_maps)}")
    end_time = datetime.now()
    delta_time = end_time - start_time
    print(f"{int(delta_time.total_seconds() * 1000)} ms für alle Durchgänge")
    print(f"ESC um zwischen mehreren Ergebnissen durchzuschalten")

    draw_map(best_maps, draw_with_border=True)


if __name__ == '__main__':
    run()
