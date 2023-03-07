import os 
import sys
import numpy as np
import time

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes.recorder import make_buffer, update_buffer


def init_buffer():
    header = ['time', 'CH1', 'CH2', 'CH3', 'CH4']
    buffer_len = 4
    buffer = make_buffer(header, buffer_len)
    return buffer, buffer_len, header

def test_buffer_has_right_shape():
    buffer, buffer_len, header = init_buffer()
    assert buffer.shape == (buffer_len, len(header)) 

def test_buffer_has_header_at_top():
    pass

def test_buffer_appends():
    buffer, buffer_len, header = init_buffer()

    # sample = [-2458.5708008, 307.06546021, -6745.5673828, -6479.7578125]
    sample = [1, 2, 3, 4]
    timestamp = 12.45

    combined_array = np.array(([timestamp] + sample))
    updated_buffer = update_buffer(buffer, combined_array)
    right_buffer = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [12.45, 1, 2, 3, 4]])
    assert np.array_equal(right_buffer, updated_buffer)

    combined_array = np.array([13.45, 0, 0, 0, 0])
    updated_buffer = update_buffer(updated_buffer, combined_array)
    right_buffer = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [12.45, 1, 2, 3, 4],
        [13.45, 0, 0, 0, 0]])
    assert np.array_equal(right_buffer, updated_buffer)

    combined_array = np.array([[14.45, 0, 0, 0, 0], [15.45, 0, 0, 0, 1]])
    updated_buffer = update_buffer(updated_buffer, combined_array)
    right_buffer = np.array([
        [12.45, 1, 2, 3, 4],
        [13.45, 0, 0, 0, 0],
        [14.45, 0, 0, 0, 0],
        [15.45, 0, 0, 0, 1]])
    assert np.array_equal(right_buffer, updated_buffer)

    # TEST IF OLD ITEMS GET REMOVED
    combined_array = np.array([[16.45, 0, 4, 0, 2], [17.45, 0, 0, 0, 1]])
    updated_buffer = update_buffer(updated_buffer, combined_array)
    right_buffer = np.array([
        [14.45, 0, 0, 0, 0],
        [15.45, 0, 0, 0, 1],
        [16.45, 0, 4, 0, 2], 
        [17.45, 0, 0, 0, 1]])
    assert np.array_equal(right_buffer, updated_buffer)


