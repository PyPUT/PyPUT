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
