import matplotlib.pyplot as plt
import numpy as np


def plot_bar_from_counter(counter, ax=None):
    """"
    This function creates a bar plot from a counter.

    :param counter: This is a counter object, a dictionary with the item as the key
     and the frequency as the value
    :param ax: an axis of matplotlib
    :return: the axis wit the object in it for further formating if necessary
    """

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    frequencies = counter.values()
    names = counter.keys()

    # Get the histogram
    x_coordinates = np.arange(len(counter))
    ax.bar(x_coordinates, frequencies, align='center')

    # Format the graph
    ax.xaxis.set_major_locator(plt.FixedLocator(x_coordinates))
    ax.xaxis.set_major_formatter(plt.FixedFormatter(names))
    ax.set_ylim([0, 1.1 * max(frequencies)])

    return ax
