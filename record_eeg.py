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

from _code.classes.recorder import make_buffer, update_buffer
from _code.classes.dataloader import MobiLab



def data_stream(pipe_start):
    eeg_stream = MobiLab()
    header = ['CH1', 'CH2','CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', 'CH9'] 
    data_buffer = make_buffer(header, buffer_size=64)
    
    start_time = time.time()
    while True:
        sample, timestamp = eeg_stream.pull_sample()
        data_buffer = update_buffer(data_buffer, np.array(sample))
        pipe_start.send(data_buffer)

        
def data_visualization(pipe_end):
    def animate(i):
        # Pull sample from pipe
        received_data = pipe_end.recv()
        xs = np.arange(0, received_data.shape[0])

        plt.cla()
        plt.plot(xs, received_data, '--', label='Channel 1')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=125)    
    plt.show()


if __name__ == "__main__":  
    # Init Pipeline, set duplex to False to make it unidirectional
    conn1, conn2 = Pipe(duplex=False)

    eeg_stream_process = Process(target = data_stream, args = (conn2,))
    eeg_stream_process.start()

    visualization_process = Process(target = data_visualization, args = (conn1,))
    visualization_process.start()

