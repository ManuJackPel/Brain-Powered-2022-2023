
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

def datastream(eye_in):
#Receive incoming data from lsl server and send to other processes through pipe

    eeg_stream, start_time = MobiLab(), time.time()

    while True:
        sample, timestamp = eeg_stream.pull_sample()
        combined_array = np.array([timestamp] + sample)

        #Send 256 packets per second
        if time.time() - start_time >= (0.00390625):
            print(round(1/(time.time() - start_time), 1))
            start_time = time.time()

            eye_in.send(sample)
            #vis_in.send(combined_array)

# def data_vis(pipe_end):
# # Plot voltage of channel one, received from pipe

#     #data setup
#     header = ['time', 'CH1', 'CH2','CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', 'CH9'] 
#     global data_buffer
#     data_buffer, combined_array = make_buffer(header, buffer_size=1024), pipe_end.recv()

#     # First set up the figure, the axis, and the plot element we want to animate    
#     fig = plt.figure()
#     ax = plt.axes(xlim=[0, 1024], ylim=[-1,1])
#     line, = ax.plot([], [], lw=2)

#     # initialization function: plot the background of each frame
#     def init():
#         line.set_data([],[])
#         return line,

#     # animation function.  This is called sequentially
#     def animate(i):
        
#         #setup data
#         global data_buffer
#         combined_array = pipe_end.recv()        
#         data_buffer = update_buffer(data_buffer, combined_array)
#         time = range(1024)
#         channels = data_buffer[:,1]
        
#         #push data to graph
#         line.set_data(time, channels)
#         return line,

#     # call the animator.  blit=True means only re-draw the parts that have changed.
#     ani = FuncAnimation(fig, animate, init_func=init, interval=(1/60), blit=False)    
#     plt.show()


def filesave(inputdata):
#Parse current eye condition from condition.txt, combine it with the data and save it as .csv when the condition is 

    data = np.zeros(10)

    while True:
        
        #Read condition
        with open('dev_code\psychopy\condition.txt') as f:
            condition_file = f.readlines()
            condition = condition_file[0]
            participant = condition_file[1]
        
        #Read sample from pipe and add condition as extra column
        sample = np.append(inputdata.recv(), condition)

        #Create data
        data = np.vstack((data, sample))
 
        #print data shape
        #print(f"acquiring data from {participant}")
        #print(np.shape(data))
        #print(f"current state is {condition}")
        

        if 'stop_threshold' in condition:
            print('saving the data')
            f = open('dev_code/psychopy/condition.txt', 'w')
            f.writelines(['saving the data\n', participant])
            f.close()

            np.savetxt(f'{participant}.csv', data, fmt="%s")

            f = open('dev_code/psychopy/condition.txt', 'w')
            f.writelines(['previous data has been saved\n', 'no current participant'])
            f.close()

            # Exit message and quit
            print(f"data saved for {participant}, exiting now")
            quit()



if __name__ == "__main__":  # confirms that the code is under main function
    
    #declare pipeline, I declare, duplex = False is meant to make the pipe unidirectional
    #vis_out, vis_in = Pipe(duplex=False)
    eye_out, eye_in = Pipe(duplex=False)

    datastream_process = Process(target = datastream, args = (eye_in,))
    datastream_process.start()

    #datavis_process = Process(target = data_vis, args = (vis_out,))
    #datavis_process.start()

    filesave_process = Process(target = filesave, args = (eye_out,))
    filesave_process.start()

