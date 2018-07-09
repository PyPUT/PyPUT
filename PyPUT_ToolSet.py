import re
import time
import scipy.sparse as sp
import math
import random
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from bisect import bisect_left


def check_move_validity(pl_file_name, node_name, new_ly, new_lx):
    """
    @gk
    This function takes as input a benchmark's pl file and a new node to be moved.
    For the node it takes its name and the new, low_y and low_x.
    Then it checks for overflow and overlaps and returns a boolean.
    False if the move is not valid, True otherwise.
    :param pl_file_name:
    :param node_name:
    :param new_ly:
    :param new_lx:
    :return:
    """

    overflow = False
    overlap = False
    data = []
    given_node = [float(new_ly), float(new_lx)]
    nodes = {}
    lines = {}
    line_key = 0

    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                if data[0] == node_name:
                    continue
                else:
                    nodes[data[0]] = [float(data[2])]
                    nodes[data[0]].append(float(data[1]))

    nodes_file_name = pl_file_name.replace('.pl', '.nodes')
    with open(nodes_file_name) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n' or \
                    'NumNodes' in line or 'NumTerminals' in line:
                continue
            else:
                data = line.split()
                if data[0] == node_name:
                    given_node.append(float(data[2]))
                    given_node.append(float(data[1]))
                else:
                    nodes[data[0]].append(float(data[2]))
                    nodes[data[0]].append(float(data[1]))

    line_counter = ly = sp = 0
    scl_file_name = pl_file_name.replace('.pl', '.scl')
    with open(scl_file_name) as s:
        for num, line in enumerate(s):
            if '#' in line or line == '\n' or 'NumRows' in line:
                continue
            else:
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


"""
=====================================================================================================================
"""


def check_non_terminal(nodes_file, node):
    """
    @gk
    Function takes as input the file's name and the node's name.
    It pinpoints the line of the node. Then searches for the string
    terminal. It returns True if there is no terminal string after
    the name of the node.
    :param nodes_file:
    :param node:
    :return:
    """

    data = []
    with open(nodes_file) as f:
        for num, line in enumerate(f):
            if node in line:
                data = line.split()
                if node == data[0]:
                    if "terminal" in line:
                        return False

    return True


"""
=====================================================================================================================
"""


def check_terminal(nodes_file, node):
    """
    @gk
    Function takes as input the file's name and the node's name.
    Pinpoints the line of the node name , returns true if the string
    terminal is in the same line.
    :param nodes_file:
    :param node:
    :return:
    """

    data = []
    with open(nodes_file) as f:
        for num, line in enumerate(f):
            if node in line:
                data = line.split()
                if node == data[0]:
                    if "terminal" in line:
                        return True

    return False


"""
=====================================================================================================================
"""


def classify_by_weight(wts_file):
    """
    @gk
    This function takes as input .wts file's name and
    returns the weight of all nodes in a dictionary
    dictionary --> {node's name: [weight]}
    :param wts_file: str
    :return nodes{}: {str: [int]}
    """

    nodes = {}
    data =[]
    flag = 0
    with open(wts_file) as wf:
        for num, line in enumerate(wf, 0):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                nodes[data[0]] = [float(data[1])]
    return nodes


"""
=====================================================================================================================
"""


def density_in_coordinates(pl_file_name, low_y, low_x, high_y, high_x):
    """
    @gk
    This function takes as input a benchmarks pl file , and 4 coordinates
    to signify and area , low_x, low_y, high_x, high_y.
    It calculates the area of the given coordinates and finds the nodes in that area.
    returns the density by dividing the total node area by the area given.
    :param pl_file_name:
    :param low_y:
    :param low_x:
    :param high_y:
    :param high_x:
    :return:
    """
    area = float((high_x - low_x)) * float((high_y - low_y))
    nodes_area = 0.0
    data = []
    nodes = {}

    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                nodes[data[0]] = [float(data[1])]
                nodes[data[0]].append(float(data[2]))

    nodes_file_name = pl_file_name.replace('.pl', '.nodes')
    with open(nodes_file_name) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            else:
                data = line.split()
                nodes[data[0]].append(float(data[1]))
                nodes[data[0]].append(float(data[2]))

    for cell in nodes.items():
        if low_x <= cell[1][0] < high_x \
                and low_y <= cell[1][1] < high_y:
            continue
        else:
            data.append(cell[0])

    for i in range(len(data)):
        nodes.pop(data[i], None)

    for n in nodes.items():
        nodes_area += n[1][2] * n[1][3]

    return nodes_area / area


"""
=====================================================================================================================
"""


def density_per_row(scl_file_name):
    """
    @gk
    This function takes as input the name of an .scl file in string form
    and it returns the density of all lines of the design in a dictionary of floats.
    Form of dictionary: density {line number: line density}
    :param scl_file_name: str
    :return density: {int: int}
    """
    number_of_lines = 0
    line_counter = 0
    data = []
    lines = {}
    nodes = {}
    lx = rx = ly = uy = height = width = 0
    with open(scl_file_name) as sf:
        for num, line in enumerate(sf, 0):
            if "NumRows" in line:
                data = line.split()
                number_of_lines = int(data[2])
            if "CoreRow" in line:
                line_counter += 1
                if line_counter == number_of_lines:
                    break
            if "Coordinate" in line:
                data = line.split()
                ly = float(data[2])
            if "Height" in line:
                data = line.split()
                height = float(data[2])
                uy = ly + height
            if "SubrowOrigin" in line:
                data = line.split()
                lx = float(data[2])
                width = float(data[5])
                rx = lx + width * 1
            lines[line_counter] = [ly]
            lines[line_counter].append(uy)
            lines[line_counter].append(lx)
            lines[line_counter].append(rx)
            lines[line_counter].append(width)

    pl_file_name = scl_file_name.replace(".scl", ".pl")
    with open(pl_file_name) as pf:
        for num, line in enumerate(pf, 0):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                lx = float(data[1])
                ly = float(data[2])
                nodes[data[0]] = [lx]
                nodes[data[0]].append(ly)

    nodes_file_name = scl_file_name.replace(".scl", ".nodes")
    with open(nodes_file_name) as nf:
        for num, line in enumerate(nf):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            else:
                data = line.split()
                nodes[data[0]].append(float(data[1]))
                nodes[data[0]].append(float(data[2]))

    density = {k: 0 for k in range(number_of_lines)}
    s = 0
    widths = []
    for l in lines.items():
        for n in nodes.items():
            if (l[1][2] <= n[1][0] < l[1][3]) and \
                    (l[1][0] <= n[1][1] < l[1][1]):
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


"""
=====================================================================================================================
"""


def find_similar_cells(nodes_file_name, node_name):
    """
    @gk
    This function takes as input a benchmarks node file
    and a node's name and returns a list of the nodes similar to the
    given one in width and height
    :param nodes_file_name:
    :param node_name:
    :return:
    """
    data = []
    nodes = {}
    result = []

    with open(nodes_file_name) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            else:
                data = line.split()
                nodes[data[0]] = [float(data[1])]
                nodes[data[0]].append(float(data[2]))

    wh = nodes.get(node_name)

    for n in nodes.items():
        if n[1][0] == wh[0] and n[1][1] == wh[1]:
            result.append(n[0])

    return result


"""
=====================================================================================================================
"""


def find_similar_set_of_cells(nodes_file_name, node_names):
    """
    @gk
    This function takes as input a benchmarks nodes file and
    a list of nodes to search. It returns the names of the similar nodes
    according to width and height in a dictionary. The dictionary has as keys
    the names of the given nodes and as values the names of the similar nodes.
    :param nodes_file_name:
    :param node_names:
    :return:
    """
    data = []
    nodes = {}
    nodes_cp = {}

    with open(nodes_file_name) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            else:
                data = line.split()
                nodes[data[0]] = [float(data[1])]
                nodes[data[0]].append(float(data[2]))

    for nc in nodes.items():
        for n in node_names:
            if n == nc[0]:
                nodes_cp[n] = [nc[1][0]]
                nodes_cp[n].append(nc[1][1])

    cells_set = nodes_cp.copy()
    cells_set = cells_set.fromkeys(cells_set, [])
    for nc in nodes_cp.items():
        for n in nodes.items():
            if nc[0] == n[0]:
                continue
            elif nc[1][0] == n[1][0] and nc[1][1] == n[1][1]:
                cells_set[nc[0]].append(n[0])

    return cells_set


"""
=====================================================================================================================
"""


def get_coordinates(pl_file_name, node_name):
    """
    @gk
    This function takes as input a pl-file's name and a node's name
    and returns an int-type list of the coordinates.
    list's form : [x-coordinate, y-coordinate]
    :param pl_file_name:
    :param node_name:
    :return:
    """
    coordinates = []
    with open(pl_file_name) as f:
        for num, line in enumerate(f):
            if node_name in line:
                data = line.split()
                if node_name == data[0]:
                    coordinates.append(float(data[1]))
                    coordinates.append(float(data[2]))
                    break
    return coordinates


"""
=====================================================================================================================
"""


def get_coordinates_row(pl_file, chip_row_number):
    """
    @gk
    This function takes as input the name of a .pl file as a string
    and the row's number of a chip and returns a dictionary with
    the coordinates of the chip's nodes.
    Form of dictionary: chip_coordinates = {'node's name': [x,y,width,height]}
    :param pl_file: str
    :param chip_row_number: int
    :return chip_coordinates : {str: list[int,int,int,int]}
    """

    data = []
    lines = {}
    nodes = {}
    lx = rx = ly = uy = height = width = 0
    counter = 0

    scl_file = pl_file.replace('.pl', '.scl')
    with open(scl_file) as s:
        for num, line in enumerate(s):
            if "CoreRow" in line:
                counter += 1
                if counter == chip_row_number + 1:
                    break
            if "Coordinate" in line:
                data = line.split()
                ly = int(data[2])
            if "Height" in line:
                data = line.split()
                height = int(data[2])
                uy = ly + height
            if "SubrowOrigin" in line:
                data = line.split()
                lx = int(data[2])
                width = int(data[5])
                rx = lx + width * 1
            lines[counter] = [ly]
            lines[counter].append(uy)
            lines[counter].append(lx)
            lines[counter].append(rx)

    for i in range(chip_row_number):
        del lines[i]

    with open(pl_file) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                lx = int(data[1])
                ly = int(data[2])
                nodes[data[0]] = [lx]
                nodes[data[0]].append(ly)

    nodes_file_name = pl_file.replace(".pl", ".nodes")
    with open(nodes_file_name) as nf:
        for num, line in enumerate(nf):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            else:
                data = line.split()
                nodes[data[0]].append(int(data[1]))
                nodes[data[0]].append(int(data[2]))

    chip_coordinates = {k: 0 for k in nodes.keys()}
    for l in lines.items():
        for n in nodes.items():
            if (l[1][2] <= n[1][0] < l[1][3]) and \
                    (l[1][0] <= n[1][1] < l[1][1]):
                chip_coordinates[n[0]] = n[1]
            else:
                del chip_coordinates[n[0]]

    return chip_coordinates


"""
====================================================================================================================
"""


def get_coordinates_net(net_file, net_name):
    """
    @gk
    This function takes as input a .nets file's name and the name of a net
    and returns a dictionary of nodes and their coordinates
    dictionary's form: {'node's name': ['x','y'], ...}
    :param net_file: str
    :param net_name: str
    :return net: dict{'str': ['str','str']}
    """
    pl_file = net_file.replace('.nets', '.pl')
    net = {}
    net_name_number = int(net_name.replace('n', ''))
    nodes_in_net_num = 0
    node_names = []
    data = []
    pos = 0
    counter = -1
    with open(net_file) as nf:
        for num, line in enumerate(nf, 0):
            if "NetDegree" in line:
                counter += 1
                if counter == net_name_number:
                    pos = num
                    data = line.split()
                    nodes_in_net_num = data[2]

    with open(net_file) as nf:
        for num, line in enumerate(nf, 0):
            if pos < num <= pos + int(nodes_in_net_num):
                data = line.split()
                node_names.append(data[0])

    data.clear()
    with open(pl_file) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net[i] = [j[1]]
                net[i].append(j[2])

    return net


"""
=====================================================================================================================
"""


def get_info_non_terminal_number_2(node_name, nodes_file_name):
    """
    @gk
    This function takes as input a benchmark's node file name
    and the name of a node and returns a list with the width and the height
    as floats --> [width, height]
    :param node_name:
    :param nodes_file_name:
    :return:
    """
    data = []
    node = []
    with open(nodes_file_name) as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if data[0] == node_name:
                    if "terminal" in line or "terminal_NI" in line:
                        print("Given Node is Terminal")
                        return False
                    else:
                        node.append(float(data[1]))
                        node.append(float(data[2]))
                        break
                else:
                    print("Given node does not exist")
                    return False
    return node


"""
=====================================================================================================================
"""


def get_info_terminal_number_2(node_name, nodes_file_name):
    """
    @gk
    This function takes as input a benchmarks nodes file
    and a nodes name and returns a list of the given node's
    width and height if the node is terminal else it returns false
    [width, height] --> [float, float]
    :param node_name:
    :param nodes_file_name:
    :return:
    """
    data = []
    node = []
    with open(nodes_file_name) as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split()
                if data[0] == node_name:
                    if "terminal" in line or "terminal_NI" in line:
                        node.append(float(data[1]))
                        node.append(float(data[2]))
                        break
                    else:
                        print("Given Node is non-Terminal")
                        return False
                else:
                    print("Given node does not exist")
                    return False
    return node


"""
=====================================================================================================================
"""


def get_net_info(net_file, net_name):
    """
    @gk
    This function takes as input a benchmarks nets file
    and a nets name , and returns a dictionary with the net's
    nodes info --> dictionary {'node_name': [low_x, low_y, width, height, movetype]}
    :param net_file:
    :param net_name:
    :return:
    """

    pl_file = net_file.replace('.nets', '.pl')
    net = {}
    net_name_number = int(net_name.replace('n', ''))
    nodes_in_net_num = 0
    node_names = []
    data = []
    pos = 0
    counter = -1

    with open(net_file) as nf:
        for num, line in enumerate(nf, 0):
            if "NetDegree" in line:
                counter += 1
                if counter == net_name_number:
                    pos = num
                    data = line.split()
                    nodes_in_net_num = data[2]

    with open(net_file) as nf:
        for num, line in enumerate(nf, 0):
            if pos < num <= pos + int(nodes_in_net_num):
                data = line.split()
                node_names.append(data[0])

    data.clear()
    with open(pl_file) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net[i] = [j[1]]
                net[i].append(j[2])

    data.clear()
    nodes_file = net_file.replace('.nets', '.nodes')
    with open(nodes_file) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n'\
                        or 'NumNodes' in line or 'NumTerminals' in line:
                continue
            else:
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


"""
=====================================================================================================================
"""


