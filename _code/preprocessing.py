import numpy as np 
import mne

def filter_sig(sample, Fs, freq_range: tuple[float, float]):
    low_bnd, up_bnd = freq_range
    filt_sig = mne.filter.filter_data(sample, Fs, low_bnd, up_bnd, verbose=False)
    return filt_sig

def pwelch(sample, Fs):
    power, freq = mne.time_frequency.psd_array_welch(sample, sfreq=Fs, verbose=False)
    return power, freq
    

    
