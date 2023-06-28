import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from _code.feature_extraction import bandpass
import pickle
from scipy.signal import butter, sosfiltfilt
from _code.feature_extraction import CSP

FS = 250
cl1 = 'left'
cl2 = 'right'


def get_filtered_matrices():
    # Load in pickled data
    trials_raw, trials_filt, channel_names = load_pickled_data()
    print('Loaded data')

    trials_filt_matrix = {}
    trials_filt_matrix[cl1] = np.array(trials_filt[cl1]).transpose(2, 1, 0)
    trials_filt_matrix[cl2] = np.array(trials_filt[cl2]).transpose(2, 1, 0)

    return trials_filt_matrix


def load_pickled_data():
    with open('../eventide_data/manu_mm_1.pickle', 'rb') as f:
        base_report_one, raw_data_one = pickle.load(f)
    with open('../eventide_data/manu_mm_2.pickle', 'rb') as f:
        base_report_two, raw_data_two = pickle.load(f)

    trials_raw = { cl1: [], cl2: [], }
    trials_filt = { cl1: [], cl2: [], }

    lower_bound = 0
    upper_bound = 820

    data = [
        (base_report_one, raw_data_one),
        (base_report_two, raw_data_two),
        ]
        
    for base_report, raw_data in data:
        task_start_index = raw_data[raw_data['marker type'].isin(['trial'])].index
        task_end_index = raw_data[raw_data['marker type'].isin(['Pause'])].index
        trial_condition = np.array(base_report['condition'].apply(int))

        sos = butter(N=2, Wn=[8, 15], btype='band', fs=250, output='sos')

        raw_data_filt = raw_data.drop(columns=['Timestamp',  'bs1', 'marker', 'marker time', 'marker type'])
        raw_data_filt = raw_data_filt.apply(lambda x: sosfiltfilt(sos, x), axis=0)

        for start, end, _class in zip(task_start_index, task_end_index, trial_condition):
            raw_interval= raw_data[start:end]
            filt_interval= raw_data_filt[start:end]

            raw_interval.reset_index(drop=True, inplace=True)
            filt_interval.reset_index(drop=True, inplace=True)

            if _class == 0:
                trials_raw[cl1].append(raw_interval[lower_bound:upper_bound])
                trials_filt[cl1].append(filt_interval[lower_bound:upper_bound])

            elif _class == 1:
                trials_raw[cl2].append(raw_interval[lower_bound:upper_bound])
                trials_filt[cl2].append(filt_interval[lower_bound:upper_bound])
            
    channel_names = list(trials_filt[cl1][0].columns)
    return trials_raw, trials_filt, channel_names

def get_trials_logvar(trials):
    trials_logvar = []
    for data_df in trials:
        logvar_df = data_df.apply(lambda x: np.log(x.var()), axis=0)
        trials_logvar.append(logvar_df)
    return trials_logvar

if __name__ == "__main__":
    get_filtered_matrices()
