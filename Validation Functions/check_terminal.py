def check_terminal(nodes_file, node):
    """
    @gk
    Function takes as input the file's name and the node's name.
    Pinpoints the line of the node name , returns true if the string
    terminal is in the same line.
    :param nodes_file:
    :param node:
    :return:
    """

    data = []
    with open(nodes_file) as f:
        for num, line in enumerate(f):
            if node in line:
                data = line.split()
                if node == data[0]:
                    if "terminal" in line:
                        return True

    return False
