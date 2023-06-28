from numpy import linalg
import numpy as np
import scipy.signal
import scipy

class CSP():
    def __init__(self, cl_one_data, cl_two_data):
        self.n_channels, self.n_samples, self.n_trials = cl_one_data.shape
        self.W = self.csp(cl_one_data, cl_two_data)

    def csp(self, trials_r, trials_f):
        '''
        Calculate the CSP transformation matrix W.
        arguments:
            trials_r - Array (channels x samples x trials) containing right hand movement trials
            trials_f - Array (channels x samples x trials) containing foot movement trials
        returns:
            Mixing matrix W
        '''
        cov_r = self.cov(trials_r)
        cov_f = self.cov(trials_f)
        P = self.whitening(cov_r + cov_f)
        B, _, _ = linalg.svd( P.T.dot(cov_f).dot(P) )
        W = P.dot(B)
        return W


    def cov(self, trials):
        ''' Calculate the covariance for each trial and return their average '''
        ntrials = trials.shape[2]
        covs = [ trials[:,:,i].dot(trials[:,:,i].T) / self.n_samples for i in range(ntrials) ]
        return np.mean(covs, axis=0)


    def whitening(self, sigma):
        ''' Calculate a whitening matrix for covariance matrix sigma. '''
        U, l, _ = linalg.svd(sigma)
        return U.dot( np.diag(l ** -0.5) )


    def __call__(self, trials):
        ''' Apply a mixing matrix to each trial (basically multiply W with the EEG signal matrix)'''
        ntrials = trials.shape[2]
        trials_csp = np.zeros((self.n_channels, self.n_samples, self.n_trials))
        for i in range(ntrials):
            trials_csp[:,:,i] = self.W.T.dot(trials[:,:,i])
        return trials_csp

def bandpass(trials, lo, hi, sample_rate):
    '''
    Designs and applies a bandpass filter to the signal.
    
    Parameters
    ----------
    trials : 3d-array (channels x samples x trials)
        The EEGsignal
    lo : float
        Lower frequency bound (in Hz)
    hi : float
        Upper frequency bound (in Hz)
    sample_rate : float
        Sample rate of the signal (in Hz)
    
    Returns
    -------
    trials_filt : 3d-array (channels x samples x trials)
        The bandpassed signal

    Adapted from https://github.com/wmvanvliet/neuroscience_tutorials/blob/master/eeg-bci/3.%20Imagined%20movement.ipynb
    '''

    # The iirfilter() function takes the filter order: higher numbers mean a sharper frequency cutoff,
    # but the resulting signal might be shifted in time, lower numbers mean a soft frequency cutoff,
    # but the resulting signal less distorted in time. It also takes the lower and upper frequency bounds
    # to pass, divided by the niquist frequency, which is the sample rate divided by 2:
    a, b = scipy.signal.iirfilter(6, [lo/(sample_rate/2.0), hi/(sample_rate/2.0)])

    # Applying the filter to each trial
    trials_filt = []
    for data_df in trials: 
        df_filt = data_df.apply(lambda x: scipy.signal.filtfilt(b, a, x), axis=0)
        trials_filt.append(df_filt)

    return trials_filt

