from __future__ import print_function
import numpy as np

type_of_data_to_index = {'Time of Cue': 0, 'Time of Sample': 1, 'trialnum': 2, 'spiketrain': 3, 'IsMatch': 4,
                         'fix': 5,
                         'cuerate': 6, 'cuedelay': 7, 'samplerate': 8, 'sampledelay': 9, 'Time of Reward': 10}


code = [('Cue_onT', 'O'), ('Sample_onT', 'O'), ('trialnum', 'O'), ('TS', 'O'), ('IsMatch', 'O'), ('fix', 'O'), ('cuerate', 'O'),
 ('cuedelay', 'O'), ('samplerate', 'O'), ('sampledelay', 'O'), ('Reward_onT', 'O')]


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

    for key, value in type_of_data_to_index.items():
        if key not in ['spiketrain']:
            print(key, trial[value][0][0])
        else:
            print(key, trial[value])


def get_spike_train_from_trial(trial):
    """
    :param trial: a trial extracted from the database
    :return: the spike train
    """

    spikes = trial[type_of_data_to_index['spiketrain']]

    if len(spikes) > 0:
        return spikes[0]
    else:
        return []


def get_rates_for_trial(trials, trial_N):
    trial = trials[trial_N]
    keys_of_rates = ['cuerate', 'cuedelay', 'samplerate', 'sampledelay', 'IsMatch']

    rates = np.zeros(len(keys_of_rates))
    for index, key in enumerate(keys_of_rates):
        rates[index] = trial[type_of_data_to_index[key]]

    return rates


def get_rates_for_trials(trials):

    number_of_trials = trials.size

    rates = np.zeros((number_of_trials, 5))

    for trial_N in range(number_of_trials):
        trial = trials[trial_N]
        rates[trial_N, :] = get_rates_for_trial(trials, trial_N)

    return rates