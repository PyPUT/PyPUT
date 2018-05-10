import re

def check_swap_cells_hpwl(file_name, node1, node2):
    '''
    @gt
    this function takes in as a parameter a benchmark and two (2) nodes
    returns supposed hpwl if these nodes were swapped
    :param file_name: str
    :param node1: str
    :param node2: str
    :return hpwl: int
    '''

    nodes = {}
    netsx = {}
    netsy = {}
    counter = 0
    hpwl = 0
    
    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
                                                                                                                                    
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] not in nodes:
                        nodes[line.split()[0]] = []
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])
    
    with open(file_name + ".pl") as f:
        for i, line in enumerate(f):
                                                                                    
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    nodes[line.split()[0]].append(int(line.split()[1]))
                    nodes[line.split()[0]].append(int(line.split()[2]))

    nodes[node1][2] += nodes[node2][2]
    nodes[node2][2] = nodes[node1][2] - nodes[node2][2]
    nodes[node1][2] = nodes[node1][2] - nodes[node2][2]                    

    nodes[node1][3] += nodes[node2][3]
    nodes[node2][3] = nodes[node1][3] - nodes[node2][3]
    nodes[node1][3] = nodes[node1][3] - nodes[node2][3] 

    with open(file_name + ".nets") as f:
            for i, line in enumerate(f):
    
                line = line.strip()
                    
                if line:
                    if "NetDegree" in line:
                        num_of_nodes = int(line.split()[2])
                        net_name = "n"+str(counter)
                        counter += 1
                        netsx[net_name] = []
                        netsy[net_name] = []
                    elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                        if net_name in netsx:
                            if len(netsx[net_name]) == 0:
                                netsx[net_name].append(int(nodes[line.split()[0]][2]))
                                netsx[net_name].append(int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]))

                                netsy[net_name].append(int(nodes[line.split()[0]][3]))
                                netsy[net_name].append(int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]))
                            else:
                                if int(nodes[line.split()[0]][2]) < netsx[net_name][0]:
                                    netsx[net_name][0] = int(nodes[line.split()[0]][2])
                                                                                                                
                                if int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0]) > netsx[net_name][1]:
                                        netsx[net_name][1] = int(nodes[line.split()[0]][2]) + int(nodes[line.split()[0]][0])
                                                                                                                        
                                if int(nodes[line.split()[0]][3]) < netsy[net_name][0]:
                                    netsy[net_name][0] = int(nodes[line.split()[0]][3])
                                                                                                                        
                                if int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1]) > netsy[net_name][1]:
                                    netsy[net_name][1] = int(nodes[line.split()[0]][3]) + int(nodes[line.split()[0]][1])

    for net in netsx:
        hpwl += float(netsx[net][1] - netsx[net][0] + netsy[net][1] - netsy[net][0])
    
    return hpwl