from __future__ import print_function
import scipy.io as sio

import matplotlib.pyplot as plt
import numpy as np

from functions_plot import plot_raster_from_trials

from functions_extract_database import view_trial, get_spike_train_from_trial


folder = "./data/"
data_base_name = 'ADR001_1_3000'
format = '.mat'
data_base = sio.loadmat(folder + data_base_name + format)

monkeys = {1: 'ADR', 2: 'BEN', 3: 'ELV', 4: 'SCR'}

data = data_base['MatData']

# 8 or 9 blocks of 12 trials each
blocks = data[0][0][0]
print('This should be 8 or 9', blocks.shape)
number_of_blocks = 
# Which of all the blocks you chose
block_N = 6

trials = blocks[:, block_N][0][0][0]
numbers_of_trials = trials.size

print('This should be 12', numbers_of_trials)


ax = plot_raster_from_trials(trials)
plt.show()




