import os 
import sys
import numpy as np
import time

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes import dataloader

channels = ['Fp1', 'Fp2', 'Fc5', 'Fz', 'Fc6', 'T7', 'Cz', 'T8']
stream = dataloader.DataLoader('GIPSA-lab', channels, participant = 0)

def test_static_sample_speed():
    test_duration = 5 # seconds
    samp_data = stream.pull_sample()
    start_time = time.time()
    while True:
        output = stream.pull_sample()
        samp_data = np.vstack((samp_data, output))
        if time.time() - start_time >= test_duration:
            break
    n_samples = samp_data.shape[0]
    assert abs(n_samples - test_duration * 256) < 4


def test_data_shape():
    nrows, ncols = stream.return_data().shape
    assert ncols == 8

def test_combination_trigger_cols():
    triggers = stream.return_triggers()
    triggers_combined_properly = np.array_equal(np.unique(triggers), np.array([0, 1., 2.]))
    assert triggers_combined_properly, f"When transforming the data the last column should only consist of 0, 1, 2"

def test_channel_to_name():
    ch_names = ['Fp2', 'Fc5', 'Cz', 'Fp1', 'Oz', 'P4', 'Fc6', 'Fz']
    ch_ints = stream.channel_to_int(ch_names)
    assert ch_ints.sort() == [2, 3, 7, 1, 15, 12, 5 ,4].sort()
