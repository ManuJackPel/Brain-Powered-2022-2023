import os 
import sys
import numpy as np
import time
from tkinter import filedialog as fp
import time

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes.recorder import make_buffer, update_buffer

def main():
    # Init recorder
    header = ['time', 'CH1', 'CH2', 'CH3', 'CH4'] 
    # file_name = fp.askopenfilename()

    # Determines how often buffer is appended to save file
    saving_refresh_rate = 1 # save every 5 seconds
    samples_pulled_since_save = 0
    # Init databuffer of size sample_refresh_rate x length header
    data_buffer = make_buffer(header, buffer_size=saving_refresh_rate)
    # Export a list of samples from each channel and the timestamp as a float

    start_time = time.time()
    samples_pulled_since_save = 0
    with open('test_record.csv', 'a', encoding='UTF8') as f:
        f.truncate(0)
    while True:
        # Append timestamp to front of list and turn into numpy array
        timestamp = round(time.time() - start_time, 3)
        sample = [1 ,2, 3, 4]
        sample = [timestamp * elem for elem in sample]
        combined_array = np.array(([timestamp] + sample))

        data_buffer = update_buffer(data_buffer, combined_array)
        samples_pulled_since_save += 1

        if samples_pulled_since_save == saving_refresh_rate:
            samples_pulled_since_save = 0
            time.sleep(1)
            print(data_buffer.shape)
            with open('test_record.csv', 'a', encoding='UTF8') as f:
                np.savetxt(f, data_buffer)

main()



