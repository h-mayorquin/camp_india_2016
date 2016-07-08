import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=2.0)

file_to_read_from = './tempV.dat'

data = np.genfromtxt(fname = file_to_read_from, dtype ='float')

number_of_points, number_of_plots = data.shape

# Time parameters
t_start = 0
t_end = 200.0
time = np.linspace(t_start, t_end, number_of_points)


# Plot parameters
y_lim = [-80, -60]

fig = plt.figure(figsize=(16, 12))

ax1 = fig.add_subplot(121)

for i in range(number_of_plots / 2):
    ax1.plot(time, data[:,i])
    ax1.hold(True)
    ax1.set_ylim(y_lim)
    ax1.set_ylabel('Volatge (mV)')
    ax1.set_xlabel('Time (ms)')

ax1.set_title('Voltage traces for the IN sequence')

# ax.legend()

ax2 = fig.add_subplot(122, sharey=ax1)

for i in range(number_of_plots / 2, number_of_plots):

    ax2.plot(time, data[:,i])
    ax2.hold(True)
    ax2.set_ylim(y_lim)
    #ax2.set_ylabel('Volatge (mV)')
    ax2.set_xlabel('Time (ms)')

ax2.set_title('Voltage traces for the OUT sequence')
plt.setp(ax2.get_yticklabels(), visible=False)
# ax.legend()


plt.show()

