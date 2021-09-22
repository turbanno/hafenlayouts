from file_handling import read_map_file, write_file
import constants
path_to_maps = "island_maps/"

def load_map(index):
    return read_map_file(path_to_maps + "/"+str(index)+".txt")
