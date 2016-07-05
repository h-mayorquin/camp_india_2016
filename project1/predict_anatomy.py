from __future__ import print_function
import openpyxl
import scipy.io as sio
import numpy as np
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
number_of_trials = 12
X = np.zeros((number_of_files * number_of_trials, 5))
block_N = 0

folder = './data/'
format_type = '.mat'

for file_index, file_name in enumerate(file_names[1:]):
    aux = folder + file_name + format_type
    data_base = sio.loadmat(aux)

    # Get the rates
    data = data_base['MatData']
    blocks = data[0][0][0]
    trials = blocks[:, block_N][0][0][0]
    number_of_trials = trials.size
    print(trials.shape)
    print(file_index)
    rates = get_rates_from_trials(trials)
    X[file_index:file_index + number_of_trials, :] = rates
