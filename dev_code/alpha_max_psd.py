# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

data = np.genfromtxt('sample_eeg_data_motor_imagery.txt', delimiter=',').T # import and transpose data
data_mv = data/100000 # Converting to microVolt

# %%
def psd_alpha(nchannels, signal, fs, method='periodogram', plot=False):
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

    method: str ('periodogram' or 'welch')
        --> method used for creating the psd. Welch is faster, periodogram is more accurate

    plot: Bool

    Returns
    ----------
    alphas: dictionary with nchannel keys (each key: frequency x power)
        --> the PSD of the signal of each channel
    '''
    # Create empty list for alpha powers
    alphas = {}

    # create psd using periodogram or welch method for each channel of signal
    for channel in range(nchannels):
        if method == 'periodogram':
            f,psd = scipy.signal.periodogram(signal[channel],fs, scaling='density')
        elif method == 'welch':
            f,psd = scipy.signal.welch(signal[channel],fs, scaling='density')
        else:
            raise ValueError('Method argument needs to be "periodogram" or "welch"')
    
    # fill in alpha power list
        idx = (f>=8) & (f<=12)
        alphaband = np.array([f[idx],psd[idx]])
        alphas['channel {}'.format(channel+1)] = max(alphaband[1])

    # Optional plot of psd
        if plot == True:
            plt.semilogy(alphaband[0],alphaband[1], label='Channel {}'.format(channel+1)) # optional
            plt.xlim([8,13])
            plt.legend(loc='right', prop={'size':6})
        elif plot == False:
            continue    
        else:
            raise ValueError('Plot argument needs to be a boolean input')

    return alphas
# %%
psd_alpha(data_mv.shape[0],data_mv,256, method='periodogram', plot=False)
# %%
