from __future__ import print_function
import scipy.io as sio

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import numpy as np

from functions_plot import plot_raster_from_trials, plot_spike_raster_grid
from functions_plot import plot_psth_grid, plot_psth_from_trials
from functions_extract_database import view_trial, get_spike_train_from_trial, get_rates_from_trial, get_rates_from_trials


folder = "./data/"
data_base_name = 'ADR011_1_3071'
format = '.mat'
data_base = sio.loadmat(folder + data_base_name + format)

monkeys = {1: 'ADR', 2: 'BEN', 3: 'ELV', 4: 'SCR'}

data = data_base['MatData']

# 8 or 9 blocks of 12 trials each
blocks = data[0][0][0]
number_of_blocks = blocks.size
print('This should be 8 or 9', number_of_blocks)

# Which of all the blocks you chose
block_N = 0

trials = blocks[:, block_N][0][0][0]
number_of_trials = trials.size
# number_of_trials = trials.size

# Which of all the trials
trial_N = 0

print('This should be 12', number_of_trials)

block_to_grid_map = {1: (1, 2), 2: (0, 2), 3:(0, 1), 4: (0, 0), 5: (1, 0),
                     6: (2, 0), 7: (2, 1), 8: (2, 2), 9: (1, 1)}

# Here we can plot the raster
fig = plot_psth_grid(blocks, block_to_grid_map)
# fig = plot_spike_raster_grid(blocks, block_to_grid_map)
plt.show(fig)

# Get the trial data
view_trial(trials, trial_N)

rates1 = get_rates_from_trial(trials, trial_N)
print(rates1)

rates = get_rates_from_trials(trials)
print(trials.shape)
print(rates)