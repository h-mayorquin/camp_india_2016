from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
sns.set(font_scale=2.0)
sns.set_style('whitegrid')

data_before = np.load('block_before.npy')
data_after = np.load('block_after.npy')

x = data_before[0]
y = data_after[0]

gs = gridspec.GridSpec(3, 3)
fig = plt.figure(figsize=(16, 12))
fig.suptitle('Ventral vs Dorsal prediction before and after training')

for x in range(3):
    score_before = data_before[x]
    score_after = data_after[x]
    ax0 = fig.add_subplot(gs[x, 0])
    ax0.bar([1], [score_before], align='center', label='before')
    ax0.bar([2], [score_after], color='r', align='center', label='after')
    ax0.legend()
    ax0.set_ylim([0, 1])
    ax0.set_xlim([-0.1, 3.1])

    ax0.xaxis.set_visible(False)

    for y in range(1,3):
        score_before = data_before[x + 3 * y]
        score_after = data_after[x + 3 * y]
        ax = fig.add_subplot(gs[x, y], sharey=ax0)
        ax.bar([1], [score_before], align='center', label='before')
        ax.bar([2], [score_after], color='r', align='center', label='after')
        ax.legend()
        ax.set_ylim([0, 1])
        ax.set_xlim([-0.1, 3.1])

        # Remove axis
        ax.xaxis.set_visible(False)
        # if(y > 0):
        # ax.yaxis.set_visible(False)


plt.show()