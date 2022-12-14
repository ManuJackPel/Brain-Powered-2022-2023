import numpy as np
from matplotlib import pyplot as plt

import mne
from mne import create_info, Epochs
from mne.baseline import rescale
from mne.io import RawArray
from mne.time_frequency import (tfr_multitaper, tfr_stockwell, tfr_morlet,
                                tfr_array_morlet, AverageTFR)
from mne.viz import centers_to_edges

#for testings
from numpy import genfromtxt



sfreq = 256
ch_names = ['SIM0001', 'SIM0002', 'SIM0003', 'SIM0004', 'SIM0005', 'SIM0006', 'SIM0007', 'SIM0008', 'SIM0009']
ch_types = ['grad', 'grad', 'grad', 'grad', 'grad', 'grad', 'grad', 'grad', 'grad']
info = create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

n_times = 1024  # Just over 1 second epochs
n_epochs = 1
data = genfromtxt('data.csv', delimiter=',')

#raw = RawArray(data, info)
#events = np.zeros((n_epochs, ), dtype=int)
#events[:, 0] = np.arange(n_epochs) * n_times
#epochs = Epochs(raw, events, dict(sin50hz=0), tmin=0, tmax=n_times / sfreq,
#                reject=dict(grad=4000), baseline=None)



output = mne.time_frequency.psd_array_welch(data, sfreq, fmin=0, fmax=50, n_fft=256, n_overlap=0, n_per_seg=256, n_jobs=None, average='mean', window='hamming', verbose=None)
print(output)
