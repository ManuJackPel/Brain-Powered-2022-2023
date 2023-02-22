# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

data = np.genfromtxt('sample_eeg_data_motor_imagery.txt', delimiter=',').T # import and transpose data
data_mv = data/100000 # Converting to microVolt

def psd_alpha(nchannels, signal, fs):
    '''
    For each trial calculate the Power Spectral Density (PSD)
    
    Parameters
    -----------
    nchannels: float
        --> number of eeg channels used

    signal: 2d-array (amplitude x time)
        --> The EEG signal

    fs: float
        --> Sampling frequency of signal

    Returns
    ----------
    alphas: dictionary with nchannel keys (each key: frequency x power)
        --> the PSD of the signal of each channel
    '''

    alphas = {}
    for channel in range(nchannels):
        f,psd = scipy.signal.periodogram(signal[channel],fs, scaling='density')
        idx = (f>=8) & (f<=12)
        alphaband = np.array([f[idx],psd[idx]])
        plt.semilogy(alphaband[0],alphaband[1], label='Channel {}'.format(channel+1)) # optional
        plt.xlim([8,13])
        plt.legend(loc='right', prop={'size':6})
        alphas['channel {}'.format(channel+1)] = max(alphaband[1])

    return alphas

psd_alpha(data_mv.shape[0],data_mv,256)
# %%
