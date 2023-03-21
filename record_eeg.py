import os 
import sys
import numpy as np
import time
from tkinter import filedialog as fp
import time
from multiprocessing import Process, Pipe
import multiprocessing
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scipy.signal

from _code.classes.recorder import make_buffer, update_buffer, Recorder
from _code.classes.dataloader import MobiLab


def data_stream(data_pipe_start, condition_pipe_end):
    # Init LSL Inlet for MobiLab
    eeg_stream = MobiLab()
    # Init Recorder
    header = ['time', 'CH1', 'CH2','CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', 'CH9'] 
    file_location = input("Insert file location")
    recorder = Recorder(file_location, header)
    # Init DataBuffer
    vis_data_buffer = make_buffer(header, buffer_size=1024)

    start_time = time.time()
    while True:
        # Pull Sample from MobiLab and Condition from alpha task
        sample, timestamp = eeg_stream.pull_sample()
        condition, participant = condition_pipe_end.recv()

        # End recording if stop_threshold is reached
        if 'stop_threshold' in condition:
            print('saving the data')
            recorder.save()

        # Combine timestamp and channel data
        combined_array = np.array([timestamp] + sample + [condition])
        # Append to recorder
        recorder.append_data(combined_array)
        # Append to visualization buffer
        vis_data_buffer = update_buffer(vis_data_buffer, combined_array)

        # Save data and send data to visualization process every n seconds
        if time.time() - start_time >= 0.5:
            start_time = time.time()
            recorder.save()
            data_pipe_start.send(vis_data_buffer)

def data_visualization(pipe_end):
    def animate(i):
        data_buffer = pipe_end.recv()
        time = data_buffer[:,0]
        channels = data_buffer[:,[1,9]]

        plt.cla()
        plt.xlim([data_buffer[0,0], data_buffer[-1,0]])
        plt.ylim([-3,3])
        plt.plot(time, channels, '--')

    ani = FuncAnimation(plt.gcf(), animate, interval=125)    
    plt.show()

def get_alpha_task_condition(condition_pipe_start):
    while True:
        with open('dev_code\psychopy\condition.txt') as f:
            condition_file = f.readlines()
            condition = condition_file[0]
            participant = condition_file[1]
            # Send data to recorder
            condition_pipe_start.send((condition, participant))

if __name__ == "__main__":  
    # Init Pipeline, set duplex to False to make it unidirectional
    data_pipe_end, data_pipe_start = Pipe(duplex=False)
    condition_pipe_end, condition_pipe_start = Pipe(duplex=False)

    eeg_stream_process = Process(target = data_stream, args = (data_pipe_start, condition_pipe_end))
    eeg_stream_process.start()

    visualization_process = Process(target = data_visualization, args = (data_pipe_end,))
    visualization_process.start()

    alpha_task_process = Process(target = get_alpha_task_condition, args = (condition_pipe_start,))
    alpha_task_process.start()
