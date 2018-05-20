import re
import matplotlib.patches as patches
import matplotlib.pyplot as plt

def plot_area_macros_only(file_name, xs, xf, ys, yf):
    '''
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
    '''

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
                        if xs <= int(line.split()[1]) and nodes[line.split()[0]][0] + int(line.split()[1]) <= xf and ys <= int(line.split()[2]) and nodes[line.split()[0]][1] + int(line.split()[2]) <= yf:
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