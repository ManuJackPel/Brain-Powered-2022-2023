import os 
import sys
import numpy as np
import matplotlib.pyplot as plt

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.preprocessing import *

Fs = 256 #Hz
sig_duration = 5  #ms
time = np.linspace(0, 5, Fs * sig_duration + 1) 
sig = np.empty(len(time))
freqs = [0.5, 5]

# Combine signals
for freq in freqs:
    sig = np.vstack((sig, np.sin(2 * np.pi * freq * time)))
cum_sum_sig = np.sum(sig, axis=0) 

""" 
source: https://dsp.stackexchange.com/questions/24819/how-to-test-digital-filters 
 - Filter Should Be Linear
 - Filter Should Be Time-Invariant
 - Filter has correct impulse response
"""

power, freq = pwelch(cum_sum_sig, Fs)
fsig = filter_sig(cum_sum_sig, Fs, (4, 6))
fpower, ffreq = pwelch(fsig, Fs)

# fig, axs = plt.subplots(1,2)
# axs[0].plot(freq, power)
# axs[1].plot(ffreq, fpower)
# plt.show()