def get_node_info(node_name, nodes_file_name):
    """
    @gk
    This function takes as input the name of the node
    and a benchmarks nodes file name and returns info about the node
    info returned --> [width, height, low_x, low_y, movetype]
    :param node_name:
    :param nodes_file_name:
    :return:
    """

    data = []
    node = []
    mvtype = ''

    with open(nodes_file_name) as n:
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
                    break

    pl_file_name = nodes_file_name.replace('.nodes', '.pl')
    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if node_name in line:
                data = line.split()
                if node_name == data[0]:
                    node.append(float(data[1]))
                    node.append(float(data[2]))
                    break

    node.append(mvtype)
    return node


"""
====================================================================================================================
"""


def get_non_terminal_nodes_list_number2(nodes_file_name):
    """
    @gk
    This function takes as input a file of nodes type and
    returns a dictionary with the coordinates of each non-terminal node
    dict = {'name': [x, y, width, height]}
    :param nodes_file_name:
    :return:
    """
    widht = height = x = y = 0
    nodes = {}
    data = []

    pl_file_name = nodes_file_name.replace('.nodes', '.pl')
    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                x = int(data[1])
                y = int(data[2])
                nodes[data[0]] = [x]
                nodes[data[0]].append(y)

    with open(nodes_file_name) as nf:
        for num, line in enumerate(nf):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            elif "terminal" in line or "terminal_NI" in line:
                data = line.split()
                del nodes[data[0]]
            else:
                data = line.split()
                nodes[data[0]].append(int(data[1]))
                nodes[data[0]].append(int(data[2]))

    return nodes


"""
====================================================================================================================
"""


def get_non_terminal_nodes_number(node_file):
    """
    @gk
    This function takes as input a type .nodes file's name
    and return an integer of the non terminal nodes in it.
    :param node_file: str
    :return non_terminals: int
    """
    data = []
    terminals = 0
    sum = 0
    with open(node_file) as f:
        for num, line in enumerate(f):
            if "NumNodes" in line:
                data = line.split()
                sum = int(data[2])
            if "NumTerminals" in line:
                data = line.split()
                terminals = int(data[2])

    return sum - terminals


"""
====================================================================================================================
"""


def get_terminal_nodes_list_number2(nodes_file_name):
    """
    @gk
    This function takes as input a file of nodes type and
    returns a dictionary with the coordinates of each non-terminal node
    dict = {'name': [x, y, width, height]}
    :param nodes_file_name:
    :return:
    """
    widht = height = x = y = 0
    nodes = {}
    data = []

    pl_file_name = nodes_file_name.replace('.nodes', '.pl')
    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                x = float(data[1])
                y = float(data[2])
                nodes[data[0]] = [x]
                nodes[data[0]].append(y)

    with open(nodes_file_name) as nf:
        for num, line in enumerate(nf):
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


"""
====================================================================================================================
"""


def get_terminal_nodes_number(node_file):
    """
    @gk
    This function takes as input a type .nodes file's name
    and return an integer of the terminal nodes in it.
    :param node_file: str
    :return terminals: int
    """
    data = []
    terminals = 0
    with open(node_file) as f:
        for num, line in enumerate(f):
            if "NumTerminals" in line:
                data = line.split()
                terminals = int(data[2])

    return terminals


"""
====================================================================================================================
"""


def locate_nodes_in_area(nodes_file_name, x1, y1, x2, y2):
    """
    @gk
    This function takes as input the name of the benchmark.nodes
    and the coordinates to form an area and returns a list of the
    names of the nodes inside the defined area.
    :param nodes_file_name:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    data = []
    nodes = {}
    res_nodes = []
    lx = rx = ly = uy = height = width = 0

    pl_file_name = nodes_file_name.replace('.nodes', '.pl')
    with open(pl_file_name) as pf:
        for num, line in enumerate(pf, 0):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                lx = int(data[1])
                ly = int(data[2])
                nodes[data[0]] = [lx]
                nodes[data[0]].append(ly)

    with open(nodes_file_name) as nf:
        for num, line in enumerate(nf):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            else:
                data = line.split()
                nodes[data[0]].append(int(data[1]))
                nodes[data[0]].append(int(data[2]))

    for n in nodes.items():
        if (x1 <= n[1][0] <= x2) and \
                (y1 <= n[1][1] <= y2):
            res_nodes.append(n[0])
        else:
            continue

    return res_nodes


"""
====================================================================================================================
"""


def locate_non_terminal(nodes_file, node_name):
    """
    @gk
    This function takes as input a .nodes file's name and a node's name
    and returns the coordinates of the node if it is not terminal as a dictionary.
    Else it returns false.
    Type of the dictionary: {node's name: [x,y]}
    :param nodes_file: str
    :param node_name: str
    :return coordinates: {str: [str, str]}
    :return false: boolean
    """

    data = []
    coordinates = {}
    non_term = False
    with open(nodes_file) as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split(" ")
                if data[-1] == "terminal\n" or data[-1] == "terminal_NI\n":
                    break
                else:
                    non_term = True
                    break

    if non_term is False:
        return False
    else:
        pl_file_name = nodes_file.replace(".nodes", ".pl")
        with open(pl_file_name) as p:
            for num, line in enumerate(p):
                if node_name in line:
                    data = line.split()
                    if data[0] == node_name:
                        coordinates[data[0]] = [float(data[1])]
                        coordinates[data[0]].append(float(data[2]))
                        break
                    else:
                        continue

        return coordinates


"""
====================================================================================================================
"""


def locate_non_terminal_number_2(nodes_file, node_name):
    """
    @gk
    This function takes as input a .nodes file's name and a node's name
    and returns the coordinates of the node if it is not terminal as a list.
    Else it returns false.
    Type of the list: [x,y]
    :param nodes_file: str
    :param node_name: str
    :return coordinates: [float, float]
    :return false: boolean
    """

    data = []
    coordinates = []
    non_term = False
    with open(nodes_file) as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split(" ")
                if data[-1] == "terminal\n" or data[-1] == "terminal_NI\n":
                    break
                else:
                    non_term = True
                    break

    if non_term is False:
        return False
    else:
        pl_file_name = nodes_file.replace(".nodes", ".pl")
        with open(pl_file_name) as p:
            for num, line in enumerate(p):
                if node_name in line:
                    data = line.split()
                    if data[0] == node_name:
                        coordinates.append(float(data[1]))
                        coordinates.append(float(data[2]))
                        break
                    else:
                        continue

    return coordinates


"""
====================================================================================================================
"""


def locate_non_terminal_number_3(nodes_file, node_name):
    """
    @gk
    This function takes as input a .nodes file's name and a node's name
    and returns the coordinates of the node if it is not terminal as a tuple.
    Else it returns false.
    Type of the tuple: (x, y)
    :param nodes_file: str
    :param node_name: str
    :return coordinates: (float, float)
    :return false: boolean
    """

    data = []
    coordinates = []
    non_term = False
    with open(nodes_file) as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split(" ")
                if data[-1] == "terminal\n" or data[-1] == "terminal_NI\n":
                    break
                else:
                    non_term = True
                    break

    if non_term is False:
        return False
    else:
        pl_file_name = nodes_file.replace(".nodes", ".pl")
        with open(pl_file_name) as p:
            for num, line in enumerate(p):
                if node_name in line:
                    data = line.split()
                    if data[0] == node_name:
                        coordinates.append(float(data[1]))
                        coordinates.append(float(data[2]))
                        break
                    else:
                        continue

    return tuple(coordinates)


"""
=====================================================================================================================
"""


def locate_non_terminal_nodes_in_area(nodes_file_name, x1, y1, x2, y2):
    """
    @gk
    This function takes as input the name of the benchmark.nodes
    and the coordinates to form an area and returns a list of the
    names of the non-terminal nodes inside the defined area.
    :param nodes_file_name:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    data = []
    nodes = {}
    res_nodes = []
    lx = rx = ly = uy = height = width = 0

    pl_file_name = nodes_file_name.replace('.nodes', '.pl')
    with open(pl_file_name) as pf:
        for num, line in enumerate(pf, 0):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                lx = int(data[1])
                ly = int(data[2])
                nodes[data[0]] = [lx]
                nodes[data[0]].append(ly)

    with open(nodes_file_name) as nf:
        for num, line in enumerate(nf):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            elif "terminal" in line or "terminal_NI" in line:
                data = line.split()
                del nodes[data[0]]
            else:
                data = line.split()
                nodes[data[0]].append(int(data[1]))
                nodes[data[0]].append(int(data[2]))

    for n in nodes.items():
        if (x1 <= n[1][0] <= x2) and \
                (y1 <= n[1][1] <= y2):
            res_nodes.append(n[0])
        else:
            continue

    return res_nodes


"""
====================================================================================================================
"""


def locate_terminal(nodes_file, node_name):
    """
    @gk
    This function takes as input a .nodes file's name and a node's name
    and returns the coordinates of the node if it is terminal as a dictionary.
    Else it returns false.
    Type of the dictionary: {node's name: [x,y]}
    :param nodes_file: str
    :param node_name: str
    :return coordinates: {str: [str, str]}
    :return false: boolean.
    """

    data = []
    coordinates = {}
    term = False
    with open(nodes_file) as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split(" ")
                if data[-1] != "terminal\n" and data[-1] != "terminal_NI\n":
                    break
                else:
                    term = True
                    break

    if term is False:
        return False
    else:
        pl_file_name = nodes_file.replace(".nodes", ".pl")
        with open(pl_file_name) as p:
            for num, line in enumerate(p):
                if node_name in line:
                    data = line.split()
                    if data[0] == node_name:
                        coordinates[data[0]] = [float(data[1])]
                        coordinates[data[0]].append(float(data[2]))
                        break
                    else:
                        continue

        return coordinates


"""
===================================================================================================================
"""


def locate_terminal_number_2(nodes_file, node_name):
    """
    @gk
    This function takes as input a .nodes file's name and a node's name
    and returns the coordinates of the node if it is terminal as a list.
    Else it returns false.
    Type of the list: [x, y]
    :param nodes_file: str
    :param node_name: str
    :return coordinates: [float, float]
    :return false: boolean.
    """

    data = []
    coordinates = []
    term = False
    with open(nodes_file) as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split(" ")
                if data[-1] != "terminal\n" and data[-1] != "terminal_NI\n":
                    break
                else:
                    term = True
                    break

    if term is False:
        return False
    else:
        pl_file_name = nodes_file.replace(".nodes", ".pl")
        with open(pl_file_name) as p:
            for num, line in enumerate(p):
                if node_name in line:
                    data = line.split()
                    if data[0] == node_name:
                        coordinates.append(float(data[1]))
                        coordinates.append(float(data[2]))
                        break
                    else:
                        continue

    return coordinates


"""
====================================================================================================================
"""


def locate_terminal_number_3(nodes_file, node_name):
    """
    @gk
    This function takes as input a .nodes file's name and a node's name
    and returns the coordinates of the node if it is terminal as a tuple.
    Else it returns false.
    Type of the tuple: (x, y)
    :param nodes_file: str
    :param node_name: str
    :return coordinates: (float, float)
    :return false: boolean.
    """

    data = []
    coordinates = []
    term = False
    with open(nodes_file) as n:
        for num, line in enumerate(n):
            if node_name in line:
                data = line.split(" ")
                if data[-1] != "terminal\n" and data[-1] != "terminal_NI\n":
                    break
                else:
                    term = True
                    break

    if term is False:
        return False
    else:
        pl_file_name = nodes_file.replace(".nodes", ".pl")
        with open(pl_file_name) as p:
            for num, line in enumerate(p):
                if node_name in line:
                    data = line.split()
                    if data[0] == node_name:
                        coordinates.append(float(data[1]))
                        coordinates.append(float(data[2]))
                        break
                    else:
                        continue

    return tuple(coordinates)


"""
====================================================================================================================
"""


def locate_terminal_nodes_in_area(nodes_file_name, x1, y1, x2, y2):
    """
    @gk
    This function takes as input the name of the benchmark.nodes
    and the coordinates to form an area and returns a list of the
    names of the terminal nodes inside the defined area.
    :param nodes_file_name:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    data = []
    nodes = {}
    res_nodes = []
    lx = rx = ly = uy = height = width = 0

    pl_file_name = nodes_file_name.replace('.nodes', '.pl')
    with open(pl_file_name) as pf:
        for num, line in enumerate(pf, 0):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                lx = int(data[1])
                ly = int(data[2])
                nodes[data[0]] = [lx]
                nodes[data[0]].append(ly)

    with open(nodes_file_name) as nf:
        for num, line in enumerate(nf):
            if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
                continue
            elif "terminal" in line or "terminal_NI" in line:
                data = line.split()
                nodes[data[0]].append(int(data[1]))
                nodes[data[0]].append(int(data[2]))
            else:
                data = line.split()
                del nodes[data[0]]

    for n in nodes.items():
        if (x1 <= n[1][0] <= x2) and \
                (y1 <= n[1][1] <= y2):
            res_nodes.append(n[0])
        else:
            continue

    return res_nodes


"""
====================================================================================================================
"""


def node_weight(wts_file, node_name):
    """
    @gk
    This function takes as input the benchmarks wts file and a node's name, and
    return its weight as a string.
    It works only for ibm benchmarks, as of 2006 wts files are not used.
    :param wts_file:
    :param node_name:
    :return weight: str
    """
    data = ''
    with open(wts_file) as f:
        for num, line in enumerate(f):
            if node_name in line:
                data = line.split()
                if data[0] == node_name:
                    return data[1]
                else:
                    return False


"""
====================================================================================================================
"""


def number_of_rows(scl_file):
    """
    @gk
    This function takes as input the name of the scl file
    and return the number of rows as integer
    :param scl_file:
    :return rows' number: int
    """
    data = " "
    with open(scl_file) as f:
        for num, line in enumerate(f):
            if "NumRows" in line:
                data = line.split()
                return int(data[2])


"""
====================================================================================================================
"""


def place_node(pl_file_name, node_name, new_low_x, new_low_y):
    """
    @gk
    This function takes as input a benchmark's pl file
    and a nodes name and new low x and y.
    After that it replaces the node's old coordinates with new ones.
    NOTE that it would be better to use a copy of the original benchmark
    in order to avoid messing the original file !
    :param pl_file_name:
    :param node_name:
    :param new_low_x:
    :param new_low_y:
    :return:
    """
    data = []
    my_line = ''
    new_line = ''
    my_x = ''
    my_y = ''
    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if node_name in line:
                data = line.split()
                if data[0] == node_name:
                    my_line = line
                    new_line = line
                    my_x = data[1]
                    my_y = data[2]
                    break

    flag = False
    data = new_line.split(' ')
    for i in range(len(data)):
        if my_x == my_y:
            flag = True
        if data[i] == my_x:
            data[i] = str(new_low_x)
            if flag is True:
                my_x = None
        elif data[i] == my_y:
            data[i] = str(new_low_y)
    new_line = ' '.join(data)

    with open(pl_file_name) as p:
        data = p.readlines()

    for i in range(len(data)):
        if data[i] == my_line:
            data[i] = data[i].replace(data[i], new_line)

    with open(pl_file_name, 'w') as p:
        p.writelines(data)


"""
====================================================================================================================
"""


def swap_cells(pl_file_name, cell1, cell2):
    """
    @gk
    This function takes as input a benchmarks pl file,
    and the name of two nodes that are to be swapped.
    Then as a result it pseudo-overwrites the file, by creating
    a new one, replacing the old one.
    NOTE that it would be better to use a copy of the original benchmark
    in order to avoid messing the original file !
    :param pl_file_name:
    :param cell1:
    :param cell2:
    :return:
    """
    line_cell_1 = ''
    line_cell_2 = ''
    data = []
    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if cell1 in line:
                data = line.split()
                if data[0] == cell1:
                    line_cell_1 = line
            if cell2 in line:
                data = line.split()
                if data[0] == cell2:
                    line_cell_2 = line

    with open(pl_file_name) as p:
        data = p.readlines()

    for i in range(len(data)):
        if data[i] == line_cell_1:
            data[i] = line_cell_2.replace(cell2, cell1)
        if data[i] == line_cell_2:
            data[i] = line_cell_1.replace(cell1, cell2)

    with open(pl_file_name, 'w') as p:
        p.writelines(data)


"""
====================================================================================================================
"""



def total_density(scl_file_name):
	"""
    @gk
    This function takes as input a benchmark's scl file and
    returns the total density of the chip as a float
    :param scl_file_name:
    :return:
    """
	
	number_of_lines = 0
	line_counter = 0
	data = []
	lines = {}
	nodes = {}
	lx = rx = ly = uy = height = width = 0
	with open(scl_file_name) as sf:
	    for num, line in enumerate(sf, 0):
	        if "NumRows" in line:
	            data = line.split()
	            number_of_lines = int(data[2])
	        if "CoreRow" in line:
	            line_counter += 1
	            if line_counter == number_of_lines:
	                break
	        if "Coordinate" in line:
	            data = line.split()
	            ly = int(data[2])
	        if "Height" in line:
	            data = line.split()
	            height = int(data[2])
	            uy = ly + height
	        if "SubrowOrigin" in line:
	            data = line.split()
	            lx = int(data[2])
	            width = int(data[5])
	            rx = lx + width * 1
	        lines[line_counter] = [ly]
	        lines[line_counter].append(uy)
	        lines[line_counter].append(lx)
	        lines[line_counter].append(rx)

	nodes_file_name = scl_file_name.replace(".scl", ".nodes")
	with open(nodes_file_name) as nf:
	    for num, line in enumerate(nf):
	        if num == 0 or '#' in line or line == '\n' or "NumNodes" in line or "NumTerminals" in line:
	            continue
	        else:
	            data = line.split()
	            nodes[data[0]] = [int(data[1])]
	            nodes[data[0]].append(int(data[2]))

	chip_size = 0
	for l in lines.items():
		chip_size += (l[1][1] - l[1][0]) * (l[1][3] - l[1][2])

	cells_size = 0
	for n in nodes.items():
		cells_size += n[1][0] * n[1][1]

	return float(cells_size / chip_size)



"""
====================================================================================================================
"""


def rotate_cells(file_name, node_list):
    """
    @gt
    this function takes in as a parameter a benchmark and a list of nodes
    rotates their coordinates right to left.
    First node's coordinates go to last node's coordinates
    :param file_name: str
    :param node_list: list[str, str, str....,str]
    :return
    """

    to_change = {}

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in node_list:
                        to_change[node_list.index(line.split()[0])] = line

    with open(file_name + ".pl") as f:
        data = f.readlines()

    for i in range(len(to_change.values()) - 1, -1, -1):
        to_change[i] = to_change[i].replace(node_list[i], node_list[i - 1])

    for i in range(len(data)):

        for node in to_change.values():
            if re.search(r'\b' + node.split()[0] + r'\b', data[i]):
                data[i] = node + "\n"

    with open(file_name + ".pl", 'w') as p:
        p.writelines(data)


"""
====================================================================================================================
"""


def random_placement(file_name, node_list):
    """
    @gt
    this function takes in as a parameter a benchmark and a list of nodes
    places these nodes in a random position inside the chip
    does same function to every node if "all" is given instead of a list
    :param file_name: str
    :param node_list: list[str, str,......, str]/"all"
    :return
    """

    to_change = {}
    place = {}
    rows = {}
    counter = 0

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "Coordinate":
                    starting_height = int(line.split()[2])
                    if starting_height not in rows.keys():
                        rows[starting_height] = []
                if line.split()[0] == "Height":
                    height = int(line.split()[2])
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = int(line.split()[2])
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    rows[starting_height].append(starting_x)
                    rows[starting_height].append(ending_x)

    key_list = []
    for key in rows:
        key_list.append(key)
    key_list.sort()

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if node_list == "all":
                        to_change[counter] = line
                        counter += 1
                        place[line.split()[0]] = [line.split()[1], line.split()[2]]
                    elif line.split()[0] in node_list:
                        to_change[node_list.index(line.split()[0])] = line
                        place[line.split()[0]] = [line.split()[1], line.split()[2]]

    with open(file_name + ".pl") as f:
        data = f.readlines()

    for i in range(len(to_change.values())):
        random_y = str(random.randrange(key_list[0], key_list[-1], height))
        random_x = str(random.randrange(rows[int(random_y)][0], rows[int(random_y)][-1]))

        random_y = int(random_y)
        random_y += random.randrange(int(random_y), int(random_y + height))

        random_y = str(random_y)

        substring = to_change[i].split()[1]
        substring = substring.replace(to_change[i].split()[1], random_x, 1)
        to_change[i] = to_change[i].replace(to_change[i].split()[1], substring, 1)

        substring = to_change[i].split()[2]
        substring = substring.replace(to_change[i].split()[2], random_y, 1)
        to_change[i] = to_change[i].replace(to_change[i].split()[2], substring, 1)

    for i in range(len(data)):

        for node in to_change.values():
            if re.search(r'\b' + node.split()[0] + r'\b', data[i]):
                data[i] = node + "\n"

    with open(file_name + ".pl", 'w') as p:
        p.writelines(data)


"""
====================================================================================================================
"""


def comp_density(file_name1, row_num1, file_name2, row_num2):
    """
    @gt
    this function takes as a parameter two (2) benchmarks and two (2) rows
    compares the density between the first row in the first file
    and the second row in the second file
    index1: 1 if row1 > row2, 2 if row1 < row2, 0 if equal
    index2: the better of the two (2) densities
    index3: the difference between the two (2) densities
    :param file_name1: str
    :param row_num1: int
    :param file_name2: str
    :param row_num2: int
    :return list: [int, int, int]
    """
    density1 = density_per_row(file_name1)
    density2 = density_per_row(file_name2)

    row1 = density1[row_num1]
    row2 = density2[row_num2]

    if row1 > row2:
        return [1, row1, row1 - row2]
    elif row2 > row1:
        return [2, row2, row2 - row1]
    else:
        return [0, row1, 0]


"""
=====================================================================================================================
"""


def comp_row_density(file_name1, file_name2, row_num):
    """
    @gt
    this function takes as a parameter a benchmark and two (2) rows
    compares the density between the row in the first file
    and the same row in the second file and returns a list
    index1: 1 if row1 > row2, 2 if row1 < row2, 0 if equal
    index2: the better of the two (2) densities
    index3: the difference between the two (2) densities
    :param file_name1: str
    :param file_name2: str
    :param row_num: int
    :return list: [int, int, int]
    """
    density1 = density_per_row(file_name1)
    density2 = density_per_row(file_name2)

    row1 = density1[row_num]
    row2 = density2[row_num]

    if row1 > row2:
        return [1, row1, row1 - row2]
    elif row2 > row1:
        return [2, row2, row2 - row1]
    else:
        return [0, row1, 0]


"""
====================================================================================================================
"""


def empty_rows(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    and returns a dictionary of empty rows(key:coordinate, values:starting and finishing x and y)
    :param file_name: str
    :return dict{int: [int, int, int, int]}
    """

    rows = {}
    nodes = {}

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "Coordinate":
                    starting_height = int(line.split()[2])
                    if starting_height not in rows.keys():
                        rows[starting_height] = []
                if line.split()[0] == "Height":
                    ending_height = int(starting_height) + int(line.split()[2])
                    line_height = line.split()[2]
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = line.split()[2]
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    rows[starting_height].append(starting_x)
                    rows[starting_height].append(starting_height)
                    rows[starting_height].append(ending_x)
                    rows[starting_height].append(ending_height)

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] not in nodes.keys():
                        nodes[line.split()[0]] = []
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(int(line.split()[2]))

    keys_list = []

    for key in rows.keys():
        keys_list.append(int(key))

    min_height = keys_list[0]
    max_height = int(rows[keys_list[-1]][3])

    for node in nodes:
        if int(nodes[node][3]) not in keys_list:
            if int(nodes[node][3]) >= min_height and int(nodes[node][3]) <= max_height:
                pos = bisect_left(keys_list, int(nodes[node][3]))
                pos -= 1
            else:
                continue
        else:
            pos = keys_list.index(int(nodes[node][3]))
        if (keys_list[pos]) in rows:
            if len(rows[keys_list[pos]]) == 4:
                if int(nodes[node][2]) + int(nodes[node][0]) <= int(rows[keys_list[pos]][2]) and int(
                        nodes[node][2]) >= int(rows[keys_list[pos]][0]):
                    del rows[keys_list[pos]]
            else:
                i = 4
                while i <= len(rows[keys_list[pos]]):
                    if int(nodes[node][2]) + int(nodes[node][0]) <= int(rows[keys_list[pos]][i - 2]) and int(
                            nodes[node][2]) > int(rows[keys_list[pos]][i - 4]):
                        for j in range(4):
                            del rows[keys_list[pos]][i - 4]
                    i += 4

    for node in nodes:
        if int(nodes[node][3]) + int(nodes[node][1]) not in keys_list:
            if int(nodes[node][3]) + int(nodes[node][1]) >= min_height and int(nodes[node][3]) + int(
                    nodes[node][1]) <= max_height:
                pos = bisect_left(keys_list, int(nodes[node][3]) + int(nodes[node][1]))
                pos -= 1
            else:
                continue
        else:
            pos = keys_list.index(int(nodes[node][3]) + int(nodes[node][1]))
        if (keys_list[pos]) in rows:
            if len(rows[keys_list[pos]]) == 4:
                if int(nodes[node][2]) + int(nodes[node][0]) <= int(rows[keys_list[pos]][2]) and int(
                        nodes[node][2]) >= int(rows[keys_list[pos]][0]):
                    del rows[keys_list[pos]]
            else:
                i = 4
                while i <= len(rows[keys_list[pos]]):
                    if int(nodes[node][2]) + int(nodes[node][0]) <= int(rows[keys_list[pos]][i - 2]) and int(
                            nodes[node][2]) > int(rows[keys_list[pos]][i - 4]):
                        for j in range(4):
                            del rows[keys_list[pos]][i - 4]
                    i += 4

    return rows


