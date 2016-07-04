from __future__ import print_function

def view_trial(trials, trial_N):
    """
    Prints all the details from a given trial
    :param trial: a trial from the database
    :return: None
    """
    type_of_data_to_index = {'Time of Cue': 0, 'Time of Sample': 1, 'trialnum': 2, 'spiketrain': 3, 'IsMatch': 4,
                             'fix': 5,
                             'cuerate': 6, 'cuedelay:': 7, 'samplerate': 8, 'sampledelay': 9, 'Time of Reward': 10}

    print('---------------------------------')
    print('Trial Number', trial_N)
    trial = trials[trial_N]

    for key, value in type_of_data_to_index.items():
        if key not in ['spiketrain']:
            print(key, trial[value][0][0])
        else:
            print(key, trial[value])

