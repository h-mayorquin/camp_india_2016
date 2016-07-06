from __future__ import print_function
import openpyxl
import scipy.io as sio
import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt

from functions_extract_database import get_rates_from_trials

folder = './database/'
filename = 'SummaryDatabase'
format_type = '.xlsx'

# Extract all the data files names from excel
wb = openpyxl.load_workbook(folder + filename + format_type)
pre_spatial_set = wb.get_sheet_by_name('Pre_SpatialSet')
# pre_spatial_set = wb.get_sheet_by_name('Post_SpatialSet')

file_names = []
for file_name, neuron in zip(pre_spatial_set.columns[0], pre_spatial_set.columns[1]):
    open_string = file_name.value + '_' + str(neuron.value)
    file_names.append(open_string)

number_of_files = len(file_names)

# Get the data in the sklearn matrix format
block_N = 0
folder = './data/'
format_type = '.mat'
number_of_blocks = 9
block_score = np.zeros(number_of_blocks)

for block_N in range(number_of_blocks):

    rates_list = []

    for file_index, file_name in enumerate(file_names[1:]):
        aux = folder + file_name + format_type
        data_base = sio.loadmat(aux)

        # Get the rates
        data = data_base['MatData']
        blocks = data[0][0][0]
        trials = blocks[:, block_N][0][0][0]
        number_of_trials = trials.size
        rates = get_rates_from_trials(trials)

        rates_list.append(rates.mean(axis=0))

    # This will be the training examples
    X = np.stack(rates_list, axis=0)
    X = X[:, :4]
    # Now we will get the labels
    y = []
    for area in pre_spatial_set.columns[4]:
        y.append(area.value)

    y = np.array(y)[1:]

    # Now the machine learning

    from sklearn.cross_validation import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    clf = linear_model.LogisticRegression()
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    block_score[block_N] = score

    print(block_N, score)


np.save('block_before', block_score)

