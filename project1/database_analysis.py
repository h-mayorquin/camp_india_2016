from __future__ import print_function
import os
import matplotlib.pyplot as plt
from collections import Counter
import seaborn

from  functions_graph import plot_bar_from_counter

# This imports all the file names
filenames = os.listdir('./data/')

# We take out all the data from the filenames
monkey_names = []
sequential_stimulus = []
neurons_number = []
for filename in filenames:
    x = filename.split('_')
    name = x[0][0:3]
    sequential_stimulus.append(x[1])
    neurons_number.append(x[2].strip('.mat'))
    monkey_names.append(name.upper())

# Get the frequency of instance occurrences
monkey_hist = Counter(monkey_names)
sequential_stimulus_hist = Counter(sequential_stimulus)
neurons_number_hist = Counter(neurons_number)

# Plot what you need
# ax  = plot_bar_from_counter(sequential_stimulus_hist)
ax = plot_bar_from_counter(monkey_hist)
plt.suptitle('Experiment per monkey in the database')
plt.show()

print('number of files', len(filenames))