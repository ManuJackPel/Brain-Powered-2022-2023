"Class for choosing what data to import into the classification progam"

import os 
import re
import scipy 
import numpy as np 
import matplotlib.pyplot as plt
import math
import time

# Acquire root directory
directory = __file__
for i in range(3):
    directory = os.path.dirname(directory)
root_directory = directory

class DataLoader:
    def __init__(self, data_source, participant=0, channels=np.arange(0,8)):
        self.participant = None
        
        # Input Check
        if participant < 10:
            participant = "0" + str(participant)

        assert len(channels) == 8
        assert np.all(channels < 16)

        if data_source == "GIPSA-lab":
            # Get the amount of files that are
            data_directory = root_directory + '/data/EEG_alpha_waves_dataset'
            fname = "subject_" + str(participant)+ ".mat"

            # Get path for file
            fpath = os.path.join(data_directory, fname)
            # Col 1: Timestamps, Col 2-17: Electrode Recording, Col 18-19: Triggers for Condition 1 and 2
            fdata = scipy.io.loadmat(fpath)['SIGNAL']
            # Remove time channel 
            fdata = np.delete(fdata, 0, axis = 1)
            # Downsample from 512 Hz to 256 Hz
            fdata = fdata[::2]
            # Combine columns indicating trigger for conditions
            fdata[fdata[:, -1] == 1, -1] = 2 # Convert 1 to 2 is last column
            fdata[:, -2] = fdata[:, -1] + fdata[:, -2] # Combine both colums
            fdata = np.delete(fdata, -1 , axis = 1)

        self._data = fdata[:, channels]
        self._triggers = fdata[:, -1]
        self.last_pulled_index = -1
        self.pull_time = time.time() + 1/256


    def pull_sample(self):
        self.last_pulled_index += 1 
        time.sleep(max(0.0, self.pull_time - time.time()))
        self.pull_time += 1/256
        return self._data[self.last_pulled_index]
    
    def return_data(self):
        return self._data
    
    def return_triggers(self):
        return self._triggers


