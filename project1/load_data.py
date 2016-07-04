from __future__ import print_function
import scipy.io as sio

from functions_extract_database import view_trial


folder = "./data/"
data_base_name = 'ADR001_1_3000'
format = '.mat'
data_base = sio.loadmat(folder + data_base_name + format)

monkeys = {1: 'ADR', 2: 'BEN', 3: 'ELV', 4: 'SCR'}

data = data_base['MatData']

# 8 or 9 blocks of 12 trials each
blocks = data[0][0][0]
print('This should be 8 or 9', blocks.shape)

# Which of all the blocks you chose
block_N = 6

trials = blocks[:, block_N][0][0][0]
print('This should be 12', trials.shape)

# Which of the trials you chose
trial_N = 4
trial = trials[trial_N]

code = [('Cue_onT', 'O'), ('Sample_onT', 'O'), ('trialnum', 'O'), ('TS', 'O'), ('IsMatch', 'O'), ('fix', 'O'), ('cuerate', 'O'),
 ('cuedelay', 'O'), ('samplerate', 'O'), ('sampledelay', 'O'), ('Reward_onT', 'O')]

type_of_data_to_index = {'Time of Cue': 0, 'Time of Sample': 1, 'trialnum': 2, 'spiketrain': 3, 'IsMatch': 4, 'fix': 5,
                         'cuerate': 6, 'cuedelay:': 7, 'samplerate': 8, 'sampledelay': 9, 'Time of Reward': 10}


view_trial(trials, trial_N)