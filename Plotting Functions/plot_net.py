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
