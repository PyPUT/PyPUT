import re
import matplotlib.patches as patches
import matplotlib.pyplot as plt

def plot_overflows(file_name):

    '''
    @gt
    this function takes in as a parameter a benchmark
    finds and plots the overflowing, non-terminal nodes
    :param file_name: str
    :return
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