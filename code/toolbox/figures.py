import matplotlib.pyplot as plt

def set_dtu_colors():
    # Set a color palette
    # https://designguide.dtu.dk/colours/


    # DTU Corporate Red
    dtu_corporate_red = '#990000'
    # DTU Blue
    dtu_blue = '#2F3EEA'
    # DTU Bright Green
    dtu_bright_green = '#1FD082'
    # DTU Navy Blue
    dtu_navy_blue = '#030F4F'
    # DTU Yellow
    dtu_yellow = '#F6D04D'
    # DTU Orange
    dtu_orange = '#FC7634'
    # DTU Pink
    dtu_pink = '#F7BBB1'
    # DTU Grey
    dtu_grey = '#DADADA'
    # DTU Red
    dtu_red = '#E83F48'
    # DTU Green
    dtu_green = '#008835'
    # DTU Purple
    dtu_purple = '#79238E'

    # Create a dictionary with the colors
    dtu_colors = {
        'dtu_corporate_red': dtu_corporate_red,
        'dtu_blue': dtu_blue,
        'dtu_bright_green': dtu_bright_green,
        'dtu_navy_blue': dtu_navy_blue,
        'dtu_yellow': dtu_yellow,
        'dtu_orange': dtu_orange,
        'dtu_pink': dtu_pink,
        'dtu_grey': dtu_grey,
        'dtu_red': dtu_red,
        'dtu_green': dtu_green,
        'dtu_purple': dtu_purple,
    }
    return dtu_colors


def figure_params(
        title = 'Example title',
        xlabel = 'Example x label',
        ylabel = 'Example y label',
        x_units = 'X',
        y_units = 'Y',
        legend = False,
        legend_loc = 'upper right',
        font_scale = 1,
        figsize = (20, 10),
        dpi = 100,
        grid = False,
        grid_style = '-',
        grid_color = 'gray',

        # Line params
        linewidth = 2,
        linestyle = '-',
        marker = 'o',
        markersize = 10,
):
    # Set figure size
    plt.figure(figsize=figsize, dpi=dpi)

    # Set font scale
    plt.rcParams.update({'font.size': 22*font_scale})

    font = {
        'family': 'Arial',
        'weight': 'bold',
        'size': 22*font_scale
    }
    # use LaTeX fonts in the plot
    plt.rc('text', usetex=True)
    plt.rc('font', **font)

    # Set grid
    if grid == True:
        plt.grid(color=grid_color, linestyle=grid_style)

    # Set legend
    if legend == True:
        plt.legend(loc=legend_loc)

    # Set title
    plt.title(r'\textbf{' + title + '}', fontsize=30*font_scale)

    # Set labels
    plt.xlabel(r'\textbf{' + xlabel + '} [' + x_units + ']', fontsize=22*font_scale)
    plt.ylabel(r'\textbf{' + ylabel + '} [' + y_units + ']', fontsize=22*font_scale)

    # Set line params
    plt.setp(plt.gca().get_lines(), linewidth=linewidth, linestyle=linestyle, marker=marker, markersize=markersize)

    return plt

def figure_save(
        plt = plt,
        filename = 'example',
        save = False,
        save_path = 'g:/My Drive/master thesis/figures/',
        save_format = 'png',
        save_dpi = 300,
        show = True,
):
    if save == True:
        plt.savefig(save_path + filename + '.' + save_format, dpi=save_dpi, format=save_format)
    if show == True:
        plt.show()
    plt.close()

import matplotlib.pyplot as plt

def set_matplotlib_style():
    # Set general figure parameters
    plt.rcParams['figure.figsize'] = (10, 8)  # Figure size in inches
    plt.rcParams['figure.dpi'] = 300  # DPI resolution of the figure
    plt.rcParams['axes.grid'] = True  # Show grid lines in plots
    plt.rcParams['axes.linewidth'] = 0.5  # Line width of axes borders

    # Set font parameters globally
    plt.rcParams['font.family'] = 'Source Sans Pro'  # Font family
    plt.rcParams['font.weight'] = 'normal'  # Font weight
    plt.rcParams['font.size'] = 12  # Font size for labels and titles

    # Set weight for being bold for titles only
    plt.rcParams['axes.titleweight'] = 'bold'  # Font weight for title only
    # Bold figure title
    plt.rcParams['figure.titleweight'] = 'bold'  # Font weight for figure title
    # Set title size
    plt.rcParams['figure.titlesize'] = 22  # Font size for title only
    # Set axes label weight to bold
    plt.rcParams['axes.titlesize'] = 18  # Font weight for axes labels
    plt.rcParams['axes.labelweight'] = 'bold'  # Font weight for axes labels


    # Set line and marker parameters
    plt.rcParams['lines.linewidth'] = 1.5  # Line width
    plt.rcParams['lines.markersize'] = 6  # Marker size

    # Set color parameters
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=set_dtu_colors().values())  # Set color cycle

    # Set legend parameters
    plt.rcParams['legend.frameon'] = False  # Whether to show frame around legend
    plt.rcParams['legend.loc'] = 'best'  # Location of the legend

    # Set grid parameters
    plt.rcParams['grid.color'] = set_dtu_colors()['dtu_grey']  # Grid color light dark blue
    plt.rcParams['grid.linestyle'] = '--'  # Grid line style
    plt.rcParams['grid.linewidth'] = 0.5  # Grid line width
    plt.rcParams['axes.axisbelow'] = True  # Place grid lines behind the plot


    # Set savefig parameters
    plt.rcParams['savefig.dpi'] = 300  # DPI resolution for saving figures
    plt.rcParams['savefig.transparent'] = True  # Save figures with transparent background

def set_dtu_colors():
    # Set a color palette
    # https://designguide.dtu.dk/colours/


    # DTU Corporate Red
    dtu_corporate_red = '#990000'
    # DTU Blue
    dtu_blue = '#2F3EEA'
    # DTU Bright Green
    dtu_bright_green = '#1FD082'
    # DTU Navy Blue
    dtu_navy_blue = '#030F4F'
    # DTU Yellow
    dtu_yellow = '#F6D04D'
    # DTU Orange
    dtu_orange = '#FC7634'
    # DTU Pink
    dtu_pink = '#F7BBB1'
    # DTU Grey
    dtu_grey = '#DADADA'
    # DTU Red
    dtu_red = '#E83F48'
    # DTU Green
    dtu_green = '#008835'
    # DTU Purple
    dtu_purple = '#79238E'

    # Create a dictionary with the colors
    dtu_colors = {
        'dtu_corporate_red': dtu_corporate_red,
        'dtu_blue': dtu_blue,
        'dtu_bright_green': dtu_bright_green,
        'dtu_navy_blue': dtu_navy_blue,
        'dtu_yellow': dtu_yellow,
        'dtu_orange': dtu_orange,
        'dtu_pink': dtu_pink,
        'dtu_grey': dtu_grey,
        'dtu_red': dtu_red,
        'dtu_green': dtu_green,
        'dtu_purple': dtu_purple,
    }
    return dtu_colors



