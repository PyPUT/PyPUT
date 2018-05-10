import re

def check_move_hpwl(file_name, node, x, y):
    '''
    @gt
    this function takes in as a parameter a benchmark, a node
    and 2 coordinates x and y
    returns supposed hpwl if that node was moved to these coordinates 
    :param file_name: str
    :param node: str
    :param x: int
    :param y: int
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
                    nodes[line.split()[0]].append(line.split()[1])
                    nodes[line.split()[0]].append(line.split()[2])

    nodes[node][2] = x
    nodes[node][3] = y                        

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
    
    return(hpwl)