# Description: This file contains the color parser for the project

colors_dic = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    # primary colors
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    # secondary colors
    'yellow': (255, 255, 0),
    'magenta': (255, 0, 255),
    'cyan': (0, 255, 255),
    # tertiary colors
    'orange': (255, 165, 0),
    'purple': (128, 0, 128),
    'brown': (165, 42, 42),
}

base_colors = ["white", "black"]
primary_colors = ["red", "green", "blue"]
secondary_colors = ["yellow", "magenta", "cyan"]
tertiary_colors = ["orange", "purple", "brown"]
all_colors = primary_colors + secondary_colors + tertiary_colors

colors = {
    "base": base_colors,
    "primary":  primary_colors,
    "secondary": secondary_colors,
    "tertiary": tertiary_colors,
    "all": all_colors
}


def rgb2hex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])


def color2hex(color):
    if (isinstance(color, str)):
        color = colors_dic[color]
    return rgb2hex(color)