"""
=====================================================================================================================
"""


def return_row_for_net(file_name, net_name):
    """
    @gt
    this function takes in as a parameter a benchmark and a net
    and returns a list with the coordinates of the rows its nodes are in
    :param file_name: str
    :param net_name: str
    :return to_return: list[int, int,..., int]
    """

    rows = {}
    nodes = {}
    nets = []
    counter = 0
    found = False

    with open(file_name + ".nets") as f:
        num_of_nodes = -1
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    if found:
                        break
                    current_net = "n" + str(counter)
                    counter += 1
                    if current_net == net_name:
                        num_of_nodes = int(line.split()[2])
                        found = True
                    else:
                        found = False
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if found:
                        num_of_nodes -= 1
                        nets.append(line.split()[0])

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "Coordinate":
                    starting_height = int(line.split()[2])
                    if starting_height not in rows.keys():
                        rows[starting_height] = []
                if line.split()[0] == "Height":
                    ending_height = int(starting_height) + int(line.split()[2])
                    line_height = line.split()[2]
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = int(line.split()[2])
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    rows[starting_height].append(starting_x)
                    rows[starting_height].append(starting_height)
                    rows[starting_height].append(ending_x)
                    rows[starting_height].append(ending_height)

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in nets:
                        nodes[line.split()[0]] = []
                        nodes[line.split()[0]].append(line.split()[1])
                        nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in nets:
                        nodes[line.split()[0]].append(line.split()[1])
                        nodes[line.split()[0]].append(int(line.split()[2]))

    keys_list = []

    for key in rows.keys():
        keys_list.append(int(key))

    to_return = []

    for node in nodes:

        if nodes[node][3] + int(nodes[node][1]) < keys_list[0] or nodes[node][3] > int(rows[keys_list[-1]][3]):
            continue

        if int(nodes[node][3]) not in keys_list:
            pos = bisect_left(keys_list, int(nodes[node][3]))
            pos -= 1
        else:
            pos = keys_list.index(int(nodes[node][3]))
        if (keys_list[pos]) in rows:
            if len(rows[keys_list[pos]]) == 4:
                if int(nodes[node][2]) + int(nodes[node][0]) <= int(rows[keys_list[pos]][2]) and int(
                        nodes[node][2]) >= int(rows[keys_list[pos]][0]):
                    to_return.append(rows[keys_list[pos]][1])
            else:
                i = 4
                while i <= len(rows[keys_list[pos]]):
                    if int(nodes[node][2]) + int(nodes[node][0]) <= int(rows[keys_list[pos]][i - 2]) and int(
                            nodes[node][2]) >= int(rows[keys_list[pos]][i - 4]):
                        to_return.append(rows[keys_list[pos]][1])
                    i += 4

        if bisect_left(keys_list, int(nodes[node][3]) + int(nodes[node][1])) - 1 != pos:
            if int(nodes[node][3]) not in keys_list:
                pos = bisect_left(keys_list, int(nodes[node][3]) + int(nodes[node][1]))
                pos -= 1
            else:
                pos = keys_list.index(int(nodes[node][3]) + int(nodes[node][1]))
            if (keys_list[pos]) in rows:
                if len(rows[keys_list[pos]]) == 4:
                    if int(nodes[node][2]) + int(nodes[node][0]) <= int(rows[keys_list[pos]][2]) and int(
                            nodes[node][2]) >= int(rows[keys_list[pos]][0]):
                        to_return.append(rows[keys_list[pos]][1])
                    else:
                        i = 4
                        while i <= len(rows[keys_list[pos]]):
                            if int(nodes[node][2]) + int(nodes[node][0]) <= int(rows[keys_list[pos]][i - 2]) and int(
                                    nodes[node][2]) >= int(rows[keys_list[pos]][i - 4]):
                                to_return.append(rows[keys_list[pos]][1])
                            i += 4

    return to_return


