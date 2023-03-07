import numpy as np
import os

class Recorder():
    def __init__(self, file_name, header):
        self.file_name = file_name
        self.header = header

    def append_data(self, data):
        if self.file_name_exists():
            self._append_to_txt(data)
        else:
            self._create_txt()

    def file_name_exists(self):
        return os.path.isfile(self.file_name)

    def _append_to_txt(self, data):
        with open(self.file_name, 'a', encoding='UTF8') as f:
            f.truncate(0)
            np.savetxt(f, data)

    def _create_txt(self):
        with open(self.file_name, 'w', encoding='UTF8') as f:
            f.write(self.header)
            f.close()

def make_buffer(header: list, buffer_size: int) -> np.ndarray:
    col_size = len(header)
    row_size = buffer_size
    return np.zeros((row_size, col_size))


def update_buffer(buffer, new_sample):
    """
    Queue. Oldest data is removed and newest data is appended
    Returns immutable array
    """
    # Make buffer mutable
    buffer.setflags(write=True) 

    # If sample is 1-dimensional get length
    # Else get amount of rows
    if len(new_sample.shape) == 0:
        print('Empty sample was passed')
    elif len(new_sample.shape) == 1:
        rows_to_roll = 1
    else:
        rows_to_roll = new_sample.shape[0]
        
    buffer = np.roll(buffer, -rows_to_roll, axis=0)

    buffer[-rows_to_roll:, :] = new_sample
    # Make buffer immutable
    buffer.setflags(write=False) 
    return buffer
