import re
import matplotlib.patches as patches
import matplotlib.pyplot as plt

def plot_overlaps(file_name):

    '''
    @gt
    this function takes in a benchmark as a parameter
    plots all the non-terminal nodes that overlap
    :param file_name: str
    :return
    '''

    place = {}
    size = {}
    sap = {}
    overlapping = []
    active_list = []
    max_width = 0

    
    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):
                    
            line = line.strip()
            if line:
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = line.split()[2]
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    if ending_x > max_width:
                        max_width = ending_x
                    
    divider = max_width // 10
    
    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
                                                                                                              
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if len(line.split()) == 3:
                        size[line.split()[0]] = [line.split()[1], line.split()[2]]

    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):
                                                                                                              
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in size:
                        place[line.split()[0]] = [line.split()[1], line.split()[2]]
                        sap_num = int(line.split()[1]) // divider
                        if sap_num not in sap.keys():
                            sap[sap_num] = []
                        sap[sap_num].append([line.split()[0], int(line.split()[1]), int(line.split()[1]) + int(size[line.split()[0]][0]), int(line.split()[2]), "start"])

                        sap[sap_num].append([line.split()[0], int(line.split()[1]), int(line.split()[1]) + int(size[line.split()[0]][0]), int(line.split()[2]) + int(size[line.split()[0]][1]), "end"])

    for lista in sap.values():
        lista.sort(key=lambda x: x[3])
        lista.sort(key=lambda x: x[4], reverse = True)
        for element in lista:
            if element[4] == "start":
                if len(active_list) == 0:
                    active_list.append(element[0])
                else:
                    for node in active_list:
                        if place[node][0] <= place[element[0]][0] + size[element[0]][0] and place[node][0] + size[node][0] >= place[element[0]][0] and place[node][1] <= place[element[0]][1] + size[element[0]][1] and place[node][1] + size[node][1] >= place[element[0]][1]:
                            if node not in overlapping:
                                overlapping.append(node)
                            if element[0] not in overlapping:
                                overlapping.append(element[0])
                    active_list.append(element[0])
            else:
                active_list.remove(element[0])                    

    fig1 = plt.figure()

    for node in overlapping:
        ax1 = fig1.add_subplot(111)
        ax1.add_patch(
	        patches.Rectangle(
	        (float(place[node][0]), float(place[node][1])),
	        float(size[node][0]),
	        float(size[node][1]),

	        facecolor="none", edgecolor="black", linewidth=0.5, linestyle='solid'
	        )
        )
        ax1.plot()
    plt.show()