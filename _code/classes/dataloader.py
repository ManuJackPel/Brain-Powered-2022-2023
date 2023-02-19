"Class for choosing what data to import into the classification progam"

import os 
import scipy 
import numpy as np 
import matplotlib.pyplot as plt
import time


# Acquire root directory
directory = __file__
for i in range(3):
    directory = os.path.dirname(directory)
root_directory = directory

class DataLoader:
    def __init__(self, data_source, channels, participant=0):
        self.participant = None
        
        # Input Check
        if participant < 10:
            participant = "0" + str(participant)
        assert len(channels) == 8

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
        else:
            assert False, "invalid dataset passed to DataLoader"

        self._data = fdata[:, self.channel_to_int(channels)]
        self._triggers = fdata[:, -1]
        self.pull_index_head = -1
        self.pull_time = time.time() + 1/256


    def pull_sample(self, n_pulled_samples):
        self.pull_index_head += n_pulled_samples 
        time.sleep(max(0.0, self.pull_time - time.time()))
        self.pull_time += n_pulled_samples/256
        pull_index_tail = self.pull_index_head - n_pulled_samples
        return self._data[pull_index_tail : self.pull_index_head]
    
    def return_data(self):
        return self._data
    
    def return_triggers(self):
        return self._triggers

    def channel_to_int(self, ch_names):
        ch_to_int = {
            'Fp1' : 1,
            'Fp2' : 2, 
            'Fc5' : 3,
            'Fz' : 4,
            'Fc6' : 5,
            'T7' : 6,
            'Cz' : 7, 
            'T8' : 8,
            'P7' : 9,
            'P3' : 10,
            'Pz' : 11,
            'P4' : 12,
            'P8' : 13,
            'O1' : 14,
            'Oz' : 15,
            'O2' : 16}
        return [ch_to_int[ch_name] for ch_name in ch_names]
