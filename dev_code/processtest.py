from multiprocessing import Process, Pipe
import numpy as np
import random
import time
from pylsl import StreamInlet, resolve_stream # pylsl for lsl streaming, the streaming technology used by openvibe to stream to python (and other environments)
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

def datastream(vis_in, eye_in):
#Receive incoming data from lsl server and send to other processes through pipe

    # First resolve an EEG stream on the lab network
    print("ls")
    streams = resolve_stream('type', 'EEG')   
    # Create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    
    x=0
    while True:
        #start = time.time()
        x=x+1

        #make the EEG data every time
        data, timestamp  = inlet.pull_sample()
        data = np.zeros(9)

        #send data to pipe
        vis_in.send(np.array(data))
        eye_in.send(np.array(data))
        #end = time.time()
        print(x)
        #if(x>40):
         #   print(1/(end - start))

def data_vis(connection):
# Plot voltage of channel one, received from pipe

    def animate(i):
        # Pull sample from pipe
        sample = connection.recv()
        xs = np.arange(0, sample.shape[0])

        plt.cla()
        plt.plot(xs, sample, '--', label='Channel 1')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=125)    
    plt.show()


def eyestate(connection):
#Parse current eye condition from condition.txt, combine it with the data and save it as .csv

    while True:
        
        #Read condition
        #with open('Psychopy/condition.txt') as f:
        #    condition = f.readlines()
        condition = 1
        #Read sample from pipe and add condition
        gample = np.append(connection.recv(), condition)
        
        #test
        #print(gample)

if __name__ == "__main__":  # confirms that the code is under main function
    
    #declare pipeline, I declare, duplex = False is meant to make the pipe unidirectional
    vis_out, vis_in = Pipe(duplex=False)
    eye_out, eye_in = Pipe(duplex=False)

    datastream_process = Process(target = datastream, args = (vis_in, eye_in))
    datastream_process.start()

    datavis_process = Process(target = data_vis, args = (vis_out,))
    datavis_process.start()

    eyestate_process = Process(target = eyestate, args = (eye_out,))
    eyestate_process.start()

