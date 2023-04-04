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
from functools import partial

from _code.classes.recorder import make_buffer, update_buffer, Recorder
from _code.classes.dataloader import DataStream


def data_stream(stream_object, recorder_pipe_start, visualizer_pipe_start, condition_pipe_end):
    while True:
        # Check stop condition
        if 'stop_threshold' in condition:
            print('STOP TASK')
        # Pull sample
        sample, timestamp = stream_object.pull_sample()
        # Combine into immutable array
        combined_array = np.array([timestamp] + sample + [condition])
        combined_array.setflags(write=False)
        # Send data to recorder
        recorder_pipe_start.send(combined_array)
        # Send data to visualizer 
        visualizer_pipe_start.send(combined_array)

def record_data_stream(recorder, recorder_pipe_end):
    # Start timer
    start_time = time.time()
    while True:
        # Get stream data
        combined_array = recorder_pipe_end.recv()
        # Append to recorder
        recorder.append(combined_array)
        # Save every n seconds
        if time.time() - start_time >= 0.5:
            start_time = time.time()
            recorder.save()
    
def data_visualization(visualizer_pipe_end, header):
    # Make buffer
    vis_data_buffer = make_buffer(header, buffer_size=1024)

    def animate(i, buffer):
        # Get vis data buffer from outside the function
        global vis_data_buffer
        vis_data_buffer = update_buffer(vis_data_buffer, visualizer_pipe_end.recv())
        # Obtain Channels
        time = buffer[:,0]
        channels = buffer[:,[1,9]]
        # Plot parameters
        plt.cla()
        plt.xlim([buffer[0,0], buffer[-1,0]])
        plt.ylim([-3,3]) 
        plt.plot(time, channels, '--') 

    ani = FuncAnimation(plt.gcf(), animate, interval=500)    
    plt.show()

def get_alpha_task_condition(condition_pipe_start):
    pass
    # while True:
    #     with open('dev_code\psychopy\condition.txt') as f:
    #         condition_file = f.readlines()
    #         condition = condition_file[0]
    #         participant = condition_file[1] # Send data to recorder
    #         condition_pipe_start.send((condition, participant))

    

if __name__ == "__main__":  
    print('\n Initializing DataStream ')
    stream_name = input('What is the name of the LSL stream')
    eeg_stream = DataStream(stream_name)

    print('\n Initializing Recorder')
    header = ['time', 'CH1', 'CH2','CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', 'CH9', 'condition'] 
    file_location = '/home/kibble/Documents/School/Brain Powered/Brain-Powered-2022-2023/data/testing/testing_data_9.csv'
    recorder = Recorder(file_location, header)

    # Init Pipeline, set duplex to False to make it unidirectional
    data_pipe_end, data_pipe_start = Pipe(duplex=False)
    condition_pipe_end, condition_pipe_start = Pipe(duplex=False)

    eeg_stream_process = Process(target = data_stream, args = (data_pipe_start, condition_pipe_end))
    eeg_stream_process.start()

    visualization_process = Process(target = data_visualization, args = (data_pipe_end,))
    visualization_process.start()

    alpha_task_process = Process(target = get_alpha_task_condition, args = (condition_pipe_start,))
    alpha_task_process.start()



