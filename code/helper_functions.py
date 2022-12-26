import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from math import pi 
import mne
import time

def init_vars():
    Fs = 512
    time = np.linspace(0, 10, Fs * 10) # Change it so * 10 is not necessary
    return Fs, time 

def filter_sig(sample, Fs):
    filt_sig = mne.filter.filter_data(sample, Fs, None, 3.5, verbose=False)
    return filt_sig

def pwelch(sample, Fs):
    power, freq = mne.time_frequency.psd_array_welch(filt_sig, sfreq=Fs, verbose=False)

# def mean_power(sample, Fs):
    
