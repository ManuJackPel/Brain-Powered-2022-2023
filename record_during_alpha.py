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

from _code.classes.recorder import make_buffer, update_buffer
from _code.classes.dataloader import MobiLab



def data_stream(pipe_start):
    eeg_stream = MobiLab()
    header = ['time', 'CH1', 'CH2','CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', 'CH9'] 
    data_buffer = make_buffer(header, buffer_size=1024)

    start_time = time.time()
    while True:
        sample, timestamp = eeg_stream.pull_sample()
        combined_array = np.array([timestamp] + sample)
        data_buffer = update_buffer(data_buffer, combined_array)

        if time.time() - start_time >= 0.5:
            start_time = time.time()
            pipe_start.send(data_buffer)

def data_visualization(pipe_end):
    def animate(i):
        data_buffer = pipe_end.recv()
        time = data_buffer[:,0]
        channels = data_buffer[:,[1,9]]
        # print(time[-1])

        plt.cla()
        plt.xlim([data_buffer[0,0], data_buffer[-1,0]])
        plt.ylim([-3,3])
        plt.plot(time, channels, '--')

    ani = FuncAnimation(plt.gcf(), animate, interval=125)    
    plt.show()



if __name__ == "__main__":  
    # Init Pipeline, set duplex to False to make it unidirectional
    conn1, conn2 = Pipe(duplex=False)

    eeg_stream_process = Process(target = data_stream, args = (conn2,))
    eeg_stream_process.start()

    visualization_process = Process(target = data_visualization, args = (conn1,))
    visualization_process.start()
