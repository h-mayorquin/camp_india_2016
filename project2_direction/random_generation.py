from __future__ import print_function
import numpy as np
import seaborn as sns
import csv
import matplotlib.pyplot as plt
sns.set(font_scale=2.0)


sequence_length = 9
sorted_array = np.arange(sequence_length)

N_sequences = 10
sequences = np.zeros((N_sequences + 1, sequence_length))

for i in range(N_sequences):
    sequences[i + 1, :] = np.random.choice(sorted_array, size=sequence_length, replace=False)

# The frist element of the sequences is the shorted array
sequences[0, :] = sorted_array

# Transform to int
sequences = sequences.astype(int)
distances = np.linalg.norm(sequences - sorted_array, axis=1)


# plt.hist(distances, bins=50, normed=True)
# plt.show()

# Save the sequences
filename_sequences = './random_sequences.dat'
file_to_write = open(filename_sequences, 'w')
writer = csv.writer(file_to_write, delimiter=' ')
writer.writerow(sequences.shape)

for sequence in sequences:
    writer.writerow(sequence)

file_to_write.close()

# Save the distances
filename_distances = './distances.dat'
file_to_write = open(filename_distances, 'w')
writer = csv.writer(file_to_write, delimiter=' ')
writer.writerows(distances[:, np.newaxis])

file_to_write.close()