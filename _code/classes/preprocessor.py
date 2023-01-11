import numpy as np
import mne

class Preprocess():
    """Interface for preprocessin EEG classification methods"""
    def __init__(self, pp_args: dict):
        self.filt_range = pp_args['filt_range']
        self.samp_freq = pp_args['samp_freq']

    def filter_sig(self, sample):
        low_bnd, up_bnd = self.filt_range
        filt_sig = mne.filter.filter_data(sample, self.samp_freq, low_bnd, up_bnd, verbose=False)
        return filt_sig

    def transform(self, sample):
        return self.filter_sig(sample)
