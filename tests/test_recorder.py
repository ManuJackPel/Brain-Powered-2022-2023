import os 
import sys
import numpy as np
import time
import pandas as pd

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes.recorder import Recorder


def init_recorder():
    directory = '/home/kibble/Documents/School/Brain Powered/Brain-Powered-2022-2023/data/testing/' 
    file_location = directory + 'testing_data.csv'
    header = ['time', 'CH1', 'CH2', 'CH3', 'condition']
    if os.path.exists(file_location):
        os.remove(file_location)

    recorder = Recorder(file_location, header)
    return recorder, file_location, header


def test_recorder_should_make_new_file():
    recorder, file_location, header = init_recorder()
    assert os.path.exists(file_location)

def test_recorder_should_append_to_new_file():
    recorder, file_location, header = init_recorder()
    # Add data to file
    data = np.array([[1, 2, 3, 4, 'open'],
                     [5, 6, 7, 8, 'closed'] ])
    recorder.append_data(data)

    # Import CSV of written file
    written_data = pd.read_csv(file_location)
    d = {'time': [1,5], 'CH1': [2,6], 'CH2' : [3,7], 'CH3' : [4,8], 'condition': ['open', 'closed']}
    right_dataframe = pd.DataFrame(data=d)

    assert written_data.equals(right_dataframe)

def test_recorder_should_have_append_to_already_existing_file():
    recorder, file_location, header = init_recorder()
    # Add data to file
    first_data = np.array([
        [1, 2, 3, 4, 'open'],
        [5, 6, 7, 8, 'closed'] ])
    recorder.append_data(first_data)

    second_data = np.array([
        [9, 10, 11, 12, 'open'],
        [13, 14, 15, 16, 'closed'] ])
    recorder.append_data(second_data)

    # Import CSV of written file
    written_data = pd.read_csv(file_location)
    d = {'time': [1,5,9,13], 'CH1': [2,6, 10, 14], 'CH2' : [3,7,11,15],
         'CH3' : [4,8,12,16], 'condition': ['open', 'closed', 'open', 'closed']}

    right_dataframe = pd.DataFrame(data=d)


def test_recorder_should_prompt_user_if_file_already_exists():
    pass
