import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import mne

# Convert EEG data array to mne RAW file
data = genfromtxt('data.csv', delimiter = ',')  # import data csv
data = data[1:9,:]                              # remove 9th empty row
data = data/100000                               # convert to microV
ch_names = [                                    # specify channel names
    'channel 1',
    'channel 2',
    'channel 3',
    'channel 4',
    'channel 5',
    'channel 6',
    'channel 7',
    'channel 8']
sfreq = 256                             # specify sampling frequency of data
channel_type = 'eeg'                    # Specify channel type

info = mne.create_info(                 # Create MNE info file with measurement meta data
    ch_names, 
    sfreq, 
    ch_types, 
    verbose=None)    

raw = mne.io.RawArray(data,info)        # Create RAW file with data and metadata

#check RAW file
raw.info    # check metadata
raw.plot()  # plot EEG

# plot EEG as array
for i in range(8):
    plt.plot(data[i,:], label = 'channel {}'.format(i))
    plt.legend()

plt.show()