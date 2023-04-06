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


def mute_stdout(func):
    def wrapper(*args, **kwargs):
        # Redirect stdout to a null device
        devnull = open(os.devnull, 'w')
        sys.stdout = devnull
        # Call the function
        result = func(*args, **kwargs)
        # Restore stdout
        sys.stdout = sys.__stdout__
        return result
    return wrapper


# @mute_stdout
def data_stream(stream_object, recorder_pipe_start, visualizer_pipe_start, condition_pipe_end):
    while True:
        # Get condition of task print('recover condition')
        condition, participant = condition_pipe_end.recv()

        # Check stop condition
        if 'stop_threshold' in condition:
            print('STOP TASK')

        # Pull sample
        # print('pull_sample')
        sample, timestamp = stream_object.pull_sample()
        # Combine into immutable array
        # print('combine arrays')
        combined_array = np.array([timestamp] + sample + [condition])
        combined_array.setflags(write=False)
        # Send data to recorder
        # print('send array to recorder')
        recorder_pipe_start.send(combined_array)
        # Send data to visualizer 
        # print('send array to visualizer')
        visualizer_pipe_start.send(combined_array)

def record_data_stream(recorder, recorder_pipe_end):
    # Start timer
    start_time = time.time()
    while True:
        # Get stream data
        combined_array = recorder_pipe_end.recv()
        # Append to recorder
        recorder.append_data(combined_array)
        # Save every n seconds
        print(combined_array[0])
        if time.time() - start_time >= 0.5:
            start_time = time.time()
            pass
            # recorder.save()
    
def data_visualization(visualizer_pipe_end, header):
    # Init buffer
    buffer_size = 1024
    plot_buffer = make_buffer(header, buffer_size)
    # Create figure and axis objects
    fig, ax = plt.subplots()
    line, = ax.plot(np.zeros(buffer_size), np.zeros(buffer_size))

    # Continuously update the plot
    start_time = time.time()
    while True:
        # Update buffer 
        plot_buffer = update_buffer(plot_buffer, visualizer_pipe_end.recv())
        if time.time() - start_time > 1:
            # Reset timer
            start_time = time.time()
            # Get time and channel
            time_ch = plot_buffer[:, 0]
            volt_ch = plot_buffer[:, 1] # Get first and second electrode
            condition_ch = plot_buffer[:, -1]
            # Update the plot
            line.set_xdata(time_ch)
            line.set_ydata(volt_ch)
            # Redraw the plot
            plt.ylim([-0.1,0.1])
            plt.xlim([time_ch[0], time_ch[-1]])
            fig.canvas.draw()
        # PLT.pause somehow makes the plot show up
        plt.pause(0.000000000000000000000000000000000000001)
            

def get_alpha_task_condition(condition_pipe_start):
    # TODO: check if file exist else make file
    with open('dev_code/psychopy/condition.txt') as f:
        while True:
            condition_file = f.readlines()
            # print('file: ', end='')
            # print(condition_file)
            condition = condition_file[0]
            participant = condition_file[1] # Send data to recorder
            condition_pipe_start.send((condition, participant))
            # Set file cursor back at start of file
            f.seek(0)

if __name__ == "__main__":  
    # stream_name = input('What is the name of the LSL stream: ')
    stream_name = 'mobilab'
    print('\nInitializing DataStream... ')
    eeg_stream = DataStream(stream_name)

    print('\nInitializing Recorder')
    header = ['time', 'CH1', 'CH2','CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', 'CH9', 'condition'] 
    file_location = '/home/kibble/Documents/School/Brain Powered/Brain-Powered-2022-2023/data/testing/testing_data_9.csv'
    recorder = Recorder(file_location, header)

    # Init Pipeline, set duplex to False to make it unidirectional
    recorder_pipe_end, recorder_pipe_start = Pipe(duplex=False)
    visualizer_pipe_end, visualizer_pipe_start = Pipe(duplex=False)
    condition_pipe_end, condition_pipe_start = Pipe(duplex=False)

    data_stream_process = Process(target=data_stream, args=(eeg_stream, recorder_pipe_start, visualizer_pipe_start, condition_pipe_end))
    recorder_process = Process(target=record_data_stream, args=(recorder, recorder_pipe_end))
    visualization_process = Process(target=data_visualization, args=(visualizer_pipe_end, header))
    alpha_task_process = Process(target = get_alpha_task_condition, args = (condition_pipe_start,))

    data_stream_process.start()
    recorder_process.start()
    visualization_process.start()
    alpha_task_process.start()

