def check_non_terminal(nodes_file, node):
    """
    @gk
    Function takes as input the file's name and the node's name.
    It pinpoints the line of the node. Then searches for the string
    terminal. It returns True if there is no terminal string after
    the name of the node.
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
                        return False

    return True
