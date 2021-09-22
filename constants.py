map_encoding = {"-": "invalid", "1": "land", "2": "sea", "3": "river"}
map_decoding = {"invalid": "-", "land": "1", "sea": "2", "river": "3"}

building_decoding = {"street": "S", "house": "H", "storage_module": "s"}

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 102, 0)
GREY = (100, 100, 100)
OTHER = (100, 100, 100)
BACKGROUND = (64, 64, 64)
color_decoding = {"S": GREY, "1": GREEN, "-": BLACK, "H": RED, "s": BLUE, "2": RED}


def get_size_of_building(building_type):
    if building_type == "house":
        return 3, 3
    if building_type == "street":
        return 1, 1
    if building_type == "storage_module":
        return 4, 10

def get_ground_of_building(building_type):
    if building_type == "storage_module":
        return "land"
