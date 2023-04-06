import numpy as np
import os

class Recorder():
    def __init__(self, file_name:str, header:list):
        self.file_name = file_name
        self.header = header
        self.data_buffer = np.empty((0, len(header)))

        if not self.file_name_exists():
            self._create_file()

    def append_data(self, data): 
        self._append_to_buffer(data)

    def save(self, reset_buffer=True) -> None:
        if not self.file_name_exists():
            self._create_file()

        with open(self.file_name, 'a', encoding='UTF8') as f:
            # see if data is one-dimensional
            assert len(self.data_buffer.shape) == 2, "Data to append should be 2D"
            np.savetxt(f, self.data_buffer, fmt='%s', delimiter=',')

        if reset_buffer:
            self.empty_buffer()

    def empty_buffer(self) -> None:
        self.data_buffer = np.empty((0, len(self.header)))

    def file_name_exists(self):
        return os.path.exists(self.file_name)

    def _append_to_buffer(self, data:np.ndarray):
        self.data_buffer = np.vstack((self.data_buffer, data))

    def _create_file(self):
        with open(self.file_name, 'w', encoding='UTF8') as f:
            f.write(','.join(self.header))
            f.write('\n')
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