"""
=====================================================================================================================
"""


def check_net(file_name, search_net):
    """
    @gt
    this function takes in as a parameter a benchmark and a net
    returns a tuple
    1st index has its terminal nodes
    2nd its non terminal
    :param file_name: str
    :param search_net: str
    :return net_info: tupple(list[str, str,..., str], list[str, str,..., str])
    """

    nets = {}
    nodes = {}
    counter = 0
    terminals = []
    non_terminals = []

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    if net_name == search_net:
                        nets[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if net_name in nets:
                        nets[net_name].append(line.split()[0])

    for value in nets.values():
        for element in value:
            if element not in nodes.keys():
                nodes[element] = []

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in nodes.keys():
                        if len(line.split()) == 3:
                            non_terminals.append(line.split()[0])
                        else:
                            terminals.append(line.split()[0])

    net_info = (terminals, non_terminals)
    return net_info


"""
====================================================================================================================
"""


def check_consistency(file_name):
    """
    @gt
    this function takes in as parameter an aux file
    informs if consistency succeded
    if not, prints missing files
    :param file_name: str
    :return
    """

    files = [".nodes", ".nets", ".wts", ".pl", ".scl", ".shapes", ".route"]

    is_included = [False, False, False, False, False, False, False]
    aux_file = file_name + ".aux"

    with open(file_name + ".aux") as f:

        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if line.split()[0] == "RowBasedPlacement":
                    if ".nodes" in line:
                        is_included[0] = True
                    if ".nets" in line:
                        is_included[1] = True
                    if ".wts" in line:
                        is_included[2] = True
                    if ".pl" in line:
                        is_included[3] = True
                    if ".scl" in line:
                        is_included[4] = True
                    if ".shapes" in line:
                        is_included[5] = True
                    if ".route" in line:
                        is_included[6] = True

    missing = []
    if False not in is_included:
        print(aux_file + " consistency check completed successfully")
    else:
        for i in range(len(is_included)):
            if is_included[i] is False:
                missing.append(i)

    print(aux_file + " consistency check failed, missing files: ")
    for index in missing:
        print(files[index])


"""
====================================================================================================================
"""


def get_non_terminal_nodes_list(file_name):
    """
    @gt
    this function takes in as a parameter a .nodes file,
    after checking if the line contains node information
    it checks if the node of that line is characterized as a terminal one
    and if it is not, it appends it in a list
    :param file_name: str
    :return non_terminal_list: list[str, str,..., str]
    """
    non_terminal_list = []
    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    node_info = line.split()
                    if len(node_info) == 3:
                        non_terminal_list.append(node_info[0])

    return non_terminal_list


"""
====================================================================================================================
"""


def get_terminal_nodes_list(file_name):
    """
    @gt #4
    this function takes in as a parameter a .nodes file,
    after checking if the line contains node information
    it checks if the node of that line is characterized as a terminal one
    and if it is, it appends it in a list
    :param file_name: str
    :return terminal_list: list[str, str,..., str]
    """
    terminal_list = []

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    node_info = line.split()
                    if len(node_info) == 4:
                        terminal_list.append(node_info[0])

    return terminal_list


"""
====================================================================================================================
"""


def get_info_non_terminal(node_name, file_name):
    """
    @gt
    this function takes in as a parameter the name of the non-terminal node the user
    wants to search as well as the benchmark in which he wants to search it in
    it returns a tuple containing the width and height of the node respectively
    :param node_name: str
    :param file_name: str
    :return node_info: tupple(str, str)
    """

    node_info = ()
    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if node_name == line.split()[0] and "terminal" not in line:
                        node_info = (line.split()[1], line.split()[2])
                        break

    return node_info


"""
====================================================================================================================
"""


def get_info_terminal(node_name, file_name):
    """
    @gt
    this function takes in as a parameter the name of the terminal node the user
    wants to search as well as the benchmark in which he wants to search it in
    it returns a tuple containing the width and height of the node respectively
    :param node_name: str
    :param file_name: str
    :return node_info: tupple(str, str)
    """

    node_info = ()
    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if node_name == line.split()[0] and "terminal" in line:
                        node_info = (line.split()[1], line.split()[2])
                        break

    return node_info


"""
====================================================================================================================
"""


def return_all_nets(file_name, info):
    """
    @gt
    this function takes in as a parameter the name of the benchmark the user
    wants to search in and the amount of information he wants to receive
    low: returns a list of the names of all nets
    med: returns a dictionary where key is the name of the net and value is the degree of that net
    high: returns a dictionary where key is the name of the net and values are the degree of the net and the
    nodes of it
    vhigh: returns a dictionary where key is the name of the net and values are the degree of the net, the nodes of it
    and the orientation of each node
    other: same as low option
    :param file_name: str
    :param info: str
    :return nets: list[str, str,..., str]/dict{str: int}/dickt{str: int, str, str,..., str}
    """

    if info == "med" or info == "high" or info == "vhigh":
        nets = {}
    else:
        nets = []
    counter = 0

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    if isinstance(nets, list):
                        nets.append(net_name)
                    else:
                        if info == "med":
                            nets[net_name] = num_of_nodes
                        else:
                            nets[net_name] = []
                            nets[net_name].append(num_of_nodes)
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if not isinstance(nets, list):
                        if info != "med":
                            nets[net_name].append(line.split()[0])
                        if info == "vhigh":
                            nets[net_name].append(line.split()[1])

    return nets


"""
===================================================================================================================
"""


def corner_node(file_name, search_node):
    """
    @gt
    this function takes in as a parameter the name of the benchmark the user
    wants to search as well as the node which he wants to check if
    if in a net corner
    it returns true if it is, false otherwise
    :param file_name: str
    :param search_node: str
    :return bool
    """

    nodes = {}
    netsx = {}
    netsy = {}
    counter = 0
    in_area = []

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] not in nodes:
                        nodes[line.split()[0]] = []
                        nodes[line.split()[0]].append(line.split()[1])
                        nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    netsx[net_name] = []
                    netsy[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if net_name in netsx:
                        if len(netsx[net_name]) == 0:
                            netsx[net_name].append(int(nodes[line.split()[0]][2]))
                            netsx[net_name].append(line.split()[0])
                            netsx[net_name].append(int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]))
                            netsx[net_name].append(line.split()[0])

                            netsy[net_name].append(int(nodes[line.split()[0]][3]))
                            netsy[net_name].append(line.split()[0])
                            netsy[net_name].append(int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]))
                            netsy[net_name].append(line.split()[0])
                        else:
                            if int(nodes[line.split()[0]][2]) < netsx[net_name][0]:
                                netsx[net_name][0] = int(nodes[line.split()[0]][2])
                                netsx[net_name][1] = line.split()[0]

                            if int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]) > netsx[net_name][2]:
                                netsx[net_name][2] = int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0])
                                netsx[net_name][3] = line.split()[0]

                            if int(nodes[line.split()[0]][3]) < netsy[net_name][0]:
                                netsy[net_name][0] = int(nodes[line.split()[0]][3])
                                netsy[net_name][1] = line.split()[0]

                            if int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]) > netsy[net_name][2]:
                                netsy[net_name][2] = int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1])
                                netsx[net_name][3] = line.split()[0]

    for net in netsx:
        if netsx[net][1] == search_node or netsx[net][3] == search_node or netsy[net][1] == search_node or netsy[net][
                 3] == search_node:
            return True
    return False


"""
======================================================================================================================
"""


def corner_node_in_nets(file_name, search_node):
    """
    @gt
    this function takes in as a parameter a benchmark and a node
    returns a list of the nets in which the node is a corner
    :param file_name: str
    :param search_node: str
    :return corner_in_nets: list[str, str,..., str]
    """

    nodes = {}
    netsx = {}
    netsy = {}
    counter = 0
    corner_in_nets = []

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] not in nodes:
                        nodes[line.split()[0]] = []
                        nodes[line.split()[0]].append(line.split()[1])
                        nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    netsx[net_name] = []
                    netsy[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if net_name in netsx:
                        if len(netsx[net_name]) == 0:
                            netsx[net_name].append(int(nodes[line.split()[0]][2]))
                            netsx[net_name].append(line.split()[0])
                            netsx[net_name].append(int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]))
                            netsx[net_name].append(line.split()[0])

                            netsy[net_name].append(int(nodes[line.split()[0]][3]))
                            netsy[net_name].append(line.split()[0])
                            netsy[net_name].append(int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]))
                            netsy[net_name].append(line.split()[0])
                        else:
                            if int(nodes[line.split()[0]][2]) < netsx[net_name][0]:
                                netsx[net_name][0] = int(nodes[line.split()[0]][2])
                                netsx[net_name][1] = line.split()[0]

                            if int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]) > netsx[net_name][2]:
                                netsx[net_name][2] = int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0])
                                netsx[net_name][3] = line.split()[0]

                            if int(nodes[line.split()[0]][3]) < netsy[net_name][0]:
                                netsy[net_name][0] = int(nodes[line.split()[0]][3])
                                netsy[net_name][1] = line.split()[0]

                            if int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]) > netsy[net_name][2]:
                                netsy[net_name][2] = int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1])
                                netsx[net_name][3] = line.split()[0]

    for net in netsx:
        if netsx[net][1] == search_node or netsx[net][3] == search_node or netsy[net][1] == search_node or netsy[net][
                3] == search_node:
            corner_in_nets.append(net)

    return corner_in_nets


"""
======================================================================================================================
"""


def return_nets_for_node(file_name, search_node):
    """
    @gt
    this function takes in as a parameter the name of the benchmark the user
    wants to search and a node
    returns all nets the node is part of
    :param file_name: str
    :param search_node: str
    :return nets_in: list[str, str,..., str]
    """

    nets = {}
    counter = 0
    nets_in = []

    with open(file_name + ".nets") as f:
        num_of_nodes = -1
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    nets[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    num_of_nodes -= 1
                    nets[net_name].append(line.split()[0])
            if num_of_nodes == 0:
                if search_node not in nets[net_name]:
                    del nets[net_name]
                else:
                    nets_in.append(net_name)

    return nets_in


"""
=====================================================================================================================
"""


def hpwl_for_net(file_name, search_net):
    """
    @gt
    this function takes in as a parameter a benchmark and a net
    returns hpwl for that net
    :param file_name: str
    :param search_net: str
    :return hpwl: int
    """

    nodes = {}
    netsx = {}
    netsy = {}
    counter = 0
    hpwl = 0

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] not in nodes:
                        nodes[line.split()[0]] = []
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    if search_net == net_name:
                        netsx[net_name] = []
                        netsy[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if net_name in netsx:
                        if len(netsx[net_name]) == 0:
                            netsx[net_name].append(int(nodes[line.split()[0]][2]))
                            netsx[net_name].append(int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]))

                            netsy[net_name].append(int(nodes[line.split()[0]][3]))
                            netsy[net_name].append(int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]))
                        else:
                            if int(nodes[line.split()[0]][2]) < netsx[net_name][0]:
                                netsx[net_name][0] = int(nodes[line.split()[0]][2])

                            if int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]) > netsx[net_name][1]:
                                netsx[net_name][1] = int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0])

                            if int(nodes[line.split()[0]][3]) < netsy[net_name][0]:
                                netsy[net_name][0] = int(nodes[line.split()[0]][3])

                            if int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]) > netsy[net_name][1]:
                                netsy[net_name][1] = int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1])

    for net in netsx:
        hpwl += float(netsx[net][1] - netsx[net][0] + netsy[net][1] - netsy[net][0])

    return (hpwl)


"""
=====================================================================================================================
"""


def classify_nets_by_degree(file_name):
    """
    @gt
    this function takes in as a parameter the name of the benchmark the user
    wants to search
    returns a dictionary where keys are the net degrees and values the net names
    :param file_name: str
    :return nets: dict{int: [str, str,..., str]}
    """

    nets = {}
    counter = 0

    with open(file_name + ".nets") as f:
        num_of_nodes = -1
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    if num_of_nodes not in nets.keys():
                        nets[num_of_nodes] = []
                    nets[num_of_nodes].append(net_name)

    return nets


"""
=====================================================================================================================
"""


