import re

def check_overflows(file_name):

    '''
    @gt
    this function takes in as a parameter a benchmark
    returns True if there are overflows
    False otherwise
    :param file_name: str
    :return bool
    '''

    nodes = {}
    overflows = {}
    rows = []
    max_width = 0

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):
                    
            line = line.strip()
            if line:
                if line.split()[0] == "Coordinate":
                    starting_height = line.split()[2]
                if line.split()[0] == "Height":
                    ending_height = int(starting_height) + int(line.split()[2])
                    line_height = line.split()[2]
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = line.split()[2]
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    if ending_x > max_width:
                        max_width = ending_x
                    rows.append([starting_x,starting_height,ending_x,ending_height])

    max_height = rows[-1][3]
    
    chip_size = float(max_height * max_width)


    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
                                                                                            
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if len(line.split()) == 3:
                        nodes[line.split()[0]] = []
                        nodes[line.split()[0]].append(int(line.split()[1]))
                        nodes[line.split()[0]].append(int(line.split()[2]))

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):
                
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in nodes:
                        nodes[line.split()[0]].append(int(line.split()[1]))
                        nodes[line.split()[0]].append(int(line.split()[2]))

    for node in nodes.values():
        if node[2] <= 0 or node[3] <= 0 or node[0] + node[2] >= max_width or node[1] + node[3] >= max_height:
            return True

    return False