from __future__ import print_function
import numpy as np

#type_of_data_to_index = {'Time of Cue': 0, 'Time of Sample': 1, 'Time of Reward': 2, 'trialnum': 3, 'spiketrain': 4, 'IsMatch': 5,
#                         'fix': 6, 'cuerate': 7, 'cuedelay': 8, 'samplerate': 9, 'sampledelay': 10}

type_of_data_to_index_ = {'Time of Cue': 0, 'Time of Sample': 1, 'trialnum': 2, 'spiketrain': 3, 'IsMatch': 4,
                         'fix': 5, 'cuerate': 6, 'cuedelay': 7, 'samplerate': 8, 'sampledelay': 9, 'Time of Reward': 10}



code_post = [('Cue_onT', 'O'), ('Sample_onT', 'O'), ('trialnum', 'O'), ('TS', 'O'), ('IsMatch', 'O'), ('fix', 'O'), ('cuerate', 'O'),
 ('cuedelay', 'O'), ('samplerate', 'O'), ('sampledelay', 'O'), ('Reward_onT', 'O')]

code_pre =[('Cue_onT', 'O'), ('Sample_onT', 'O'), ('Reward_onT', 'O'), ('trialnum', 'O'), ('TS', 'O'), ('IsMatch', 'O'),
           ('fix', 'O'), ('cuerate', 'O'), ('cuedelay', 'O'), ('samplerate', 'O'), ('sampledelay', 'O')]


def build_entry_dictionary(trials):
    type_of_data_to_index = {}

    for index, key in enumerate(trials.dtype.names):
        type_of_data_to_index[key] = index

    return type_of_data_to_index


def view_trial(trials, trial_N):
    """
    Prints all the details from a given trial
    :param trials: a trial from the database
           trial_N: the number of trial that we are talking about.
    :return: None
    """

    print('---------------------------------')
    print('Trial Number', trial_N)
    trial = trials[trial_N]

    type_of_data_to_index = build_entry_dictionary(trials)

    for key, value in type_of_data_to_index.items():
        if key not in ['TS']:
            print(key, trial[value][0][0])
        else:
            print(key, trial[value])


def get_spike_train_from_trial(trials, trial_n):

    type_of_data_to_index = build_entry_dictionary(trials)

    trial = trials[trial_n]
    spikes = trial[type_of_data_to_index['TS']]

    if len(spikes) > 0:
        return spikes[0]
    else:
        return []


def get_rates_from_trial(trials, trial_n):

    trial = trials[trial_n]
    type_of_data_to_index = build_entry_dictionary(trials)
    keys_of_rates = ['cuerate', 'cuedelay', 'samplerate', 'sampledelay', 'IsMatch']

    rates = np.zeros(len(keys_of_rates))
    for index, key in enumerate(keys_of_rates):
        if trial[type_of_data_to_index[key]]:
            rates[index] = trial[type_of_data_to_index[key]]

    return rates


def get_rates_from_trials(trials):

    number_of_trials = trials.size

    rates = np.zeros((number_of_trials, 5))

    for trial_n in range(number_of_trials):
        rates[trial_n, :] = get_rates_from_trial(trials, trial_n)

    return rates