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
