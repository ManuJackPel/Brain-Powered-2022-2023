import pandas as pd
import numpy as np
from collections import OrderedDict

def import_csv(task_data_dir, raw_data_dir):
    # Trial Data
    task_data = pd.read_csv(task_data_dir, header=7, sep=',')
    task_data.rename(columns={"'Trial Number" : 'trial number', "Hand Condition'": 'condition'}, inplace=True)
    task_data['condition'] = task_data['condition'].str.rstrip("'")
    task_data['trial number'] = task_data['trial number'].str.strip("'")

    # Extract the condition list
    trial_condition = np.array(task_data['condition'].apply(int))

    # Read the raw data
    raw_data = pd.read_csv(raw_data_dir, delimiter=',', skiprows=1)
    raw_data.rename(columns={'Unnamed: 22': 'marker time', 'Unnamed: 23': 'marker type'}, inplace=True)

    # Get the indices for start and finish
    task_start_index = raw_data[raw_data['marker type'].isin(['trial'])].index
    task_end_index = raw_data[raw_data['marker type'].isin(['Pause'])].index

    # Get raw data for each trial
    trial_data = OrderedDict()
    for trial, (start, end) in enumerate(zip(task_start_index, task_end_index)):
        interval = raw_data[start:end]
        interval = interval.drop(columns=['Timestamp', 'Hardware timestamp', 'Unnamed: 21', 'marker time', 'marker type'])
        interval.reset_index(drop=True, inplace=True)
        trial_data[trial + 1] = interval[0:840]

    assert len(trial_data.keys()) == 140

    return trial_data, trial_condition

