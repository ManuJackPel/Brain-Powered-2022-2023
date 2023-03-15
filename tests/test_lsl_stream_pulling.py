from multiprocessing import Process, Pipe
import time
import multiprocessing
from pylsl import resolve_stream, StreamInlet
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import sys
import os

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes.recorder import update_buffer, make_buffer

# Visual Tests
def data_stream(pipe_start):
    # Resolve Stream 
    streams = resolve_stream('name', 'MyStream')
    inlet = StreamInlet(streams[0])
    data_buffer = make_buffer(['time', 'CH1', 'CH2'], 1024)

    start_time = time.time()
    while True:
        sample, timestamp = inlet.pull_sample()
        data_buffer = update_buffer(data_buffer, np.array(sample))

        if time.time() - start_time >= 1:
            start_time = time.time()
            print(data_buffer[-1][0])
            pipe_start.send(data_buffer)



def data_visualization(pipe_end):
    #     data_buffer = pipe_end.recv()
    # while True:

    #     if data_buffer[0][0] < 125:
    #         print('\n================\n')
    #     print(data_buffer)

    def animate(i):
        data_buffer = pipe_end.recv()
        time = data_buffer[:,0]
        channels = data_buffer[:,[1,2]]
        # print(time[-1])

        plt.cla()
        plt.xlim([data_buffer[0,0], data_buffer[-1,0]])
        plt.ylim([-3,3])
        plt.plot(time, channels, '*')
        # plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=125)    
    plt.show()


if __name__ == "__main__":  
    # Init Pipeline, set duplex to False to make it unidirectional
    conn1, conn2 = Pipe(duplex=False)

    eeg_stream_process = Process(target = data_stream, args = (conn2,))
    eeg_stream_process.start()

    visualization_process = Process(target = data_visualization, args = (conn1,))
    visualization_process.start()

