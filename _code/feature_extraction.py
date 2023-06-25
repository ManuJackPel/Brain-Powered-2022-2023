from numpy import linalg

class CSP():
    def __init__(cl_one_data, cl_two_data):
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
        covs = [ trials[:,:,i].dot(trials[:,:,i].T) / nsamples for i in range(ntrials) ]
        return np.mean(covs, axis=0)


    def whitening(self, sigma):
        ''' Calculate a whitening matrix for covariance matrix sigma. '''
        U, l, _ = linalg.svd(sigma)
        return U.dot( np.diag(l ** -0.5) )


    def __call__(trials):
        ''' Apply a mixing matrix to each trial (basically multiply W with the EEG signal matrix)'''
        ntrials = trials.shape[2]
        trials_csp = np.zeros((nchannels, nsamples, ntrials))
        for i in range(ntrials):
            trials_csp[:,:,i] = self.W.T.dot(trials[:,:,i])
        return trials_csp

