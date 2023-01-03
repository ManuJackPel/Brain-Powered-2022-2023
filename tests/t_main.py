import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from math import pi 
import mne
import time

def main():
    # Init Vars
    Fs = 512
    time = np.linspace(0, 10, Fs * 10) # Change it so * 10 is not necessary
    sig = np.empty(len(time))
    # freqs = [0.5, 5]

    for i, frequency in enumerate(freqs):
        sig = np.vstack((sig, np.sin(2 * np.pi * frequency * time)))
    cum_sum_sig = np.sum(sig, axis=0) # Change it so * 10 is not necessary
    # Remove 0-th empty column
    sig = np.delete(sig, 0, 0)
    
    # Filter
    filt_sig = mne.filter.filter_data(cum_sum_sig, Fs, None, 3.5, verbose=False)
    # Pwelch
    power, freq = mne.time_frequency.psd_array_welch(filt_sig, sfreq=Fs, verbose=False)
    # Get average Alpha Band Power
    alpha_range_hz = (8, 12)
    inx = np.where(np.logical_and(freq >= 8, freq <= 12))
    alpha_mean = np.mean(power[inx])
    # Classify

    alph_thresh = 0.005
    if alpha_mean > alpha_thresh:
        eyes_open = True
    else:
        eyes_open = False

    # # Plot waves
    # # for i in range(sig.shape[0]):
    # #     plt.plot(sig[i, :])
    # plt.plot(cum_sum_sig)
    # plt.plot(filt_sig)
    # plt.show()

def classify(data):
    clean_data = pre_process(data)
    filtered_data = filter(clean_data)
    
def filter(data):
    pass

def pre_process():
    # FFT
    pass

if __name__ == "__main__":
    main()

