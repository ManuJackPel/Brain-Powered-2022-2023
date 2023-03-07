import os 
import mne
import sys
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes.preprocessor import PreProcessorBuilder



#####################
# Helper Functions
####################

dummy_filter_params = {
        'data' : None,
        'sfreq' : 256,
        'l_freq' : 8,
        'h_freq' : 12,
        'verbose' : False,
        }

def init_pp_builder_with_filter():
    pp_builder = PreProcessorBuilder()
    pp_builder.add_filter(dummy_filter_params)
    return pp_builder

def generate_noisy_signal()-> np.ndarray:
    # Pick a random frequency between 0 and 50 
    random_freq = np.random.randint(0,50)
    # Pick a random amplitude between 0 and 5
    random_amplitude = np.random.randint(1,5)
    signal = np.sin(np.arange(0, 1080) * random_freq * np.pi / 180. ) 
    for i in range(10):
        # Pick a random frequency between 0 and 50 
        random_freq = np.random.randint(0,50)
        # Pick a random amplitude between 0 and 5
        random_amplitude = np.random.randint(1,5)
        signal += np.sin(np.arange(0, 1080) * random_freq * np.pi / 180. ) 
    return signal


#####################
# Assertions Tests
####################
def test_pp_builder_list_parts():
    pp_builder = init_pp_builder_with_filter()
    parts = pp_builder.list_parts()
    assert parts == ['fir_filter'], "Listed Parts do not match with added parts for PreProcessorBuilder"

def test_pp_same_as_mne_filter():
    pp_builder = init_pp_builder_with_filter()
    pp = pp_builder.build()

    random_data = generate_noisy_signal()
    mne_params = deepcopy(dummy_filter_params)
    mne_params['data'] = random_data

    err_msg = 'filter in process does not match the MNE filter'
    assert np.array_equal(pp.process_data(random_data), mne.filter.filter_data(**mne_params)), err_msg


################
# Visual Tests
################

def visual_comparison_mne_and_class_filter():
    pp_builder = init_pp_builder_with_filter()
    pp = pp_builder.build()

    fig, (ax1, ax2) = plt.subplots(2, 1)
    data = generate_noisy_signal()
    ax1.plot(pp.process_data(data))

    params = deepcopy(dummy_filter_params)
    params['data'] = data
    ax2.plot(mne.filter.filter_data(**params))
    plt.show()

