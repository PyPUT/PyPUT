import re
import matplotlib.patches as patches
import matplotlib.pyplot as plt

def plot_chip_macros_only(file_name):
    '''
    @gt
    this function takes a benchmark as a parameter
    plots all macros of the chip
    :param file_name: str
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

plot_chip_macros_only("ibm01")