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


valid_params = {
        'filter_bounds' : tuple,
        }

parameter_checker = ParameterChecker(valid_params)


def construct_preprocessor(preprocessor_params: dict):
    # Iterate through the params
    parameter_names = tuple(preprocessor_params.keys())
    if not parameter_checker.is_valid_parameter_names(parameter_names):
        return KeyError()
    return None
