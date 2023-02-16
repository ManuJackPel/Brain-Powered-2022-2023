from multiprocessing import Process, Pipe
import multiprocessing
import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os 
import sys
import numpy as np
import time

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes import dataloader, preprocessor

def update_buffer(buffer, new_sample):
    """
    Removes older sample whilst adding newer sample, buffer size stays consistent
    Returns immutable array
    """
    buffer.setflags(write=True)
    samp_len = new_sample.shape[0]
    buffer = np.roll(buffer, samp_len)
    buffer[-samp_len:] = new_sample
    buffer.setflags(write=False)
    return buffer

def datastream(connection):
    # Sample Parameters
    channels = ['Fp1', 'Fp2', 'Fc5', 'Fz', 'Fc6', 'T7', 'Cz', 'T8']
    stream_hz = 256 # Code always works in 256 
    pull_interval = 0.25 # Time between samples pulled
    n_samples_pulled = int(stream_hz * pull_interval) # N samples gotten per pull

    # DataSet parameters
    dataset = 'GIPSA-lab'
    participant = 0

    # Pipeline Parameters
    classification_size = 1024
    assert (classification_size % n_samples_pulled) == 0

    # LOAD DATA
    stream = dataloader.DataLoader(dataset, channels, participant)
    samp_data = stream.pull_sample(n_samples_pulled)


    data_buffer = np.zeros(classification_size)
    assert n_samples_pulled < data_buffer.shape[0], "Sample pull size is larger then sample buffer size"
    pull_iters = 0
    while True:
        output = stream.pull_sample(n_samples_pulled)
        output = output[participant] # change this in GIPSA-lab code
        
        data_buffer = update_buffer(data_buffer, output)

        # Send data to pipe
        connection.send(data_buffer)

        pull_iters += 1
        print(pull_iters * n_samples_pulled)
        if pull_iters * n_samples_pulled == classification_size:
            print(data_buffer)
            pull_iters = 0
            pass

            # PRE-PROCESS
            # FEATURE EXTRACTION
            # CLASSIFER

def data_vis(connection):
    def animate(i):
        # Pull sample from pipe
        sample = connection.recv()
        xs = np.arange(0, sample.shape[0])

        plt.cla()
        plt.plot(xs, sample, '--', label='Channel 1')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=1)    
    plt.show()
  

if __name__ == "__main__":  # confirms that the code is under main function
    
    # Init Pipeline, set duplex to False to make it unidirectional
    conn1, conn2 = Pipe(duplex=False)
    print('Init Pipe')

    datastream_process = Process(target = datastream, args = (conn2,))
    datastream_process.start()
    print('Started Datastream')

    datavis_process = Process(target = data_vis, args = (conn1,))
    datavis_process.start()
    print('Started Datavis')




