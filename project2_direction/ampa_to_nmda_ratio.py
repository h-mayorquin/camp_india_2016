import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(font_scale=2.0)
# This imports all the file names
data_location = './data/an_ratio/'
filenames = os.listdir('./data/an_ratio/')

# Get the times
# Time parameters

fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
ax.hold(True)

file_name = filenames[0]
for file_name in filenames:
    parameters = file_name.split('_')
    if np.abs(float(parameters[2]) - 5.0) < 0.1:
        print(file_name)
        data = np.genfromtxt(data_location + file_name, dtype='float')
        t_start = 0
        t_end = 200.0
        time = np.linspace(t_start, t_end, data.size)
        ax.plot(time, data, label=parameters[1])
        ax.legend()

fig.show()

