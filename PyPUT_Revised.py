def check_move_validity(pl_file_name, node_name, new_ly, new_lx):
    """
    @gk
    This function takes as input a benchmark's pl file and a new node to be moved.
    For the node it takes its name and the new, low_y and low_x.
    Then it checks for overflow and overlaps and returns a boolean.
    False if the move is not valid, True otherwise.

    Revision: OLD --> REVISED.
    pl_file_name = path.pl --> pl_file_name = path
    Cut down statements to min form and removed unnecessary vars --> smaller file size, possibly time
    Added case for invalid node name

    REVISED | NO KNOWN BUGS
    """

    overflow = False
    overlap = False 
    data = []
    given_node = [float(new_ly), float(new_lx)]
    nodes = {}
    lines = {}
    line_key = 0
    name_flag = False

    with open(pl_file_name + '.pl') as p:
        for num, line in enumerate(p):
            if not (num == 0 or '#' in line or line == '\n'):
                data = line.split()
                if data[0] != node_name:
                    nodes[data[0]] = [float(data[2])]
                    nodes[data[0]].append(float(data[1]))
                else:
                    name_flag = True
    
    if name_flag is False:
        print('NODE NAME NOT FOUND!')
        return None

    
    with open(pl_file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if not (num == 0 or '#' in line or line == '\n' or 'NumNodes' in line or 'NumTerminals' in line):
                data = line.split()
                if data[0] == node_name:
                    given_node.append(float(data[2]))
                    given_node.append(float(data[1]))
                else:
                    nodes[data[0]].append(float(data[2]))
                    nodes[data[0]].append(float(data[1]))

    line_counter = ly = sp = 0
    with open(pl_file_name + '.scl') as s:
        for num, line in enumerate(s):
            if not ('#' in line or line == '\n' or 'NumRows' in line):
                if 'CoreRow' in line:
                    line_counter += 1
                if 'Coordinate' in line:
                    data = line.split()
                    ly = float(data[2])
                    lines[line_counter] = [ly]
                if 'Height' in line:
                    data = line.split()
                    lines[line_counter].append(float(data[2]) + ly)
                if 'Sitespacing' in line:
                    data = line.split()
                    sp = float(data[2])
                if 'SubrowOrigin' in line:
                    data = line.split()
                    lines[line_counter].append(float(data[2]))
                    lines[line_counter].append(float(data[5]) * sp + float(data[2]))

    for l in lines.items():
        if l[1][0] <= given_node[0] <= l[1][1] and l[1][0] <= given_node[0] + given_node[2] <= l[1][1]\
                and l[1][2] <= given_node[1] <= l[1][3] and l[1][2] <= given_node[1] + given_node[3] <= l[1][3]:
            line_key = l[0]

    if line_key == 0:
        overflow = True

    for n in nodes.items():
        if given_node[0] >= n[1][0] + n[1][2] and given_node[1] >= n[1][1] + n[1][3]\
                and given_node[0] + given_node[2] <= n[1][0] and given_node[1] + given_node[3] <= n[1][1]:
            continue
        else:
            overlap = True
        if overlap is True:
            break

    validity = overlap and overflow
    return not validity


def check_non_terminal(nodes_file, node_name):
    """
    @gk
    Function takes as input the file's name and the node's name.
    It pinpoints the line of the node. Then searches for the string
    terminal. It returns True if there is no terminal string after
    the name of the node.
    
    REVISION
    Changed input variable names.
    Added case for invalid name.
    Input format is now path/name it was path/name.nodes

    REVISED | NO KNOWN BUGS
    """

    name_flag = False
    data = []
    with open(nodes_file + '.nodes') as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if node_name == data[0]:
                    name_flag = True
                    if 'terminal' in line:
                        return False
    
    if name_flag is False:
        print('NODE NAME NOT FOUND!')
        return None

    return True


def check_terminal(nodes_file, node_name):
    """
    @gk
    Function takes as input the file's name and the node's name.
    Pinpoints the line of the node name , returns true if the string
    terminal is in the same line.

    REVISION
    Changed input variable names.
    Added case for invalid name.
    Input format is now path/name.

    REVISED | NO KNOWN BUGS
    """

    data = []
    name_flag = False
    with open(nodes_file + '.nodes') as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if node_name == data[0]:
                    name_flag = True
                    if 'terminal' in line:
                        return True

    if name_flag is False:
        print('NODE NAME NOT FOUND!')
        return None

    return False


def classify_by_weight(wts_file):
    """
    @gk
    This function takes as input .wts file's name and
    returns the weight of all nodes in a dictionary
    dictionary --> {node's name: [weight]}.

    REVISION
    Removed unused variables.
    File name input changed as the rest.

    REVISED | NO KNOWN BUGS
    """

    nodes = {}
    data = []
    with open(wts_file + '.wts') as wf:
        for num, line in enumerate(wf):
            if not (num == 0 or '#' in line or line == '\n'):
                data = line.split()
                nodes[data[0]] = [float(data[1])]

    return nodes



def density_in_coordinates(pl_file_name, low_y, low_x, high_y, high_x):
    """
    @gk
    This function takes as input a benchmarks pl file , and 4 coordinates
    to signify an area , low_x, low_y, high_x, high_y.
    It calculates the area of the given coordinates and finds the nodes in that area.
    returns the density by dividing the total node area by the area given.

    REVISION
    FIXED Know_Bug: Its not calculating terminal nodes in density anymore
    Using check_non_terminal function... makes it slower.

    REVISED | NO KNOWN BUGS 
    """

    nodes_area = 0.0
    data = []
    nodes = {}

    if (high_x < 0 or low_x < 0 or high_y < 0 or low_y < 0):
        print('Density is calculated in lines (positive values)!')
        return None

    area = float((high_x - low_x)) * float((high_y - low_y))

    with open(pl_file_name + '.pl') as p:
        for num, line in enumerate(p):
            if not (num == 0 or '#' in line or line == '\n'):
                data = line.split()
                if check_non_terminal(pl_file_name, data[0]):
                    nodes[data[0]] = [float(data[1])]
                    nodes[data[0]].append(float(data[2]))

    with open(pl_file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if not (num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line):
                data = line.split()
                if check_non_terminal(pl_file_name, data[0]):
                    nodes[data[0]].append(float(data[1]))
                    nodes[data[0]].append(float(data[2]))
                
    for cell in nodes.items():
        if not (low_x <= cell[1][0] < high_x and low_y <= cell[1][1] < high_y):
            data.append(cell[0])

    for i in range(len(data)):
        nodes.pop(data[i], None)

    for n in nodes.items():
        nodes_area += n[1][2] * n[1][3]

    return nodes_area / area



def density_per_row(file_name):
    """
    @gk
    This function takes as input the name of an .scl file in string form
    and it returns the density of all lines of the design in a dictionary of floats.
    Form of dictionary: density {line number: line density}

    REVISION
    FIXED bug: Density{} now shows the last line, before it did not

    REVISED | NO KNOWN BUGS
    """

    number_of_lines = 0
    line_counter = 0
    data = []
    lines = {}
    nodes = {}
    lx = rx = ly = uy = height = width = 0

    with open(file_name + '.scl') as sf:
        for num, line in enumerate(sf):
            if 'NumRows' in line:
                data = line.split()
                number_of_lines = int(data[2])
            if 'CoreRow' in line:
                line_counter += 1
                if line_counter == number_of_lines + 1:
                    break
            if 'Coordinate' in line:
                data = line.split()
                ly = float(data[2])
            if 'Height' in line:
                data = line.split()
                height = float(data[2])
                uy = ly + height
            if 'SubrowOrigin' in line:
                data = line.split()
                lx = float(data[2])
                width = float(data[5])
                rx = lx + width * 1
            lines[line_counter] = [ly]
            lines[line_counter].append(uy)
            lines[line_counter].append(lx)
            lines[line_counter].append(rx)
            lines[line_counter].append(width)

    with open(file_name + '.pl') as p:
        for num, line in enumerate(p):
            if not (num == 0 or '#' in line or line == '\n'):
                data = line.split()
                lx = float(data[1])
                ly = float(data[2])
                nodes[data[0]] = [lx]
                nodes[data[0]].append(ly)

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if not (num == 0 or '#' in line or line == '\n' or 'NumNodes' in line or 'NumTerminals' in line):
                data = line.split()
                nodes[data[0]].append(float(data[1]))
                nodes[data[0]].append(float(data[2]))

    density = {k: 0 for k in range(number_of_lines + 1)}
    s = 0
    widths = []
    for l in lines.items():
        for n in nodes.items():
            if (l[1][2] <= n[1][0] < l[1][3]) and (l[1][0] <= n[1][1] < l[1][1]):
                s = density[l[0]]
                s += n[1][3] 
                density[l[0]] = s
        widths.append(l[1][4])
    
    del widths[0]
    del density[0]
    del lines[0]

    counter_width = -1
    counter_den = 0
    for d in density.items():
        counter_width += 1
        counter_den += 1
        s = d[1]
        s = s / float(widths[counter_width])
        density[counter_den] = s

    return density


def find_similar_cells(nodes_file_name, node_name):
    """
    @gk
    This function takes as input a benchmarks node file
    and a node's name and returns a list of the nodes similar to the
    given one in width and height.

    REVISION
    Function does not return the given node in results.
    Invalid input name check.

    REVISED | NO KNOWN BUGS
    """

    data = []
    nodes = {}
    result = []

    with open(nodes_file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if not (num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line):
                data = line.split()
                nodes[data[0]] = [float(data[1])]
                nodes[data[0]].append(float(data[2]))

    given_node = nodes.get(node_name)
    if (given_node is None):
        print('NODE NAME NOT FOUND!')
        return None
    
    for n in nodes.items():
        if n[0] == node_name:
            continue
        elif n[1][0] == given_node[0] and n[1][1] == given_node[1]:
            result.append(n[0])

    return result


def find_similar_set_of_cells(nodes_file_name, node_names):
    """
    @gk
    This function takes as input a benchmarks nodes file and
    a list of nodes to search. It returns the names of the similar nodes
    according to width and height in a dictionary. The dictionary has as keys
    the names of the given nodes and as values the names of the similar nodes.

    REVISION
    Added: if a given node is non-existand then the function works for the rest of the list.
            Also gives feedback. The message will be on TOP.

    REVISED | NO KNOWN BUGS
    """

    data = []
    nodes = {}
    nodes_cp = {}
    flag_array = [False for n in node_names]

    with open(nodes_file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if not (num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line):
                data = line.split()
                nodes[data[0]] = [float(data[1])]
                nodes[data[0]].append(float(data[2]))
        
    flag_counter = 0
    for n in node_names:
        for i in nodes.items():
            if n == i[0]:
                flag_array[flag_counter] = True
                nodes_cp[n] = [i[1][0]]
                nodes_cp[n].append(i[1][1])
        flag_counter += 1

    for f in range(len(flag_array)):
        if flag_array[f] is False:
            print(node_names[f], 'NODE DOES NOT EXIST IN FILE!\n')

    cells_set = nodes_cp.copy()
    cells_set = cells_set.fromkeys(cells_set, [])
    for nc in nodes_cp.items():
        for n in nodes.items():
            if nc[0] == n[0]:
                continue
            elif nc[1][0] == n[1][0] and nc[1][1] == n[1][1]:
                cells_set[nc[0]].append(n[0])

    return cells_set


def get_coordinates(file_name, node_name):
    """
    @gk
    This function takes as input a pl-file's name and a node's name
    and returns an int-type list of the coordinates.
    list's form : [x-coordinate, y-coordinate].

    REVISION
    Added invalid name check.

    REVISED | NO KNOWN BUGS
    """

    coordinates = []
    with open(file_name + '.pl') as p:
        for num, line in enumerate(p):
            if node_name in line:
                data = line.split()
                if node_name == data[0]:
                    coordinates.append(float(data[1]))
                    coordinates.append(float(data[2]))
                    break
    
    if len(coordinates) == 0:
        print('NODE NAME NOT FOUND!')
        return None
    
    return coordinates


def get_coordinates_row(file_name, chip_row_number):
    """
    @gk
    This function takes as input the name of a .pl file as a string
    and the row's number of a chip and returns a dictionary with
    the coordinates of the chip's nodes.
    Form of dictionary: chip_coordinates = {'node's name': [x,y,width,height]}

    REVISION
    Reading the chip's lines Bug Fix

    REVISED | NO KNOWN BUGS
    """

    data = []
    lines = {}
    nodes = {}
    lx = rx = ly = uy = height = width = counter = 0

    with open(file_name + '.scl') as s:
        for num, line in enumerate(s):
            if 'CoreRow' in line:
                counter += 1
            if counter == chip_row_number:
                if 'Coordinate' in line:
                    data = line.split()
                    ly = float(data[2])
                if 'Height' in line:
                    data = line.split()
                    height = float(data[2])
                    uy = ly + height
                if 'SubrowOrigin' in line:
                    data = line.split()
                    lx = float(data[2])
                    width = float(data[5])
                    rx = lx + width * 1
                    lines[counter] = [ly]
                    lines[counter].append(uy)
                    lines[counter].append(lx)
                    lines[counter].append(rx)
            elif counter == chip_row_number + 1:
                # Stop unecessary loops
                break

    with open(file_name + '.pl') as p:
        for num, line in enumerate(p):
            if not(num == 0 or '#' in line or line == '\n'):
                data = line.split()
                lx = float(data[1])
                ly = float(data[2])
                nodes[data[0]] = [lx]
                nodes[data[0]].append(ly)

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if not (num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line):
                data = line.split()
                nodes[data[0]].append(float(data[1]))
                nodes[data[0]].append(float(data[2]))

    chip_coordinates = {k: 0 for k in nodes.keys()}
    for l in lines.items():
        for n in nodes.items():
            if(l[1][2] <= n[1][0] < l[1][3]) and (l[1][0] <= n[1][1] < l[1][1]):
                chip_coordinates[n[0]] = n[1]
            else:
                del chip_coordinates[n[0]]

    return chip_coordinates


def get_coordinates_net(file_name, net_name):
    """
    @gk
    This function takes as input a .nets file's name and the name of a net
    and returns a dictionary of nodes and their coordinates
    dictionary's form: {'node's name': ['x','y'], ...}

    REVISION
    NO major changes.

    REVISED | NO KNOWN BUGS
    """

    net = {}
    net_name_number = int(net_name.replace('n', ''))
    nodes_in_net_num = 0
    node_names = []
    data = []
    pos = 0
    counter = -1

    with open(file_name + '.nets') as n:
        for num, line in enumerate(n):
            if 'NetDegree' in line:
                counter += 1
                if counter == net_name_number:
                    pos = num
                    data = line.split()
                    nodes_in_net_num = data[2]
                    break

    with open(file_name + '.nets') as n:
        for num, line in enumerate(n):
            if pos < num <= pos + int(nodes_in_net_num):
                data = line.split()
                node_names.append(data[0])

    data.clear
    with open(file_name + '.pl') as p:
        for num, line in enumerate(p):
            if not (num == 0 or '#' in line or line == '\n'):
                data.append(line.split())

    for i in node_names:
        for j in data:
            print(i, j[0])
            if i == j[0]:
                net[i] = [j[1]]
                net[i].append(j[2])

    return net


def get_info_non_terminal_number_2(file_name, node_name):
    """
    @gk
    This function takes as input a benchmark's node file name
    and the name of a node and returns a list with the width and the height
    as floats --> [width, height].

    REVISION:
    False node_name input case fixed

    REVISED | NO KNOWN BUGS
    """

    data = []
    node = []
    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if data[0] == node_name:
                    if 'terminal' in line or 'terminal_NI' in line:
                        print('Given Node is Terminal')
                        return False
                    else:
                        node.append(float(data[1]))
                        node.append(float(data[2]))
                        break
    
    if len(node) == 0:
        print('Given node does not exist')
    return node


def get_info_terminal_number_2(file_name, node_name):
    """
    @gk
    This function takes as input a benchmarks nodes file
    and a nodes name and returns a list of the given node's
    width and height if the node is terminal else it returns false
    [width, height] --> [float, float].
    
    REVISION:
    False node_name input case fixed

    REVISED | NO KNOWN BUGS
    """

    data = []
    node = []

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if data[0] == node_name:
                    if 'terminal' in line or 'terminal_NI' in line:
                        node.append(float(data[1]))
                        node.append(float(data[2]))
                        break
                    else:
                        print('Given Node is non-Terminal')
                        return False

    if len(node) == 0:
        print('Given node does not exist')
    return node


def get_net_info(file_name, net_name):
    """
    @gk
    This function takes as input a benchmarks nets file
    and a nets name , and returns a dictionary with the net's
    nodes info --> dictionary {'node_name': [low_x, low_y, width, height, movetype]}

    REVISION:
    No major changes

    REVISED | NO KNOWN BUGS
    """
    net = {}
    net_name_number = int(net_name.replace('n', ''))
    nodes_in_net_num = 0
    node_names = []
    data = []
    pos = 0
    counter = -1

    with open(file_name + '.nets') as n:
        for num, line in enumerate(n):
            if 'NetDegree' in line:
                counter += 1
                if counter == net_name_number:
                    pos = num
                    data = line.split()
                    nodes_in_net_num = int(data[2])
                    break

    with open(file_name + '.nets') as n:
        for num, line in enumerate(n):
            if pos < num <= pos + int(nodes_in_net_num):
                data = line.split()
                node_names.append(data[0])
    data.clear()

    with open(file_name + '.pl') as p:
        for num, line in enumerate(p):
            if not(num == 0 or '#' in line or line == '\n'):
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net[i] = [j[1]]
                net[i].append(j[2])
    data.clear()

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if not(num == 0 or '#' in line or line == '\n' or 'NumNodes' in line or 'NumTerminals' in line):
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net[i].append(j[1])
                net[i].append(j[2])
                if len(j) == 4:
                    net[i].append(j[3])
                else:
                    net[i].append('non-terminal')

    return net

def get_node_info(file_name, node_name):
    """
    @gk
    This function takes as input the name of the node
    and a benchmarks nodes file name and returns info about the node
    info returned --> [width, height, low_x, low_y, movetype]
   
    REVISION:
    Added False name input case

    REVISED | NO KNOWN BUGS

    """

    data = []
    node = []
    mvtype = ''
    flag = False

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if node_name == data[0]:
                    node.append(float(data[1]))
                    node.append(float(data[2]))
                    if 'terminal' in line:
                        mvtype = 'terminal'
                    elif 'terminal_NI' in line:
                        mvtype = 'terminal_NI'
                    else:
                        mvtype = 'non-terminal'
                    
                    flag = False
                    break
            else:
                flag = True

    if flag is True:
        print('Node not found in file!')
        return None
    
    with open(file_name + '.pl') as p:
        for num, line in enumerate(p):
            if node_name in line:
                data = line.split()
                if node_name == data[0]:
                    node.append(float(data[1]))
                    node.append(float(data[2]))
                    break
    
    node.append(mvtype)
    return node

def get_non_terminal_nodes_list_number_2(file_name):
    """
    @gk
    This function takes as input a file of nodes type and
    returns a dictionary with the coordinates of each non-terminal node
    dict = {'name': [x, y, width, height]}
    
    REVISION: 
    Returns floats and not integers
    Minor changes

    REVISED | NO KNOWN BUGS

    """

    nodes = {}
    data = []
    x = y = 0

    with open(file_name + '.pl') as p:
        for num, line in enumerate(p):
            if not(num == 0 or '#' in line or line == '\n'):
                data = line.split()
                x = float(data[1])
                y = float(data[2])
                nodes[data[0]] = [x]
                nodes[data[0]].append(y)
    data.clear()

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n' or 'NumNodes' in line or 'NumTerminals' in line:
                continue
            elif 'terminal' in line or 'terminal_NI' in line:
                data = line.split()
                del nodes[data[0]]
            else:
                data = line.split()
                nodes[data[0]].append(float(data[1]))
                nodes[data[0]].append(float(data[2]))

    return nodes

def get_non_terminal_nodes_number(file_name):
    """
    @gk
    This function takes as input a type .nodes file's name
    and return an integer of the non terminal nodes in it.

    REVISION:
    No major changes

    REVISED | NO KNOWN BUGS
    """
    data = []
    terminals = 0
    sum = 0

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if 'NumNodes' in line:
                data = line.split()
                sum = int(data[2])
            if 'NumTerminals' in line:
                data = line.split()
                terminals = int(data[2])

    return sum - terminals

def get_terminal_nodes_list_number_2(file_name):
    """
    @gk
    @gk
    This function takes as input a file of nodes type and
    returns a dictionary with the coordinates of each non-terminal node.

    REVISION:
    No major changes

    REVISED | NO KNOWN BUGS
    
    """
    data = []
    nodes = {}

    with open(file_name + '.pl') as p:
        for num, line in enumerate(p):
            if not(num == 0 or '#' in line or line == '\n'):
                data = line.split()
                nodes[data[0]] = [float(data[1])]
                nodes[data[0]].append(float(data[2]))

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            elif "terminal" in line or "terminal_NI" in line:
                data = line.split()
                nodes[data[0]].append(float(data[1]))
                nodes[data[0]].append(float(data[2]))
            else:
                data = line.split()
                del nodes[data[0]]

    return nodes
    
def get_terminal_nodes_number(file_name):
    """
    @gk
    This function takes as input a type .nodes file's name
    and return an integer of the terminal nodes in it.

    REVISION:
    No major changes

    REVISED | NO KNOWN BUGS
    """

    data = []

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if 'NumTerminals' in line:
                data = line.split()
                return int(data[2])

def locate_nodes_in_area(file_name, x1, y1, x2, y2):
    """
    @gk
    This function takes as input the name of the benchmark
    and the coordinates to form an area and returns a list of the
    names of the nodes inside the defined area.

    REVISION:
    No major changes

    REVISED | NO KNOWN BUGS
    """

    data = []
    nodes = {}
    final_nodes = []

    with open(file_name + '.pl') as p:
        for num, line in enumerate(p):
            if not(num == 0 or '#' in line or line == '\n'):
                data = line.split()
                nodes[data[0]] = [float(data[1])] #low x
                nodes[data[0]].append(float(data[2])) #low y

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if not(num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line):
                data = line.split()
                nodes[data[0]].append(float(data[1]))
                nodes[data[0]].append(float(data[2]))

    for n in nodes.items():
        if(x1 <= n[1][0] <= x2) and (y1 <= n[1][1] <= y2):
            final_nodes.append(n[0])
        else:
            continue

    return final_nodes

def locate_non_terminal(file_name, node_name):
    """
    @gk
    This function takes as input a .nodes file's name and a node's name
    and returns the coordinates of the non-terminal node, as a dictionary.
    Else it returns false.

    REVISION:
    - Invalid name case and name not found case added
    - Terminals overlooked fix

    REVISED | NO KNOWN BUGSS
    """

    data = []
    coords = {}
    non_term_flag = False
    name_flag = False

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if data[0] == node_name:
                    name_flag = False        
                    if 'terminal' in line or 'terminal_NI' in line:
                        return 'Node is terminal'
                    else:
                        non_term_flag = True
                        break
                else:
                    name_flag = True
            else:
                name_flag = True

    if name_flag:
        print('Node not found in file!')
        return None

    if non_term_flag:
        with open(file_name + '.pl') as p:
            for num, line in enumerate(p):
                if node_name in line:
                    data = line.split()
                    if data[0] == node_name:
                        coords[data[0]] = [float(data[1])]
                        coords[data[0]].append(float(data[2]))
                        break
                else:
                    continue
    else:
        return non_term_flag

    return coords

def locate_non_terminal_number_2(file_name, node_name):
    """
    @gk
    This function takes as input a .nodes file's name and a node's name
    and returns the coordinates of the node if it is not terminal as a list.
    Else it returns false.

    REVISION:
        - Invalid name case and name not found case added
        - Terminals overlooked fix

    REVISED | NO KNOWN BUGS
    """

    data = []
    coords = []
    non_term_flag = False
    name_flag = False

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if data[0] == node_name:
                    name_flag = False
                    if 'terminal' in line or 'terminal_NI' in line:
                        return 'Node is terminal'
                    else:
                        non_term_flag = True
                        break
                else:
                    name_flag = True
            else:
                name_flag = True

    if name_flag:
        print('Node not found in file!')
        return None

    if non_term_flag:
        with open(file_name + '.pl') as p:
            for num, line in enumerate(p):
                if node_name in line:
                    data = line.split()
                    if data[0] == node_name:
                        coords.append(float(data[1]))
                        coords.append(float(data[2]))
                        break
                    else:
                        continue
    else:
        return False

    return coords

def locate_non_terminal_number_3(file_name, node_name):
    """
    @gk
    This function takes as input a .nodes file's name and a node's name
    and returns the coordinates of the node if it is not terminal as a tuple.
    Else it returns false.
    REVISION:
        - Invalid name case and name not found case added
        - Terminals overlooked fix

    REVISED | NO KNOWN BUGS
    """

    data = []
    coords = []
    non_term_flag = False
    name_flag = False

    with open(file_name + '.nodes') as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if data[0] == node_name:
                    name_flag = False
                    if 'terminal' in line or 'terminal_NI' in line:
                        return 'Node is terminal'
                    else:
                        non_term_flag = True
                        break
                else:
                    name_flag = True
            else:
                name_flag = True

    if name_flag:
        print('Node not found in file!')
        return None

    if non_term_flag:
        with open(file_name + '.pl') as p:
            for num, line in enumerate(p):
                if node_name in line:
                    data = line.split()
                    if data[0] == node_name:
                        coords.append(float(data[1]))
                        coords.append(float(data[2]))
                        break
                    else:
                        continue
    else:
        return False

    return tuple(coords)
    
def locate_non_terminal_nodes_in_area(file_name, x1, y1, x2, y2):
    """
    @gk
    This function takes as input the name of the benchmark.nodes
    and the coordinates to form an area and returns a list of the
    names of the non-terminal nodes inside the defined area.

    REVISION:
    
    """