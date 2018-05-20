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
