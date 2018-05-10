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

