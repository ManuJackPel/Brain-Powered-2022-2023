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

stream = dataloader.DataLoader('GIPSA-lab', participant = 0)


def test_static_sample_speed():
    test_duration = 5 # seconds
    start_time = time.time()
    samp_data = stream.pull_sample()
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

test_static_sample_speed()
