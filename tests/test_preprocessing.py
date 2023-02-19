import os 
import sys
import numpy as np
import matplotlib.pyplot as plt

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes.preprocessor import construct_preprocessor

def run_filter():
    Fs = 256 #Hz
    sig_duration = 5  #ms
    time = np.linspace(0, 5, Fs * sig_duration + 1) 
    sig = np.empty(len(time))
    freqs = [0.5, 5]

    # Combine signals
    for freq in freqs:
        sig = np.vstack((sig, np.sin(2 * np.pi * freq * time)))
    cum_sum_sig = np.sum(sig, axis=0) 

    power, freq = pwelch(cum_sum_sig, Fs)
    fsig = filter_sig(cum_sum_sig, Fs, (4, 6))
    fpower, ffreq = pwelch(fsig, Fs)

def test_preprocessor_param_keys():
    valid_pp_params = {
            'filter_bounds' :  (0.5, 5),
            }
    
    valid_preprocessor = construct_preprocessor(valid_pp_params)
    assert type(valid_preprocessor) != KeyError
    
    invalid_pp_params = {
            'filter_bounds' :  (0.5, 5),
            'non_existant_parameter' : (0),
            }

    invalid_preprocessor = construct_preprocessor(invalid_pp_params)
    assert type(invalid_preprocessor) == KeyError


    

    



