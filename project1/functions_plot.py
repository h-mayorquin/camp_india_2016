import numpy as np
import matplotlib.pyplot as plt
from functions_extract_database import get_spike_train_from_trial
import seaborn as sns

sns.set(font_scale=2.0)


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
