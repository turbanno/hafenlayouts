from tools import Position
import constants

# wenn so ein Buidling nen Input bekommt:
# new Building("type" = "Bauernhaus", pos = Position()


class Building:
    def __init__(self, position, building_type, size):
        self.position = position
        self.building_type = building_type
        self.size_x, self.size_y = size[0], size[1]
        #self.size_x, self.size_y = constants.get_size_of_building(self.building_type)
        self.representation = constants.building_decoding[building_type]

    def __repr__(self):
        return f"Building {self.building_type} at {self.position.x}/{self.position.y}"

    def get_neighboring_tiles(self):
        neighboring_tiles = []




