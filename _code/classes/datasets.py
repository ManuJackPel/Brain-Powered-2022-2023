"Class for choosing what data to import into the classification progam"

import os 
import re
import scipy 
import numpy as np 
import matplotlib.pyplot as plt
import time


# Acquire root directory
directory = __file__
for i in range(3):
    directory = os.path.dirname(directory)
root_directory = directory

class DataSets:
    def __init__(self, data_source, channels, set_type, participant=0):
        self.data_source = data_source
        self.channels = channels
        self.set_type = set_type
        self.participant = participant

        if data_source == "GIPSA-lab":
            self.data_set = self.make_GIPSA_set()


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

    def make_GIPSA_set(self):
        participant = self.participant
        if participant < 10:
            participant = "0" + str(participant)

        data_directory = root_directory + '/data/EEG_alpha_waves_dataset'
        fname = "subject_" + str(participant)+ ".mat"
        # Get path for file
        fpath = os.path.join(data_directory, fname)
        # Col 1: Timestamps, Col 2-17: Electrode Recording, Col 18-19: Triggers for Condition 1 and 2
        fdata = scipy.io.loadmat(fpath)['SIGNAL']
        return fdata

    def split_by_label(self):
        """Split whole dataset into an array of samples along with the label"""
        
        columns = [17, 18]
        identifier = 1
        split_data_set = np.zeros((1)) 
        _class = 1
        for column in columns:
            # Find all indices with a 1 in row 18
            event_onset_index = np.where(self.data_set[:, column] == 1)
        
            # # Get time of the index
            # event_onset_time = self.data_set[event_onset_index, 0]
            #     eyes_open_offset_index = (np.where(self.data_set[:,0] == eyes_open_onset_time + 10))
            #     eyes_open_onset_index = np.where(self.data_set[:, 0] == eyes_open_onset_time)

            #     sample_data = self.data_set[eyes_open_onset_index[0][0]:eyes_open_offset_index[0][0], 5].shape
            #     lable = 1                    
            # _class += 1

            
        # Take the 10 seconds following that
        # If they 1 is in row 0
        

        pass
        
    def return_labeled_data(self):
        """
        Return the labeled data in the form (sample, data)
        sample: {array-like} of shape (n_samples, n_features)
        label: {array-like} of shape (n_samples)
        """


        split_data = self.split_by_label()
        sample = split_data

        return sample, label

    def return_training_set(self):
        return self.data_set
        