def classify_nets_by_degree_ascending(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    returns its nets in ascending-degree order
    :param file_name: str
    :return nets: dict{int: [str, str,..., str]}
    """

    nets = {}
    counter = 0
    net_list = []

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    if num_of_nodes not in nets.keys():
                        nets[num_of_nodes] = []
                    nets[num_of_nodes].append(net_name)

    net_degrees = []
    for degree in nets:
        net_degrees.append(degree)
    net_degrees.sort()
    for degree in net_degrees:
        for net in nets[degree]:
            net_list.append(net)

    return net_list


"""
===================================================================================================================
"""


def classify_nets_list_by_degree(file_name, net_names):
    """
    @gt
    this function takes in as a parameter the name of the benchmark the user
    wants to search and a list of nets
    returns a dictionary where keys are the net degrees and values the net names
    :param file_name: str
    :param net_names: list[str, str,..., str]
    :return nets: dict{int: [str, str,..., str]}
    """

    nets = {}
    counter = 0
    nets_in = []

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    if net_name in net_names:
                        if num_of_nodes not in nets.keys():
                            nets[num_of_nodes] = []
                        nets[num_of_nodes].append(net_name)

    return nets


"""
====================================================================================================================
"""


def nets_in_area(file_name, xs, xf, ys, yf):
    """
    @gt
    this function takes in as a parameter the name of the benchmark the user
    wants to search in and start and finish width and height respectively
    returns all nets in given area
    :param file_name: str
    :param xs: int
    :param xf: int
    :param ys: int
    :param yf: int
    :return in_area: list[str, str,..., str]
    """

    nodes = {}
    netsx = {}
    netsy = {}
    counter = 0
    in_area = []

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] not in nodes:
                        nodes[line.split()[0]] = []
                        nodes[line.split()[0]].append(line.split()[1])
                        nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    netsx[net_name] = []
                    netsy[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if net_name in netsx:
                        if len(netsx[net_name]) == 0:
                            netsx[net_name].append(int(nodes[line.split()[0]][2]))
                            netsx[net_name].append(int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]))

                            netsy[net_name].append(int(nodes[line.split()[0]][3]))
                            netsy[net_name].append(int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]))
                        else:
                            if int(nodes[line.split()[0]][2]) < netsx[net_name][0]:
                                netsx[net_name][0] = int(nodes[line.split()[0]][2])

                            if int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]) > netsx[net_name][1]:
                                netsx[net_name][1] = int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0])

                            if int(nodes[line.split()[0]][3]) < netsy[net_name][0]:
                                netsy[net_name][0] = int(nodes[line.split()[0]][3])

                            if int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]) > netsy[net_name][1]:
                                netsy[net_name][1] = int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1])

    for net in netsx:
        if netsx[net][0] >= xs and netsx[net][1] <= xf:
            if netsy[net][0] >= ys and netsy[net][1] <= yf:
                in_area.append(net)

    return in_area


"""
====================================================================================================================
"""


def return_row_for_cell(file_name, node_name):
    """
    @gt
    this function takes in as a parameter a benchmark and a node
    and returns a list with the coordinates of the row(s) it's in
    :param file_name: str
    :param node_name: str
    :return to_return: list[int, int,..., int]
    """

    rows = {}
    nodes = []

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "Coordinate":
                    starting_height = int(line.split()[2])
                    if starting_height not in rows.keys():
                        rows[starting_height] = []
                if line.split()[0] == "Height":
                    ending_height = int(starting_height) + int(line.split()[2])
                    line_height = line.split()[2]
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = line.split()[2]
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    rows[starting_height].append(starting_x)
                    rows[starting_height].append(starting_height)
                    rows[starting_height].append(ending_x)
                    rows[starting_height].append(ending_height)

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] == node_name:
                        nodes.append(line.split()[1])
                        nodes.append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] == node_name:
                        nodes.append(line.split()[1])
                        nodes.append(int(line.split()[2]))

    keys_list = []

    for key in rows.keys():
        keys_list.append(int(key))

    if nodes[3] + int(nodes[1]) < keys_list[0] or nodes[3] > int(rows[keys_list[-1]][3]):
        print("cell out of chip")
        return []

    to_return = []

    appended = False

    if int(nodes[3]) not in keys_list:
        pos = bisect_left(keys_list, int(nodes[3]))
        pos -= 1
    else:
        pos = keys_list.index(int(nodes[3]))
    if (keys_list[pos]) in rows:
        if len(rows[keys_list[pos]]) == 4:
            if int(nodes[2]) + int(nodes[0]) <= int(rows[keys_list[pos]][2]) and int(nodes[2]) >= int(
                    rows[keys_list[pos]][0]):
                to_return.append(rows[keys_list[pos]][1])
            else:
                i = 4
                while i <= len(rows[keys_list[pos]]):
                    if int(nodes[2]) + int(nodes[0]) <= int(rows[keys_list[pos]][i - 2]) and int(nodes[2]) >= int(
                            rows[keys_list[pos]][i - 4]):
                        to_return.append(rows[keys_list[pos]][1])
                        appended = True
                    i += 4
                if not appended:
                    print("cell out of left or right chip-bounds")

    appended = False
    if bisect_left(keys_list, int(nodes[3]) + int(nodes[1])) - 1 != pos:
        if int(nodes[3]) not in keys_list:
            pos = bisect_left(keys_list, int(nodes[3]) + int(nodes[1]))
            pos -= 1
        else:
            pos = keys_list.index(int(nodes[3]) + int(nodes[1]))
        if (keys_list[pos]) in rows:
            if len(rows[keys_list[pos]]) == 4:
                if int(nodes[2]) + int(nodes[0]) <= int(rows[keys_list[pos]][2]) and int(nodes[2]) >= int(
                        rows[keys_list[pos]][0]):
                    to_return.append(rows[keys_list[pos]][1])
            else:
                i = 4
                while i <= len(rows[keys_list[pos]]):
                    if int(nodes[2]) + int(nodes[0]) <= int(rows[keys_list[pos]][i - 2]) and int(nodes[2]) > int(
                            rows[keys_list[pos]][i - 4]):
                        to_return.append(rows[keys_list[pos]][1])
                        appended = True
                    i += 4
                if not appended:
                    print("cell out of left or right chip-bounds")

    return to_return


"""
====================================================================================================================
"""


def total_hpwl(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    returns hpwl
    :param file_name: str
    :return hpwl: int
    """

    nodes = {}
    netsx = {}
    netsy = {}
    counter = 0
    hpwl = 0

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] not in nodes:
                        nodes[line.split()[0]] = []
                        nodes[line.split()[0]].append(line.split()[1])
                        nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    netsx[net_name] = []
                    netsy[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if net_name in netsx:
                        if len(netsx[net_name]) == 0:
                            netsx[net_name].append(int(nodes[line.split()[0]][2]))
                            netsx[net_name].append(int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]))

                            netsy[net_name].append(int(nodes[line.split()[0]][3]))
                            netsy[net_name].append(int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]))
                        else:
                            if int(nodes[line.split()[0]][2]) < netsx[net_name][0]:
                                netsx[net_name][0] = int(nodes[line.split()[0]][2])

                            if int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]) > netsx[net_name][1]:
                                netsx[net_name][1] = int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0])

                            if int(nodes[line.split()[0]][3]) < netsy[net_name][0]:
                                netsy[net_name][0] = int(nodes[line.split()[0]][3])

                            if int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]) > netsy[net_name][1]:
                                netsy[net_name][1] = int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1])

    for net in netsx:
        hpwl += float(netsx[net][1] - netsx[net][0] + netsy[net][1] - netsy[net][0])

    return (hpwl)


"""
====================================================================================================================
"""


def check_move_hpwl(file_name, node, x, y):
    """
    @gt
    this function takes in as a parameter a benchmark, a node
    and 2 coordinates x and y
    returns supposed hpwl if that node was moved to these coordinates
    :param file_name: str
    :param node: str
    :param x: int
    :param y: int
    :return hpwl: int
    """

    nodes = {}
    netsx = {}
    netsy = {}
    counter = 0
    hpwl = 0

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] not in nodes:
                        nodes[line.split()[0]] = []
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    nodes[node][2] = x
    nodes[node][3] = y

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()

            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    netsx[net_name] = []
                    netsy[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if net_name in netsx:
                        if len(netsx[net_name]) == 0:
                            netsx[net_name].append(int(nodes[line.split()[0]][2]))
                            netsx[net_name].append(int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]))

                            netsy[net_name].append(int(nodes[line.split()[0]][3]))
                            netsy[net_name].append(int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]))
                        else:
                            if int(nodes[line.split()[0]][2]) < netsx[net_name][0]:
                                netsx[net_name][0] = int(nodes[line.split()[0]][2])

                            if int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]) > netsx[net_name][1]:
                                netsx[net_name][1] = int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0])

                            if int(nodes[line.split()[0]][3]) < netsy[net_name][0]:
                                netsy[net_name][0] = int(nodes[line.split()[0]][3])

                            if int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]) > netsy[net_name][1]:
                                netsy[net_name][1] = int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1])

    for net in netsx:
        hpwl += float(netsx[net][1] - netsx[net][0] + netsy[net][1] - netsy[net][0])

    return (hpwl)


"""
===================================================================================================================
"""


def check_swap_cells_hpwl(file_name, node1, node2):
    """
    @gt
    this function takes in as a parameter a benchmark and two (2) nodes
    returns supposed hpwl if these nodes were swapped
    :param file_name: str
    :param node1: str
    :param node2: str
    :return hpwl: int
    """

    nodes = {}
    netsx = {}
    netsy = {}
    counter = 0
    hpwl = 0

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] not in nodes:
                        nodes[line.split()[0]] = []
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]].append(int(line.split()[1]))
                    nodes[line.split()[0]].append(int(line.split()[2]))

    nodes[node1][2] += nodes[node2][2]
    nodes[node2][2] = nodes[node1][2] - nodes[node2][2]
    nodes[node1][2] = nodes[node1][2] - nodes[node2][2]

    nodes[node1][3] += nodes[node2][3]
    nodes[node2][3] = nodes[node1][3] - nodes[node2][3]
    nodes[node1][3] = nodes[node1][3] - nodes[node2][3]

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()

            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n" + str(counter)
                    counter += 1
                    netsx[net_name] = []
                    netsy[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if net_name in netsx:
                        if len(netsx[net_name]) == 0:
                            netsx[net_name].append(int(nodes[line.split()[0]][2]))
                            netsx[net_name].append(int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]))

                            netsy[net_name].append(int(nodes[line.split()[0]][3]))
                            netsy[net_name].append(int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]))
                        else:
                            if int(nodes[line.split()[0]][2]) < netsx[net_name][0]:
                                netsx[net_name][0] = int(nodes[line.split()[0]][2])

                            if int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]) > netsx[net_name][1]:
                                netsx[net_name][1] = int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0])

                            if int(nodes[line.split()[0]][3]) < netsy[net_name][0]:
                                netsy[net_name][0] = int(nodes[line.split()[0]][3])

                            if int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]) > netsy[net_name][1]:
                                netsy[net_name][1] = int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1])

    for net in netsx:
        hpwl += float(netsx[net][1] - netsx[net][0] + netsy[net][1] - netsy[net][0])

    return (hpwl)


"""
====================================================================================================================
"""


