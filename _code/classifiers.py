import numpy as np
from numpy import linalg
from scipy.signal import butter, lfilter

def detect_blinks(eeg_data, std_dev=2):
    threshold = std_dev * np.std(eeg_data)

    # Find where the signal exceeds the threshold
    over_threshold = np.where(eeg_data > threshold)[0]

    if len(over_threshold) == 0:
        return 0

    # Find the gaps between the over-threshold regions
    diff = np.diff(over_threshold)
    gaps = np.where(diff > 1)[0]

    # Add the first and last region edges
    first_edge = -1
    last_edge = len(over_threshold)-1
    region_edges = np.concatenate([[first_edge], gaps, [last_edge]])

    
    blinks = np.zeros(len(eeg_data), dtype=int)
    for i in range(len(region_edges) - 1):
        start_point = over_threshold[region_edges[i] + 1]
        end_point = over_threshold[region_edges[i+1]]
        mid_point = (start_point + end_point) // 2
        blinks[mid_point] = 1
    
    return blinks

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs  # Nyquist Frequency
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def cov(trials):
    ''' Calculate the covariance for each trial and return their average '''
    ntrials = trials.shape[2]
    covs = [ trials[:,:,i].dot(trials[:,:,i].T) / nsamples for i in range(ntrials) ]
    return np.mean(covs, axis=0)

def whitening(sigma):
    ''' Calculate a whitening matrix for covariance matrix sigma. '''
    U, l, _ = linalg.svd(sigma)
    return U.dot( np.diag(l ** -0.5) )

def csp(trials_r, trials_f):
    '''
    Calculate the CSP transformation matrix W.
    arguments:
        trials_r - Array (channels x samples x trials) containing right hand movement trials
        trials_f - Array (channels x samples x trials) containing foot movement trials
    returns:
        Mixing matrix W
    '''
    cov_r = cov(trials_r)
    cov_f = cov(trials_f)
    P = whitening(cov_r + cov_f)
    B, _, _ = linalg.svd( P.T.dot(cov_f).dot(P) )
    W = P.dot(B)
    return W

def apply_mix(W, trials):
    ''' Apply a mixing matrix to each trial (basically multiply W with the EEG signal matrix)'''
    ntrials = trials.shape[2]
    trials_csp = np.zeros((nchannels, nsamples, ntrials))
    for i in range(ntrials):
        trials_csp[:,:,i] = W.T.dot(trials[:,:,i])
    return trials_csp


def train_classifier(classifier, cleaned_train_data):
    # Concatenate the data for each class
    cleaned_train_data = np.concatenate((train[cl1], train[cl2]), axis=1).T
    # Create target labels
    train_labels = np.concatenate((np.ones(train[cl1].shape[1]), np.zeros(train[cl2].shape[1])))
    # Train the SVM model 
    classifier.fit(train_data, train_labels)
