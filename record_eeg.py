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
        # Get condition of task print('recover condition')
        condition, participant = condition_pipe_end.recv()

        # Check stop condition
        if 'stop_threshold' in condition:
            print('STOP TASK')

        # Pull sample
        print('pull_sample')
        sample, timestamp = stream_object.pull_sample()
        # Combine into immutable array
        print('combine arrays')
        combined_array = np.array([timestamp] + sample + [condition])
        combined_array.setflags(write=False)
        # Send data to recorder
        print('send array to recorder')
        recorder_pipe_start.send(combined_array)
        # Send data to visualizer 
        print('send array to visualizer')
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
        if time.time() - start_time >= 0.5:
            start_time = time.time()
            pass
            # recorder.save()
    
def data_visualization(visualizer_pipe_end, header):
    start_time = time.time()
    # Generate initial data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Create figure and axis objects
    fig, ax = plt.subplots()

    # Plot initial data
    line, = ax.plot(x, y)

    # Continuously update the plot
    while True:
        visualizer_pipe_end.recv()
        if time.time() - start_time < 0.5:
            start_time = time.time()
            # Update the data
            x += 0.3
            y = np.sin(x)
            # Update the plot
            line.set_ydata(y)
            # Redraw the plot
            fig.canvas.draw()
        # PLT.pause somehow makes the plot show up
        plt.pause(0.00001)
            

def get_alpha_task_condition(condition_pipe_start):
    while True:
        # TODO: check if file exist else make file
        with open('dev_code/psychopy/condition.txt') as f:
            condition_file = f.readlines()
            condition = condition_file[0]
            participant = condition_file[1] # Send data to recorder
            condition_pipe_start.send((condition, participant))

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

