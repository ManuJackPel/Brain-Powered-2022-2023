
from pylsl import StreamInlet, resolve_stream # pylsl for lsl streaming, the streaming technology used by openvibe to stream to python (and other environments)
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

def datastream(vis_in, eye_in):
#Receive incoming data from lsl server and send to other processes through pipe

    eeg_stream = MobiLab()
    header = ['time', 'CH1', 'CH2','CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', 'CH9'] 
    data_buffer = make_buffer(header, buffer_size=1024)

    start_time = time.time()
    while True:
        start = time.time()
        sample, timestamp = eeg_stream.pull_sample()
        combined_array = np.array([timestamp] + sample)
        data_buffer = update_buffer(data_buffer, combined_array)

        if time.time() - start_time >= 0.5:
            start_time = time.time()
            vis_in.send(data_buffer)
            eye_in.send(sample)

def data_vis(pipe_end):
# Plot voltage of channel one, received from pipe

    def animate(i):
        data_buffer = pipe_end.recv()
        time = data_buffer[:,0]
        channels = data_buffer[:,[1,9]]
        # print(time[-1])

        plt.cla()
        plt.xlim([data_buffer[0,0], data_buffer[-1,0]])
        plt.ylim([-3,3])
        line = plt.plot(time, channels, '--')
        return line,

    ani = FuncAnimation(plt.gcf(), animate, interval=12)    
    plt.show()


def filesave(inputdata):
#Parse current eye condition from condition.txt, combine it with the data and save it as .csv when the condition is 

    data = np.zeros(10)

    while True:
        
        #Read condition
        with open('dev_code\psychopy\Psychopy\condition.txt') as f:
            condition_file = f.readlines()
            condition = condition_file[0]
            participant = condition_file[1]
        
        #Read sample from pipe and add condition as extra column
        sample = np.append(inputdata.recv(), condition)

        print(np.shape(data))

        #Create data
        data = np.vstack((data, sample))
 
        #print data shape
        print(np.shape(data))
        print(condition)

        if 'stop_threshold' in condition:
            print('saving the data')
            f = open('dev_code/psychopy/condition.txt', 'w')
            f.writelines(['saving the data\n', participant])
            f.close()

            np.savetxt(f'{participant}.csv', data, fmt="%s")



if __name__ == "__main__":  # confirms that the code is under main function
    
    #declare pipeline, I declare, duplex = False is meant to make the pipe unidirectional
    vis_out, vis_in = Pipe(duplex=False)
    eye_out, eye_in = Pipe(duplex=False)

    datastream_process = Process(target = datastream, args = (vis_in, eye_in))
    datastream_process.start()

    datavis_process = Process(target = data_vis, args = (vis_out,))
    datavis_process.start()

    filesave_process = Process(target = filesave, args = (eye_out,))
    filesave_process.start()

