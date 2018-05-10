import re

def check_net(file_name, search_net):
    '''
    @gt
    this function takes in as a parameter a benchmark and a net
    returns a tuple
    1st index has its terminal nodes
    2nd its non terminal
    :param file_name: str
    :param search_net: str
    :return net_info: tupple(list[str, str,..., str], list[str, str,..., str])
    '''
    nets = {}
    nodes = {}
    counter = 0
    terminals = []
    non_terminals = []

    with open(file_name + ".nets") as f:
        for i, line in enumerate(f):
                                                                
            line = line.strip()
            if line:
                if "NetDegree" in line:
                    num_of_nodes = int(line.split()[2])
                    net_name = "n"+str(counter)
                    counter += 1
                    if net_name == search_net:
                        nets[net_name] = []
                elif re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if net_name in nets:
                        nets[net_name].append(line.split()[0])

    for value in nets.values():
        for element in value:
            if element not in nodes.keys():
                nodes[element] = []

    with open(file_name + ".nodes") as f:
        for i, line in enumerate(f):
                                                                    
            line = line.strip()
            if line:
                if re.match(r'[a-z]{1}[0-9]+', line.split()[0]):
                    if line.split()[0] in nodes.keys():
                        if len(line.split()) == 3:
                            non_terminals.append(line.split()[0])
                        else:
                            terminals.append(line.split()[0])
                                                            
    
    net_info = (terminals, non_terminals)
    return net_info