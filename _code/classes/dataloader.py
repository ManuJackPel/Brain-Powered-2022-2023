"Class for choosing what data to import into the classification progam"

import os 
import re
import scipy 
import numpy as np 
import matplotlib.pyplot as plt
import math

# Acquire root directory
directory = __file__
for i in range(3):
    directory = os.path.dirname(directory)
root_directory = directory

class DataLoader:
    def __init__(self, data_source, participant=0, channels=np.arange(0,8)):
        self.participant = None

        if data_source == "GIPSA-lab":
            # Get the amount of files that are
            data_directory = root_directory + '/data/EEG_alpha_waves_dataset'
            fnames = os.listdir(data_directory)
            regex_file_name = re.compile('^subject\S+mat$')
            fnames = list(filter(regex_file_name.match, fnames))


            for fname in fnames:
                # Get path for file
                fpath = os.path.join(data_directory, fname)
                # Col 1: Timestamps, Col 2-17: Electrode Recording, Col 18-19: Triggers for Condition 1 and 2
                fdata = scipy.io.loadmat(fpath)['SIGNAL']
                # Remove time channel 
                fdata = np.delete(fdata, 0, axis = 1)
                # Downsample from 512 Hz to 256 Hz
                fdata = fdata[::2]
                # Combine colums indicating trigger for conditions
                fdata[fdata[:, -1] == 1, -1] = 2 # Convert 1 to 2 is last column
                fdata[:, -2] = fdata[:, -1] + fdata[:, -2] # Combine both colums
                fdata = np.delete(fdata, -1 , axis = 1)

                # Assert that combination of last two trigger cols went right
                last_col_only_has_triggers = np.array_equal(np.unique(fdata[:,-1]), np.array([0, 1. , 2.]))
                sec_to_last_col_no_triggers = not np.array_equal(np.unique(fdata[:,-2]), np.array([0, 1. , 2.]))
                assert last_col_only_has_triggers, f"When transforming the data the last column should only consist of 0, 1, 2"
                assert sec_to_last_col_no_triggers, f"The second to last column should not consist of trigger markers 0, 1 ,2"

                

                
                # Display Data
                fig, axs = plt.subplots(4, 5)
                for i in range(17):
                    row = i % 4 
                    col = math.floor(i / 4)
                    axs[row, col].plot(fdata[:1000, i])
                plt.show()
                break
            

    def pull_sample():
        pass
