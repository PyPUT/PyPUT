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

    plt.show()
