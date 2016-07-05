import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from functions_extract_database import get_spike_train_from_trial
import seaborn as sns

sns.set(font_scale=2.0)
sns.set_style('white')


def plot_raster_from_trials(trials, ax=None):
    """
    :param trials: the spike trials
    :param ax: the axis, if None a new axes is created
    :return: ax, the axis
    """

    if ax is None:
        fig = plt.figure(figsize=(16, 12))
        fig.hold(True)
        ax = fig.add_subplot(111)

    numbers_of_trials = trials.size
    # We need to plot the raster plot
    for trial_N in range(numbers_of_trials):
        trial = trials[trial_N]
        spikes = get_spike_train_from_trial(trial)
        aux = np.ones(len(spikes)) * (trial_N + 1)
        ax.plot(spikes, aux, '*', color='black', markersize=20)

    ax.set_ylabel('Trial')
    ax.set_xlabel('Time (ms)')
    ax.set_ylim([0, numbers_of_trials + 1])

    return ax


def plot_spike_raster_grid(blocks, block_to_grid_map):
    fig = plt.figure(figsize=(16, 12))
    number_of_blocks = blocks.size
    gs = gridspec.GridSpec(3, 3)
    for block_N in range(number_of_blocks):
        trials = blocks[:, block_N][0][0][0]
        x, y = block_to_grid_map[block_N + 1]
        ax = fig.add_subplot(gs[x, y])
        ax = plot_raster_from_trials(trials, ax)

    return fig


def plot_psth_from_trials(trials, ax=None):
    """
    This function plots the peri-stimulus time histogram from a
    set of trials of spike trains
    :param trials: a collection of trials
    :param ax: an axis of matplotlib

    :return: the axis (matplotlib)
    """

    if ax is None:
        fig = plt.figure(figsize=(16, 12))
        fig.hold(True)
        ax = fig.add_subplot(111)

    numbers_of_trials = trials.size
    all_spikes = []
    # We need to plot the raster plot
    for trial_N in range(numbers_of_trials):
        trial = trials[trial_N]
        spikes = get_spike_train_from_trial(trial)
        all_spikes = np.concatenate((all_spikes, spikes))

    histogram_data = ax.hist(all_spikes, bins=10)

    ax.set_xlabel('Time (ms)')

    return ax, histogram_data

def plot_psth_grid(blocks block_to_grid_map):