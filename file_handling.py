def read_map_file(path):
    with open(path) as f:
        lines = f.readlines()
    for x in range(0, len(lines)):
        lines[x] = list(lines[x])[:-1]
    return lines


# creates or overwrites a file with given text
def write_file(path, content):
    f = open(path, "w")
    for line in content:
        f.write(line+"\n")
    f.close()


