import os
import numpy as np
import scipy
import pandas as pd

directory = __file__
data_directory = os.path.dirname(directory)
participant = 10

if participant < 10:
    participant = "0" + str(participant)

fname = "subject_" + str(participant)+ ".mat"
# Get path for file
fpath = os.path.join(data_directory, fname)
# Col 1: Timestamps, Col 2-17: Electrode Recording, Col 18-19: Triggers for Condition 1 and 2
fdata = scipy.io.loadmat(fpath)['SIGNAL']
# Remove time channel 
fdata = np.delete(fdata, 0, axis = 1)
# Downsample from 512 Hz to 256 Hz
fdata = fdata[::2]
# # Combine columns indicating trigger for conditions
# fdata[fdata[:, -1] == 1, -1] = 2 # Convert 1 to 2 is last column
# fdata[:, -2] = fdata[:, -1] + fdata[:, -2] # Combine both colums

np.savetxt("subject_" + str(participant)+ ".csv", fdata, delimiter=',')
