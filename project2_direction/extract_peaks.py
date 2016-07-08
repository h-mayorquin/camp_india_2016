import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=2.0)

file_to_read_from = './tempM.dat'

data = np.genfromtxt(fname = file_to_read_from, dtype ='float')
time = np.genfromtxt(fname='./time.dat', dtype='float')

nuber_of_time_intervals, number_of_sequences = data.shape

# Input velocity
input_velocity = np.arange(0, int(time), 1).astype(int)


# Plot
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)

ax.plot(input_velocity, data[:, 0], 'o-', markersize=20, label='in')
ax.plot(input_velocity, data[:, 1], 'o-', markersize=20, label='out')
ax.fill_between(input_velocity, data[:, 0], data[:, 1], alpha=0.5, label='difference')

ax.legend()
ax.set_title('Peak EPSP at Soma at different interval times')
ax.set_ylabel('Peak EPSP (mV)')
ax.set_ylim([0, 15])
ax.set_xlabel('Input velocity')
ax.legend()
plt.show()

