import matplotlib.patches as patches
import matplotlib.pyplot as plt

def plot_density_map_area(file_name, xs, ys, xf, yf, divider):

    '''
    @gt
    this function takes in as a parameter a benchmark, a number x
    and four (4) coordinates (starting and finishing x and y)
    divides these coordinates of the chip in x*x parts and plots the density of each part
    green being 25% or less, red being 76% or more
    :param file_name: str
    :param xs: int
    :param xf: int
    :param ys: int
    :param yf: int
    :param divider: int
    :return
    '''

    rows = []
    max_width = 0
    bins = []

    with open(file_name + ".scl") as f:
        for i, line in enumerate(f):
                    
            line = line.strip()
            if line:
                if line.split()[0] == "Coordinate":
                    starting_height = line.split()[2]
                if line.split()[0] == "Height":
                    ending_height = int(starting_height) + int(line.split()[2])
                    line_height = line.split()[2]
                if line.split()[0] == "Sitespacing":
                    sitespacing = line.split()[2]
                if line.split()[0] == "SubrowOrigin":
                    starting_x = line.split()[2]
                    ending_x = int(starting_x) + int(sitespacing) * int(line.split()[5])
                    if ending_x > max_width:
                        max_width = ending_x
                    rows.append([starting_x,starting_height,ending_x,ending_height])

    max_height = rows[-1][3]

    step_x = int((xf-xs) / divider)+1
    step_y = int((yf-ys) / divider)+1

    for i in range(ys, yf, step_y):
        for j in range(xs, xf, step_x):
            start_x = j
            start_y = i
            end_x   = j+step_x
            end_y   = i+step_y

            bins.append([start_x, start_y, end_x, end_y])

    fig1 = plt.figure()

    for area in bins:

        percentage = density_in_coordinates(file_name + ".pl", area[1], area[0], area[3], area[2])

        if percentage <= 0.25:
            facecolor = "green"
        elif percentage <= 0.5:
            facecolor = "yellow"
        elif percentage <= 0.75:
            facecolor = "orange"
        else:
            facecolor = "red"

        ax1 = fig1.add_subplot(111)
        ax1.add_patch(
            patches.Rectangle(
            (area[0], area[1]),
            area[2]-area[0],
            area[3]-area[1],

            facecolor=facecolor, edgecolor="black", linewidth=0.5, linestyle='solid'
            )
        )
        ax1.plot()
    plt.show()