def check_overflows(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    returns True if there are overflows
    False otherwise
    :param file_name: str
    :return bool
    """

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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

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


"""
====================================================================================================================
"""


def check_overlaps(file_name):
    """
    @gt
    this function takes in a benchmark as a parameter
    returns True if there are overlaps
    false otherwise
    :param file_name: str
    :return bool
    """

    place = {}
    size = {}
    sap = {}
    overlapping = []
    active_list = []
    max_width = 0

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = line.split()[2]
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    if ending_x > max_width:
                        max_width = ending_x

    divider = max_width // 10

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    size[line.split()[0]] = [line.split()[1], line.split()[2]]

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    place[line.split()[0]] = [line.split()[1], line.split()[2]]
                    sap_num = int(line.split()[1]) // divider
                    if sap_num not in sap.keys():
                        sap[sap_num] = []
                    sap[sap_num].append(
                        [line.split()[0], int(line.split()[1]), int(line.split()[1]) + int(size[line.split()[0]][0]),
                         int(line.split()[2]), "start"])

                    sap[sap_num].append(
                        [line.split()[0], int(line.split()[1]), int(line.split()[1]) + int(size[line.split()[0]][0]),
                         int(line.split()[2]) + int(size[line.split()[0]][1]), "end"])

    for lista in sap.values():
        lista.sort(key=lambda x: x[3])
        lista.sort(key=lambda x: x[4], reverse=True)
        for element in lista:
            if element[4] == "start":
                if len(active_list) == 0:
                    active_list.append(element[0])
                else:
                    for node in active_list:
                        if place[node][0] <= place[element[0]][0] + size[element[0]][0] and place[node][0] + size[node][
                            0] >= place[element[0]][0] and place[node][1] <= place[element[0]][1] + size[element[0]][
                                1] and place[node][1] + size[node][1] >= place[element[0]][1]:
                            return True
                    active_list.append(element[0])
            else:
                active_list.remove(element[0])

    return False


"""
====================================================================================================================
"""


def is_legalized(file_name):
    """
    @gt
    this function takes a benchmark as a parameter
    returns True if the benchmark is legalized
    False otherwise
    :param file_name: str
    :return bool
    """

    if not check_overflows(file_name) or not check_overlaps(file_name):
        return True
    return False


"""
=====================================================================================================================
"""


def get_overflows(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    returns a dictionary of the overflowing nodes
    keys are the nodes
    value is the overflow direction
    :param file_name: str
    :return overflows: dict{str: str}
    """

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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

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

    for node in nodes:
        if nodes[node][2] <= 0:
            overflows[node] = "W"
            continue

        if nodes[node][0] + nodes[node][2] >= max_width:
            overflows[node] = "E"
            continue

        if nodes[node][3] <= 0:
            overflows[node] = "S"
            continue

        if nodes[node][1] + nodes[node][3] >= max_height:
            overflows[node] = "N"

    return overflows


"""
====================================================================================================================
"""


def get_overlaps_row_alligned(file_name):
    """
    @gt
    this function takes in a benchmark as a parameter
    returns a list of the overlapping nodes
    if a node is floating between two rows, it is
    moved to the lowest row it occupies
    :param file_name: str
    :return overlapping: list[str, str,..., str]
    """

    place = {}
    size = {}
    rows = {}
    overlapping = []

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "Coordinate":
                    if line.split()[2] not in rows:
                        rows[int(line.split()[2])] = []
                if line.split()[0] == "Height":
                    row_height = line.split()[2]

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    size[line.split()[0]] = [line.split()[1], line.split()[2]]
                    if len(line.split()) == 4:
                        size[line.split()[0]].append("terminal")

    key_list = []

    for key in rows.keys():
        key_list.append(int(key))

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if "terminal" not in size[line.split()[0]]:
                        if int(line.split()[2]) not in rows.keys():
                            if int(line.split()[2]) < key_list[0]:
                                pos = 0
                            else:
                                pos = bisect_left(key_list, int(line.split()[2])) - 1
                            place[line.split()[0]] = [line.split()[1], key_list[pos]]
                            rows[key_list[pos]].append([line.split()[0], int(line.split()[1]),
                                                        int(line.split()[1]) + int(size[line.split()[0]][0]),
                                                        key_list[pos], key_list[pos] + int(size[line.split()[0]][1])])
                            continue

                    place[line.split()[0]] = [line.split()[1], line.split()[2]]

                    if int(line.split()[2]) not in rows.keys():
                        rows[int(line.split()[2])] = []
                    rows[int(line.split()[2])].append(
                        [line.split()[0], int(line.split()[1]), int(line.split()[1]) + int(size[line.split()[0]][0]),
                         int(line.split()[2]), int(line.split()[2]) + int(size[line.split()[0]][1])])

    for node_list in rows.values():
        node_list.sort(key=lambda x: x[1])
        for i in range(len(node_list)):
            if len(node_list) <= 1:
                break
            if i == 0:
                if node_list[i][1] <= node_list[i + 1][2] and node_list[i][2] >= node_list[i + 1][1] and node_list[i][
                        3] <= node_list[i + 1][4] and node_list[i][4] >= node_list[i + 1][3]:
                    overlapping.append(node_list[i][0])
            elif i == len(node_list) - 1:
                if node_list[i - 1][1] <= node_list[i][2] and node_list[i - 1][2] >= node_list[i][1] and \
                        node_list[i - 1][3] <= node_list[i][4] and node_list[i - 1][4] >= node_list[i][3]:
                    overlapping.append(node_list[i][0])
            else:
                if node_list[i][1] <= node_list[i + 1][2] and node_list[i][2] >= node_list[i + 1][1] and node_list[i][
                        3] <= node_list[i + 1][4] and node_list[i][4] >= node_list[i + 1][3]:
                    overlapping.append(node_list[i][0])
                    continue

                if node_list[i - 1][1] <= node_list[i][2] and node_list[i - 1][2] >= node_list[i][1] and \
                        node_list[i - 1][3] <= node_list[i][4] and node_list[i - 1][4] >= node_list[i][3]:
                    overlapping.append(node_list[i][0])

    return overlapping


"""
=====================================================================================================================
"""


def get_overlaps(file_name):
    """
    @gt
    this function takes in a benchmark as a parameter
    returns lists the overlapping nodes
    :param file_name: str
    :return overlapping: list[(str, str), (str, str),..., (str, str)]
    """

    place = {}
    size = {}
    sap = {}
    overlapping = []
    active_list = []
    max_width = 0

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = line.split()[2]
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    if ending_x > max_width:
                        max_width = ending_x

    divider = max_width // 10

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if len(line.split()) == 3:
                        size[line.split()[0]] = [line.split()[1], line.split()[2]]

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in size:
                        place[line.split()[0]] = [line.split()[1], line.split()[2]]
                        sap_num = int(line.split()[1]) // divider
                        if sap_num not in sap.keys():
                            sap[sap_num] = []
                        sap[sap_num].append([line.split()[0], int(line.split()[1]),
                                             int(line.split()[1]) + int(size[line.split()[0]][0]), int(line.split()[2]),
                                             "start"])

                        sap[sap_num].append([line.split()[0], int(line.split()[1]),
                                             int(line.split()[1]) + int(size[line.split()[0]][0]),
                                             int(line.split()[2]) + int(size[line.split()[0]][1]), "end"])

    for lista in sap.values():
        lista.sort(key=lambda x: x[3])
        lista.sort(key=lambda x: x[4], reverse=True)
        for element in lista:
            if element[4] == "start":
                if len(active_list) == 0:
                    active_list.append(element[0])
                else:
                    for node in active_list:
                        if place[node][0] <= place[element[0]][0] + size[element[0]][0] and place[node][0] + size[node][
                            0] >= place[element[0]][0] and place[node][1] <= place[element[0]][1] + size[element[0]][
                                1] and place[node][1] + size[node][1] >= place[element[0]][1]:
                            overlap = (node, element[0])
                            overlapping.append(overlap)
                    active_list.append(element[0])
            else:
                active_list.remove(element[0])

    return overlapping


"""
====================================================================================================================
"""


def comp_overlap(file_name1, file_name2):
    """
    @gt
    this function takes as a parameter two benchmarks and compares their overlaps
    returns a list
    1st index: benchmark with least overlaps (1=first, 2=second, 0=equal)
    2nd index: the better overlap
    3rd index: overlap difference
    :param file_name1: str
    :param file_name2: str
    :return list[int, int, int]
    """
    overlap1 = len(get_overlaps(file_name1))
    overlap2 = len(get_overlaps(file_name2))


    if overlap1 > overlap2:
        return [2, overlap2, overlap1-overlap2]
    elif overlap2 > overlap1:
        return [1, overlap1, overlap2-overlap1]
    else:
        return [0, overlap1, 0]


"""
====================================================================================================================
"""


def comp_overflow(file_name1, file_name2):
    """
    @gt
    this function takes in as a parameter two (2) benchmarks
    and compares their overflows
    returns a list
    1st index: file with least overflows (1 for first, 2 for second, 0 for equal)
    2nd index: the winner file's number of overflows
    3rd index: the difference between the two (2) overfows
    :param file_name1: str
    :param file_name2: str
    :return list[int, int, int]
    """
    overflow1 = len(get_overflows(file_name1))
    overflow2 = len(get_overflows(file_name2))

    if overflow1 > overflow2:
        return [2, overflow2, overflow1 - overflow2]
    elif overflow2 > overflow1:
        return [1, overflow1, overflow2 - overflow1]
    else:
        return [0, overflow1, 0]


"""
=====================================================================================================================
"""


def comp_overlap_row_alligned(file_name1, file_name2):
    """
    @gt
    this function takes as a parameter two benchmarks and compares their overlaps
    returns a list
    1st index: benchmark with least overlaps (1=first, 2=second, 0=equal)
    2nd index: the better overlap
    3rd index: overlap difference
    :param file_name1: str
    :param file_name2: str
    :return list[int, int, int]
    """
    overlap1 = len(get_overlaps_row_alligned(file_name1))
    overlap2 = len(get_overlaps_row_alligned(file_name2))

    if overlap1 > overlap2:
        return [2, overlap2, overlap1-overlap2]
    elif overlap2 > overlap1:
        return [1, overlap1, overlap2-overlap1]
    else:
        return [0, overlap1, 0]


"""
====================================================================================================================
"""


def compare_wirelength(file_name1, file_name2):
    """
    @gt
    this function takes as a parameter two (2) benchmarks
    and compares their total hpwl
    returns a list
    1st index: the file with the smaller total hpwl
    (1 for first, 2 for second, 0 for equal)
    2nd index: the smaller of the two (2) total hpwls
    3rd index: the difference between the two (2) total hpwls
    :param file_name1: str
    :param file_name2: str
    :return list[int, int, int]
    """
    hpwl1 = total_hpwl(file_name1)
    hpwl2 = total_hpwl(file_name2)

    if hpwl1 < hpwl2:
        return [1, hpwl1, hpwl1-hpwl2]
    elif hpwl2 < hpwl1:
        return [2, hpwl2, hpwl2-hpwl1]
    else:
        return [0, hpwl1, 0]


"""
====================================================================================================================
"""


def comp_nets_wirelength(filename1, net1, filename2, net2):
    """
    @gt
    this function takes in two (2) benchmarks and two (2) nets
    finds wirelength of first net in first benchmark
    and compares it to the wirelength of the second net in
    the second benchmark
    returns a list
    1st index: winning net, 1 = first, 2 = second, 0 = equal
    2nd index: net's wirelength
    3rd index: wirelength difference
    :param file_name1: str
    :param net1: str
    :param file_name2: str
    :param net2: str
    :return list[int, int, int]
    """
    hpwl1 = hpwl_for_net(filename1, net1)
    hpwl2 = hpwl_for_net(filename2, net2)

    if hpwl1 < hpwl2:
        return [1, hpwl1, hpwl2 - hpwl1]
    elif hpwl2 < hpwl1:
        return [2, hpwl2, hpwl1 - hpwl2]
    else:
        return [0, hpwl1, 0]


"""
====================================================================================================================
"""


def comp_cell_position(filename1, filename2, node):
    """
    @gt
    This function takes as a parameter two (2) pl files and a node
    compares the position of the node in the two (2) files
    returns a dictionary
    key: node name
    value: a list
    1st index: coordinates of node in first file
    2nd index: coordinates of node in second file
    3rd index: the difference between the previous coordinates
    :param file_name1: str
    :param file_name2: str
    :param node: str
    :return node_comp: dict{str: [int, int, int]}
    """
    coordinates1 = get_coordinates(filename1, node)
    coordinates2 = get_coordinates(filename2, node)

    difference = [abs(float(coordinates1[0])-float(coordinates2[0])),
                  abs(float(coordinates1[1])-float(coordinates2[1]))]
    node_comp = {node: [coordinates1, coordinates2, difference]}

    return node_comp


"""
===================================================================================================================
"""


def chip_size(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    and returns its size as float
    :param file_name: str
    :return chip_size: float
    """

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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

    chip_size = float(max_height * max_width)

    return chip_size


"""
===================================================================================================================
"""


def generate_statistics_unplaced_design(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    and returns a list of statistics, row-related,
    then node-related and then net-related
    spcifically, returns number of rows, max chip width,
    max chip height, total node number, terminal-node number,
    non-terminal-node number, total net number, largest net weight
    and number of nets per existing weight
    in that order
    :param file_name: str
    :return list[int, int, int, int, int, int, int, int, int]
    """

    rows = []
    max_width = 0
    max_net_nodes = 0
    net_weight = {}

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "NumRows":
                    rows_num = line.split()[2]
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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if line.split()[0] == "NumNodes":
                    nodes_num = int(line.split()[2])
                if line.split()[0] == "NumTerminals":
                    terminal_num = int(line.split()[2])
                    non_terminal_num = nodes_num - terminal_num

    with open(file_name + ".nets") as f:
        num_of_nodes = -1
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NumNets" in line:
                    net_num = int(line.split()[2])
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    if num_of_nodes > max_net_nodes:
                        max_net_nodes = num_of_nodes
                    if num_of_nodes not in net_weight.keys():
                        net_weight[num_of_nodes] = 0
                    net_weight[num_of_nodes] += 1

    return [rows_num, max_width, max_height, nodes_num, terminal_num, non_terminal_num, net_num, max_net_nodes,
            net_weight]


"""
===================================================================================================================
"""


def generate_statistics_placed_design(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    and returns a list of statistics, row-related,
    then node-related and then net-related
    specifically, returns number of rows, max chip width,
    max chip height, total node number, terminal-node number,
    non-terminal-node number, total net number, largest net weight
    and number of nets per existing weight
    in that order
    :param file_name: str
    :return list[int, int, int, int, int, int, int, int, int]
    """

    rows = []
    max_width = 0
    max_net_nodes = 0
    net_weight = {}

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "NumRows":
                    rows_num = line.split()[2]
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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if line.split()[0] == "NumNodes":
                    nodes_num = int(line.split()[2])
                if line.split()[0] == "NumTerminals":
                    terminal_num = int(line.split()[2])
                    non_terminal_num = nodes_num - terminal_num

    with open(file_name + ".nets") as f:
        num_of_nodes = -1
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NumNets" in line:
                    net_num = int(line.split()[2])
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    if num_of_nodes > max_net_nodes:
                        max_net_nodes = num_of_nodes
                    if num_of_nodes not in net_weight.keys():
                        net_weight[num_of_nodes] = 0
                    net_weight[num_of_nodes] += 1

    return [rows_num, max_width, max_height, nodes_num, terminal_num, non_terminal_num, net_num, max_net_nodes,
            net_weight]


"""
====================================================================================================================
"""


def left_allign_maintaining_order(file_name, row_height):
    """
    @gt
    this function takes in as a parameter a benchmark
    and the height of a row.
    Alligns all nodes from left to right
    :param file_name: str
    :param row_height: int
    :return:
    """

    nodes = {}
    nodes_list = []
    to_change = []

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if int(line.split()[2]) == row_height:
                        to_change.append(line)
                        nodes[line.split()[0]] = []
                        nodes[line.split()[0]].append(int(line.split()[1]))
                        nodes[line.split()[0]].append(int(line.split()[2]))

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in nodes:
                        if len(line.split()) == 4:
                            del nodes[line.split()[0]]
                        else:
                            nodes[line.split()[0]].append(int(line.split()[1]))
                            nodes[line.split()[0]].append(int(line.split()[2]))

    with open(file_name + ".pl") as f:
        data = f.readlines()

    for key in nodes.keys():
        nodes_list.append([key, nodes[key][0], nodes[key][1], nodes[key][2], nodes[key][3]])

    new_node_list = []

    nodes_list.sort(key=lambda x: x[1])
    new_node_list.append(nodes_list[0])

    for k in range(len(nodes_list) - 1):
        new_node_list.append(nodes_list[k + 1])
        if nodes_list[k + 1][1] - (nodes_list[k][1] + nodes_list[k][3]) != 1:
            new_node_list[-1][1] = nodes_list[k][1] + nodes_list[k][3] + 1

    for line in to_change:
        x = to_change.index(line)
        for node in new_node_list:

            if re.search(r'\b' + line.split()[0] + r'\b', node[0]):
                substring = line[7:]
                substring = substring.replace(line.split()[1], str(node[1]), 1)
                line = line.replace(line[7:], substring)
                to_change[x] = line

    for i in range(len(data)):
        for node in to_change:
            if re.search(r'\b' + node.split()[0] + r'\b', data[i]):
                data[i] = node + "\n"

    with open(file_name + ".pl", 'w') as p:
        p.writelines(data)


"""
=====================================================================================================================
"""


def create_adjacency_matrix(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    creates and returns an adjacency sparse matrix showing node correaltion
    :param file_name: str
    :return adjacency_matrix: lil_matrix
    """
    nodes = {}
    nets = {}
    coordinatesx = {}
    coordinatesy = {}
    counter = 0

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    coordinatesx[counter] = int(line.split()[1])
                    coordinatesy[counter] = int(line.split()[2])
                    counter += 1

    adjacency_matrix = sp.lil_matrix((counter, counter), dtype=float)

    counter = 0

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]] = counter
                    counter += 1

    counter = 0

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    net_name = "n" + str(counter)
                    counter += 1
                    nets[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    for net in nets[net_name]:
                        adjacency_matrix[nodes[net], nodes[line.split()[0]]] = math.sqrt(
                            (coordinatesx[nodes[net]] - coordinatesx[nodes[line.split()[0]]]) ** 2 + (
                                        coordinatesy[nodes[net]] - coordinatesy[nodes[line.split()[0]]]) ** 2)

                        adjacency_matrix[nodes[line.split()[0]], nodes[net]] = math.sqrt(
                            (coordinatesx[nodes[line.split()[0]]] - coordinatesx[nodes[net]]) ** 2 + (
                                        coordinatesy[nodes[line.split()[0]]] - coordinatesy[nodes[net]]) ** 2)

                    nets[net_name].append(line.split()[0])

    return adjacency_matrix


"""
====================================================================================================================
"""


def chip_area(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    and returns its available area as float
    :param file_name: str
    :return chip_area: float
    """

    rows = []
    max_width = 0
    size = {}

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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if len(line.split()) == 4:
                        size[line.split()[0]] = [int(line.split()[1]), int(line.split()[2])]

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in size:
                        if int(line.split()[1]) > max_width or int(line.split()[2]) > max_height or int(
                                line.split()[1]) + size[line.split()[0]][0] < 0 or int(line.split()[2]) + \
                                size[line.split()[0]][1] < 0:
                            del size[line.split()[0]]

    chip_area = float(max_height * max_width)
    for node in size.values():
        chip_area -= float(node[0] * node[1])

    return chip_area


"""
===================================================================================================================
"""


def right_allign_maintaining_order(file_name, row_height):
    '''
    @gt
    this function takes in as a parameter a benchmark
    and the height of a row.
    Alligns all nodes from right to left
    :param file_name: str
    :param row_height: int
    :return
    '''

    nodes = {}
    nodes_list = []
    to_change = []

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if int(line.split()[2]) == row_height:
                        to_change.append(line)
                        nodes[line.split()[0]] = []
                        nodes[line.split()[0]].append(int(line.split()[1]))
                        nodes[line.split()[0]].append(int(line.split()[2]))

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in nodes:
                        if len(line.split()) == 4:
                            del nodes[line.split()[0]]
                        else:
                            nodes[line.split()[0]].append(int(line.split()[1]))
                            nodes[line.split()[0]].append(int(line.split()[2]))

    with open(file_name + ".pl") as f:
        data = f.readlines()

    for key in nodes.keys():
        nodes_list.append([key, nodes[key][0], nodes[key][1], nodes[key][2], nodes[key][3]])

    new_node_list = []

    nodes_list.sort(key=lambda x: x[1], reverse=True)
    new_node_list.append(nodes_list[0])

    for k in range(len(nodes_list) - 1):
        new_node_list.append(nodes_list[k + 1])
        if nodes_list[k][1] - (nodes_list[k + 1][1] + nodes_list[k + 1][3]) != 1:
            new_node_list[-1][1] = nodes_list[k][1] - nodes_list[k][3] - 1

    for line in to_change:
        x = to_change.index(line)
        for node in new_node_list:

            if re.search(r'\b' + line.split()[0] + r'\b', node[0]):
                substring = line[7:]
                substring = substring.replace(line.split()[1], str(node[1]), 1)
                line = line.replace(line[7:], substring)
                to_change[x] = line

    for i in range(len(data)):
        for node in to_change:
            if re.search(r'\b' + node.split()[0] + r'\b', data[i]):
                data[i] = node + "\n"

    with open(file_name + ".pl", 'w') as p:
        p.writelines(data)


"""
===================================================================================================================
"""


def create_connectivity_matrix(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    creates and returns a connectivity sparse matrix showing node correaltion
    :param file_name: str
    :return connectivity_matrix: lil_matrix
    """
    nodes = {}
    nets = {}
    coordinatesx = {}
    coordinatesy = {}
    counter = 0

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    coordinatesx[counter] = int(line.split()[1])
                    coordinatesy[counter] = int(line.split()[2])
                    coordinatesx[counter + 1] = 0
                    coordinatesy[counter + 1] = 0
                    counter += 2

    connectivity_matrix = sp.lil_matrix((counter, counter), dtype=float)

    counter = 0

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]] = counter
                    counter += 2

    counter = 0

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if "NetDegree" in line:
                    net_name = "n" + str(counter)
                    counter += 1
                    nets[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if len(line.split()) == 5:
                        coordinatesx[nodes[line.split()[0]] + 1] = coordinatesx[nodes[line.split()[0]]] + int(
                            line.split()[3])
                        coordinatesy[nodes[line.split()[0]] + 1] = coordinatesy[nodes[line.split()[0]]] + int(
                            line.split()[4])
                    for net in nets[net_name]:
                        connectivity_matrix[nodes[net], nodes[line.split()[0]]] = math.sqrt(
                            (coordinatesx[nodes[net]] - coordinatesx[nodes[line.split()[0]]]) ** 2 + (
                                        coordinatesy[nodes[net]] - coordinatesy[nodes[line.split()[0]]]) ** 2)

                        connectivity_matrix[nodes[line.split()[0]], nodes[net]] = math.sqrt(
                            (coordinatesx[nodes[line.split()[0]]] - coordinatesx[nodes[net]]) ** 2 + (
                                        coordinatesy[nodes[line.split()[0]]] - coordinatesy[nodes[net]]) ** 2)

                        connectivity_matrix[nodes[net] + 1, nodes[line.split()[0]] + 1] = math.sqrt(
                            (coordinatesx[nodes[net] + 1] - coordinatesx[nodes[line.split()[0]] + 1]) ** 2 + (
                                        coordinatesy[nodes[net] + 1] - coordinatesy[nodes[line.split()[0]] + 1]) ** 2)

                        connectivity_matrix[nodes[line.split()[0]] + 1, nodes[net] + 1] = math.sqrt(
                            (coordinatesx[nodes[line.split()[0]] + 1] - coordinatesx[nodes[net] + 1]) ** 2 + (
                                        coordinatesy[nodes[line.split()[0]] + 1] - coordinatesy[nodes[net] + 1]) ** 2)

                    nets[net_name].append(line.split()[0])

    return connectivity_matrix


"""
====================================================================================================================
"""


def plot_chip_macros_only(file_name):
    """
    @gt
    this function takes a benchmark as a parameter
    plots all macros of the chip
    :param file_name: str
    :return
    """

    nodes = {}

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if len(line.split()) == 4:
                        nodes[line.split()[0]] = [float(line.split()[1]), float(line.split()[2])]

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in nodes:
                        nodes[line.split()[0]].append(float(line.split()[1]))
                        nodes[line.split()[0]].append(float(line.split()[2]))

    fig1 = plt.figure()

    for node in nodes.values():
        ax1 = fig1.add_subplot(111)
        ax1.add_patch(
        patches.Rectangle(
        (node[2], node[3]),
        node[0],
        node[1],

        facecolor="none", edgecolor="black", linewidth=0.5, linestyle='solid'
        )
        )
        ax1.plot()
    plt.show()


"""
====================================================================================================================
"""


def plot_area_macros_only(file_name, xs, xf, ys, yf):
    """
    @gt
    this function takes a benchmark and four (4) integers as a parameter,
    two (2) x values and two (2) y values
    plots all macros of the chip that are exclusively in that area
    :param file_name: str
    :param xs: int
    :param xf: int
    :param ys: int
    :param yf: int
    :return
    """

    nodes = {}

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if len(line.split()) == 4:
                        nodes[line.split()[0]] = [float(line.split()[1]), float(line.split()[2])]

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in nodes:
                        if xs <= int(line.split()[1]) and nodes[line.split()[0]][0] + int(line.split()[1]) <= xf\
                                and ys <= int(line.split()[2])\
                                and nodes[line.split()[0]][1] + int(line.split()[2]) <= yf:
                            nodes[line.split()[0]].append(float(line.split()[1]))
                            nodes[line.split()[0]].append(float(line.split()[2]))
                        else:
                            del nodes[line.split()[0]]

    fig1 = plt.figure()

    for node in nodes.values():
        ax1 = fig1.add_subplot(111)
        ax1.add_patch(
        patches.Rectangle(
        (node[2], node[3]),
        node[0],
        node[1],

        facecolor="red", edgecolor="black", linewidth=0.5, linestyle='solid'
        )
        )
        ax1.plot()
    plt.show()


"""
=====================================================================================================================
"""


def plot_overlaps(file_name):
    """
    @gt
    this function takes in a benchmark as a parameter
    plots all the non-terminal nodes that overlap
    :param file_name: str
    :return
    """

    place = {}
    size = {}
    sap = {}
    overlapping = []
    active_list = []
    max_width = 0

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = line.split()[2]
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    if ending_x > max_width:
                        max_width = ending_x

    divider = max_width // 10

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if len(line.split()) == 3:
                        size[line.split()[0]] = [line.split()[1], line.split()[2]]

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):

            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in size:
                        place[line.split()[0]] = [line.split()[1], line.split()[2]]
                        sap_num = int(line.split()[1]) // divider
                        if sap_num not in sap.keys():
                            sap[sap_num] = []
                        sap[sap_num].append([line.split()[0], int(line.split()[1]),
                                             int(line.split()[1]) + int(size[line.split()[0]][0]), int(line.split()[2]),
                                             "start"])

                        sap[sap_num].append([line.split()[0], int(line.split()[1]),
                                             int(line.split()[1]) + int(size[line.split()[0]][0]),
                                             int(line.split()[2]) + int(size[line.split()[0]][1]), "end"])

    for lista in sap.values():
        lista.sort(key=lambda x: x[3])
        lista.sort(key=lambda x: x[4], reverse=True)
        for element in lista:
            if element[4] == "start":
                if len(active_list) == 0:
                    active_list.append(element[0])
                else:
                    for node in active_list:
                        if place[node][0] <= place[element[0]][0] + size[element[0]][0] and place[node][0] + size[node][
                            0] >= place[element[0]][0] and place[node][1] <= place[element[0]][1] + size[element[0]][
                                1] and place[node][1] + size[node][1] >= place[element[0]][1]:
                            if node not in overlapping:
                                overlapping.append(node)
                            if element[0] not in overlapping:
                                overlapping.append(element[0])
                    active_list.append(element[0])
            else:
                active_list.remove(element[0])

    fig1 = plt.figure()

    for node in overlapping:
        ax1 = fig1.add_subplot(111)
        ax1.add_patch(
            patches.Rectangle(
                (float(place[node][0]), float(place[node][1])),
                float(size[node][0]),
                float(size[node][1]),

                facecolor="none", edgecolor="black", linewidth=0.5, linestyle='solid'
            )
        )
        ax1.plot()
    plt.show()


"""
====================================================================================================================
"""


def plot_overflows(file_name):
    """
    @gt
    this function takes in as a parameter a benchmark
    finds and plots the overflowing, non-terminal nodes
    :param file_name: str
    :return
    """

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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

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

    for node in nodes:
        if nodes[node][2] <= 0:
            overflows[node] = "W"
            continue

        if nodes[node][0] + nodes[node][2] >= max_width:
            overflows[node] = "E"
            continue

        if nodes[node][3] <= 0:
            overflows[node] = "S"
            continue

        if nodes[node][1] + nodes[node][3] >= max_height:
            overflows[node] = "N"

    fig1 = plt.figure()

    for node in overflows:
        ax1 = fig1.add_subplot(111)
        ax1.add_patch(
            patches.Rectangle(
                (float(nodes[node][2]), float(nodes[node][3])),
                float(nodes[node][0]),
                float(nodes[node][1]),

                facecolor="none", edgecolor="black", linewidth=0.5, linestyle='solid'
            )
        )
        ax1.plot()
    plt.show()


"""
===================================================================================================================
"""


def plot_density_map(file_name, divider):
    '''
    @gt
    this function takes in as a parameter a benchmark and a number x
    divides the chip in x*x parts and plots the density of each part
    green being 25% or less, red being 76% or more
    :param file_name: str
    :param divider: int
    :return
    '''

    rows = []
    max_width = 0
    bins = []

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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

    for i in range(divider):
        for j in range(divider):
            start_x = (j) * (max_width / divider)
            start_y = (i) * (max_height / divider)
            end_x = (j + 1) * (max_width / divider)
            end_y = (i + 1) * (max_height / divider)

            bins.append([start_x, start_y, end_x, end_y])

    fig1 = plt.figure()

    for area in bins:

        percentage = density_in_coordinates(file_name + ".pl", area[1], area[0], area[3], area[2])

        if percentage <= 0.25:
            facecolor = "green"
        elif percentage <= 0.5:
            facecolor = "yellow"
        elif percentage <= 0.75:
            facecolor = "orange"
        else:
            facecolor = "red"

        ax1 = fig1.add_subplot(111)
        ax1.add_patch(
            patches.Rectangle(
                (area[0], area[1]),
                area[2] - area[0],
                area[3] - area[1],

                facecolor=facecolor, edgecolor="black", linewidth=0.5, linestyle='solid'
            )
        )
        ax1.plot()
    plt.show()


"""
===================================================================================================================
"""


def plot_density_map_area(file_name, xs, ys, xf, yf, divider):
    '''
    @gt
    this function takes in as a parameter a benchmark, a number x
    and four (4) coordinates (starting and finishing x and y)
    divides these coordinates of the chip in x*x parts and plots the density of each part
    green being 25% or less, red being 76% or more
    :param file_name: str
    :param xs: int
    :param xf: int
    :param ys: int
    :param yf: int
    :param divider: int
    :return
    '''

    rows = []
    max_width = 0
    bins = []

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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

    step_x = int((xf - xs) / divider) + 1
    step_y = int((yf - ys) / divider) + 1

    for i in range(ys, yf, step_y):
        for j in range(xs, xf, step_x):
            start_x = j
            start_y = i
            end_x = j + step_x
            end_y = i + step_y

            bins.append([start_x, start_y, end_x, end_y])

    fig1 = plt.figure()

    for area in bins:

        percentage = density_in_coordinates(file_name + ".pl", area[1], area[0], area[3], area[2])

        if percentage <= 0.25:
            facecolor = "green"
        elif percentage <= 0.5:
            facecolor = "yellow"
        elif percentage <= 0.75:
            facecolor = "orange"
        else:
            facecolor = "red"

        ax1 = fig1.add_subplot(111)
        ax1.add_patch(
            patches.Rectangle(
                (area[0], area[1]),
                area[2] - area[0],
                area[3] - area[1],

                facecolor=facecolor, edgecolor="black", linewidth=0.5, linestyle='solid'
            )
        )
        ax1.plot()
    plt.show()


"""
===================================================================================================================
"""


def chip_dimensions(file_name):
    '''
    @gt
    this function takes in as a parameter a benchmark
    and returns its starting and finishing coordinates in a list
    :param file_name: str
    :return list[int, int, int, int]
    '''

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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

    return [0, 0, max_width, max_height]


"""
===================================================================================================================
"""


def create_uniform_bins(file_name, divider):
    '''
    @gt
    this function takes in as a parameter a benchmark and a number x
    divides the chip in x*x parts and returns a dictionary with the
    starting and finishing coordinates of each part
    :param file_name: str
    :param divider: int
    :return
    '''

    rows = []
    max_width = 0
    bins = {}

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
                    rows.append([starting_x, starting_height, ending_x, ending_height])

    max_height = rows[-1][3]

    counter = 0

    for i in range(divider):
        for j in range(divider):
            start_x = (j) * (max_width / divider)
            start_y = (i) * (max_height / divider)
            end_x = (j + 1) * (max_width / divider)
            end_y = (i + 1) * (max_height / divider)

            bins[counter] = [start_x, start_y, end_x, end_y]
            counter += 1

    return bins


"""
===================================================================================================================
"""


def plot_area(pl_file_name, leftx, lowy, rightx, highy):
    """
    @gk
    This function takes as input a benchmark's pl file,
    and xy-s that define an area and plots that area.
    :param pl_file_name:
    :param leftx:
    :param lowy:
    :param rightx:
    :param highy:
    :return:
    """

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import warnings
    import matplotlib.cbook
    warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

    start = time.time()

    data = []
    cells = {}
    lines = {}
    line_number = ly = uy = lx = rx = sitesp = 0

    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                cells[data[0]] = [float(data[1])]
                cells[data[0]].append(float(data[2]))

    with open(pl_file_name.replace('pl', 'nodes')) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n'\
                        or 'NumNodes' in line or 'NumTerminals' in line:
                continue
            else:
                data = line.split()
                cells[data[0]].append(float(data[1]))
                cells[data[0]].append(float(data[2]))

    with open(pl_file_name.replace('pl', 'scl')) as s:
        for num, line in enumerate(s):
            if num == 0 or '#' in line or line == '\n' or 'NumRows' in line:
                continue
            else:
                if 'CoreRow' in line:
                    line_number += 1
                if 'Coordinate' in line:
                    data = line.split()
                    ly = float(data[2])
                    lines['line' + str(line_number)] = [ly]
                if 'Height' in line:
                    data = line.split()
                    uy = float(data[2])
                    lines['line' + str(line_number)].append(uy)
                if 'Sitespacing' in line:
                    data = line.split()
                    sitesp = float(data[2])
                if 'SubrowOrigin' in line:
                    data = line.split()
                    lx = float(data[2])
                    rx = float(data[5]) * sitesp
                    lines['line' + str(line_number)].append(lx)
                    lines['line' + str(line_number)].append(rx)

    keys_to_del = []
    for c in cells.items():
        if leftx <= c[1][0] < rightx and lowy <= c[1][1] < highy:
            continue
        else:
            keys_to_del.append(c[0])

    for key in keys_to_del:
        del cells[key]

    keys_to_del.clear()
    for l in lines.items():
        if leftx <= l[1][2] < rightx and lowy <= l[1][0] < highy:
            continue
        else:
            keys_to_del.append(l[0])

    for key in keys_to_del:
        del lines[key]

    fig = plt.figure(num=pl_file_name.replace('.pl', ''))
    for l in lines.items():
        ax1 = fig.add_subplot(111, aspect='equal', adjustable='datalim')
        ax1.add_patch(patches.Rectangle(
            (l[1][2], l[1][0]),
            l[1][3],
            l[1][1],
            fill=False
        ))
        ax1.plot()

    for c in cells.items():
        ax2 = fig.add_subplot(111, aspect='equal', adjustable='datalim')
        ax2.add_patch(patches.Rectangle(
            (c[1][0], c[1][1]),
            c[1][2],
            c[1][3],
            fill=False
        ))
        ax2.plot()

    print(time.time() - start)

    plt.show()


"""
===================================================================================================================
"""


def plot_cells(pl_file_name, set_of_cells):
    """
    @gk
    This function takes a benchmark's pl file and a list of nodes' names
    and plots the cells as a rectangle in the same figure plot.
    :param pl_file_name:
    :param set_of_cells:
    :return:
    """

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import warnings
    import matplotlib.cbook
    warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

    data = []
    nodes = {}

    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if '#' in line or num == 0 or line == '\n':
                continue
            else:
                data.append(line.split())

    for n in set_of_cells:
        for d in data:
            if n == d[0]:
                nodes[d[0]] = [float(d[1])]
                nodes[d[0]].append(float(d[2]))

    with open(pl_file_name.replace('pl', 'nodes')) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n'\
                    or 'NumNodes' in line or 'NumTerminals' in line:
                continue
            else:
                data = line.split()
                if data[0] in nodes.keys():
                    nodes[data[0]].append(float(data[1]))
                    nodes[data[0]].append(float(data[2]))

    fig = plt.figure(num='Set Of Cells')
    for n in nodes.items():
        ax = fig.add_subplot(111, aspect='equal', adjustable='datalim')
        ax.add_patch(patches.Rectangle(
            (float(n[1][0]), float(n[1][1])),
            float(n[1][2]),
            float(n[1][3]),
            fill=False
        ))
        ax.plot()
    plt.show()


"""
===================================================================================================================
"""


def plot_compare_cells(pl_file1, pl_file2, cell_pl1, cell_pl2):
    """
    @gk
    This function takes as input two benchmarks' pl files and
    a node for each file, and plots them colored red and green accordingly.
    :param pl_file1:
    :param pl_file2:
    :param cell_pl1:
    :param cell_pl2:
    :return:
    """

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import warnings
    import matplotlib.cbook
    warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

    start = time.time()

    data = []
    cell_1 = []
    cell_2 = []

    with open(pl_file1) as pl1:
        for num, line in enumerate(pl1):
            if cell_pl1 in line:
                data = line.split()
                if data[0] == cell_pl1:
                    cell_1.append(float(data[1]))
                    cell_1.append(float(data[2]))
                    break

    with open(pl_file1.replace('pl', 'nodes')) as n1:
        for num, line in enumerate(n1):
            if cell_pl1 in line:
                data = line.split()
                if data[0] == cell_pl1:
                    cell_1.append(float(data[1]))
                    cell_1.append(float(data[2]))
                    break

    with open(pl_file2) as pl2:
        for num, line in enumerate(pl2):
            if cell_pl2 in line:
                data = line.split()
                if data[0] == cell_pl2:
                    cell_2.append(float(data[1]))
                    cell_2.append(float(data[2]))
                    break

    with open(pl_file2.replace('pl', 'nodes')) as n2:
        for num, line in enumerate(n2):
            if cell_pl2 in line:
                data = line.split()
                if data[0] == cell_pl2:
                    cell_2.append(float(data[1]))
                    cell_2.append(float(data[2]))
                    break

    fig = plt.figure(num=cell_pl1 + ' ' + cell_pl2)
    ax1 = fig.add_subplot(111, aspect='equal', adjustable='datalim')
    ax1.add_patch(patches.Rectangle(
        (cell_1[0], cell_1[1]),
        cell_1[2],
        cell_1[3],
        facecolor='red',
        label=cell_pl1
    ))
    ax1.plot()
    ax2 = fig.add_subplot(111, aspect='equal', adjustable='datalim')
    ax2.add_patch(patches.Rectangle(
        (cell_2[0], cell_2[1]),
        cell_2[2],
        cell_2[3],
        facecolor='green',
        label=cell_pl2
    ))
    ax2.plot()

    print(time.time()-start)

    plt.show()


"""
===================================================================================================================
"""


def plot_compare_nets(nets_file_name1, nets_file_name2, net_name):
    """
    @gk
    This function takes as input 2 benchmarks' pl files and
    one common net and it plots it. The difference is not clearly visible
    but the net of the second file in only bold-outlined while the first file's
    net is in blue color without outline.
    :param nets_file_name1:
    :param nets_file_name2:
    :param net_name:
    :return:
    """

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import warnings
    import matplotlib.cbook
    warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

    net1 = {}
    net2 = {}
    net_name_number = int(net_name.replace('n', ''))
    nodes_in_net_num = 0
    node_names = []
    data = []
    pos = 0
    counter = -1

    with open(nets_file_name1) as nf:
        for num, line in enumerate(nf):
            if "NetDegree" in line:
                counter += 1
                if counter == net_name_number:
                    pos = num + 1
                    data = line.split()
                    nodes_in_net_num = data[2]

    with open(nets_file_name1) as nf:
        for num, line in enumerate(nf):
            if pos <= num < pos + int(nodes_in_net_num):
                data = line.split()
                node_names.append(data[0])

    data.clear()
    with open(nets_file_name1.replace('nets', 'pl')) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net1[i] = [j[1]]
                net1[i].append(j[2])

    data.clear()
    with open(nets_file_name1.replace('nets', 'nodes')) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n' \
                    or 'NumNodes' in line or 'NumTerminals' in line:
                continue
            else:
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net1[i].append(j[1])
                net1[i].append(j[2])

    data.clear()
    node_names.clear()

    with open(nets_file_name2) as nf:
        for num, line in enumerate(nf):
            if "NetDegree" in line:
                counter += 1
                if counter == net_name_number:
                    pos = num + 1
                    data = line.split()
                    nodes_in_net_num = data[2]

    with open(nets_file_name2) as nf:
        for num, line in enumerate(nf):
            if pos <= num < pos + int(nodes_in_net_num):
                data = line.split()
                node_names.append(data[0])

    data.clear()
    with open(nets_file_name2.replace('nets', 'pl')) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net2[i] = [j[1]]
                net2[i].append(j[2])

    data.clear()
    with open(nets_file_name2.replace('nets', 'nodes')) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n' \
                    or 'NumNodes' in line or 'NumTerminals' in line:
                continue
            else:
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net2[i].append(j[1])
                net2[i].append(j[2])

    fig = plt.figure(num=net_name)
    for n in net1.items():
        ax1 = fig.add_subplot(111, aspect='equal', adjustable='datalim')
        ax1.add_patch(patches.Rectangle(
            (float(n[1][0]), float(n[1][1])),
            float(n[1][2]),
            float(n[1][3]),
            facecolor='blue'
        ))
        ax1.plot()
    for n in net2.items():
        ax2 = fig.add_subplot(111, aspect='equal', adjustable='datalim')
        ax2.add_patch(patches.Rectangle(
            (float(n[1][0]), float(n[1][1])),
            float(n[1][2]),
            float(n[1][3]),
            fill=False
        ))
        ax2.plot()

    plt.show()


"""
====================================================================================================================
"""


def plot_net(net_file, net_name):
    """
    @gk
    This function takes as input a benchmark's nets file and the name of a net
    and it plots the nodes of the net in the same figure plot.
    Note that usually some nodes-cells are overlapping !
    :param net_file:
    :param net_name:
    :return:
    """

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import warnings
    import matplotlib.cbook
    warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

    pl_file = net_file.replace('.nets', '.pl')
    net = {}
    net_name_number = int(net_name.replace('n', ''))
    nodes_in_net_num = 0
    node_names = []
    data = []
    pos = 0
    counter = -1

    with open(net_file) as nf:
        for num, line in enumerate(nf, 0):
            if "NetDegree" in line:
                counter += 1
                if counter == net_name_number:
                    pos = num + 1
                    data = line.split()
                    nodes_in_net_num = data[2]

    with open(net_file) as nf:
        for num, line in enumerate(nf, 0):
            if pos <= num < pos + int(nodes_in_net_num):
                data = line.split()
                node_names.append(data[0])

    data.clear()
    with open(pl_file) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net[i] = [j[1]]
                net[i].append(j[2])

    data.clear()
    nodes_file = net_file.replace('.nets', '.nodes')
    with open(nodes_file) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n' \
                    or 'NumNodes' in line or 'NumTerminals' in line:
                continue
            else:
                data.append(line.split())

    for i in node_names:
        for j in data:
            if i == j[0]:
                net[i].append(j[1])
                net[i].append(j[2])

    fig = plt.figure(num=net_name)
    for n in net.items():
        ax = fig.add_subplot(111, aspect='equal', adjustable='datalim')
        ax.add_patch(patches.Rectangle(
            (float(n[1][0]), float(n[1][1])),
            float(n[1][2]),
            float(n[1][3]),
            fill=False
        ))
        ax.plot()
    plt.show()


"""
====================================================================================================================
"""


def plot_nets(nets_file_name, net_names):
    """
    @gk
    This function takes as input a benchmark's net file,
    and a list of net names and plots each net , with a random
    filling pattern.
    :param nets_file_name:
    :param net_names:
    :return:
    """

    from random import randint
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import warnings
    import matplotlib.cbook
    warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

    net_names_number = []
    nets_to_plot = []

    for i in net_names:
        net_names_number.append(int(i.replace('n', '')))

    for number in range(len(net_names_number)):
        nodes_in_net_num = 0
        node_names = []
        data = []
        pos = 0
        counter = -1
        net = {}
        with open(nets_file_name) as nf:
            for num, line in enumerate(nf, 0):
                if "NetDegree" in line:
                    counter += 1
                    if counter == net_names_number[number]:
                        pos = num
                        data = line.split()
                        nodes_in_net_num = data[2]

        with open(nets_file_name) as nf:
            for num, line in enumerate(nf, 0):
                if pos < num <= pos + int(nodes_in_net_num):
                    data = line.split()
                    node_names.append(data[0])

        data.clear()
        with open(nets_file_name.replace('nets', 'pl')) as p:
            for num, line in enumerate(p):
                if num == 0 or '#' in line or line == '\n':
                    continue
                else:
                    data.append(line.split())

        for i in node_names:
            for j in data:
                if i == j[0]:
                    net[i] = [j[1]]
                    net[i].append(j[2])

        data.clear()
        with open(nets_file_name.replace('nets', 'nodes')) as n:
            for num, line in enumerate(n):
                if num == 0 or '#' in line or line == '\n' \
                        or 'NumNodes' in line or 'NumTerminals' in line:
                    continue
                else:
                    data.append(line.split())

        for i in node_names:
            for j in data:
                if i == j[0]:
                    net[i].append(j[1])
                    net[i].append(j[2])

        nets_to_plot.append(net)

    colors = ['red', 'blue', 'green', 'black', 'gold', 'yellow', 'brown', 'purple', 'pink', 'crimson']
    fig = plt.figure(num=nets_file_name)
    for n in nets_to_plot:
        for k in n.items():
            print(k)
            ax = fig.add_subplot(111, aspect='equal', adjustable='datalim')
            ax.add_patch(patches.Rectangle(
                (float(k[1][0]), float(k[1][1])),
                float(k[1][2]),
                float(k[1][3]),
                facecolor=colors[randint(0, 9)]
            ))
            ax.plot()
    plt.show()


"""
====================================================================================================================
"""


def plot_placed_design(pl_file_name):

    """
    @gk
    This function takes as input a benchmarks pl file
    and plots the whole benchmark.
    :param pl_file_name:
    :return:
    """

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import warnings
    import matplotlib.cbook
    warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

    data = []
    cells = {}
    lines = {}
    line_number = ly = uy = lx = rx = sitesp = 0

    with open(pl_file_name) as p:
        for num, line in enumerate(p):
            if num == 0 or '#' in line or line == '\n':
                continue
            else:
                data = line.split()
                cells[data[0]] = [float(data[1])]
                cells[data[0]].append(float(data[2]))

    with open(pl_file_name.replace('pl', 'nodes')) as n:
        for num, line in enumerate(n):
            if num == 0 or '#' in line or line == '\n'\
                        or 'NumNodes' in line or 'NumTerminals' in line:
                continue
            else:
                data = line.split()
                cells[data[0]].append(float(data[1]))
                cells[data[0]].append(float(data[2]))

    with open(pl_file_name.replace('pl', 'scl')) as s:
        for num, line in enumerate(s):
            if num == 0 or '#' in line or line == '\n' or 'NumRows' in line:
                continue
            else:
                if 'CoreRow' in line:
                    line_number += 1
                if 'Coordinate' in line:
                    data = line.split()
                    ly = float(data[2])
                    lines['line' + str(line_number)] = [ly]
                if 'Height' in line:
                    data = line.split()
                    uy = float(data[2])
                    lines['line' + str(line_number)].append(uy)
                if 'Sitespacing' in line:
                    data = line.split()
                    sitesp = float(data[2])
                if 'SubrowOrigin' in line:
                    data = line.split()
                    lx = float(data[2])
                    rx = float(data[5]) * sitesp
                    lines['line' + str(line_number)].append(lx)
                    lines['line' + str(line_number)].append(rx)

    fig = plt.figure(num=pl_file_name.replace('.pl', ''))
    for l in lines.items():
        ax1 = fig.add_subplot(111, aspect='equal', adjustable='datalim')
        ax1.add_patch(patches.Rectangle(
            (l[1][2], l[1][0]),
            l[1][3],
            l[1][1],
            fill=False
        ))
        ax1.plot()

    for c in cells.items():
        ax2 = fig.add_subplot(111, aspect='equal', adjustable='datalim')
        ax2.add_patch(patches.Rectangle(
            (c[1][0], c[1][1]),
            c[1][2],
            c[1][3],
            fill=False
        ))
        ax2.plot()

    plt.show()


"""
===================================================================================================================
"""
