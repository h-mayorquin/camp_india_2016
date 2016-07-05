from __future__ import print_function

type_of_data_to_index = {'Time of Cue': 0, 'Time of Sample': 1, 'trialnum': 2, 'spiketrain': 3, 'IsMatch': 4,
                         'fix': 5,
                         'cuerate': 6, 'cuedelay:': 7, 'samplerate': 8, 'sampledelay': 9, 'Time of Reward': 10}


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




