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
