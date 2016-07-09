from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import csv
sns.set(font_scale=2.0)

# Load the distances
distances_file = './distances.dat'
distances = np.genfromtxt(fname=distances_file, dtype ='float')

# Load the maximum EPSP
data_file = './tempM.dat'
data = np.genfromtxt(fname=data_file, dtype ='float')

max_epsp = data[3, :]

# Plot the figure
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
ax.plot(distances, data[4, :], 'o', label='4')
ax.plot(distances, data[3, :], 'o', label='3')
ax.plot(distances, data[2, :], 'o', label='2')
ax.plot(distances, data[1, :], 'o', label='1')
ax.plot(distances, data[0, :], 'o', label='0')

ax.set_xlabel('Distance to In sequence')
ax.set_ylabel('Max EPSP')
ax.set_ylim((7, 12))
ax.set_xlim((-1, 17))
ax.set_title('Random sequence analysis for different input speeds')

ax.legend()

plt.show()