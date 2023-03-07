from multiprocessing import Process, Pipe
import multiprocessing
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

from _code.classes import dataloader, preprocessor

def datastream(connection, pipeline):
    # Sample Parameters
    channels = ['Fp1', 'Fp2', 'Fc5', 'Fz', 'Fc6', 'T7', 'Cz', 'T8']
    pull_interval = 0.25 # Time between samples pulled
    stream_hz = 256 # Current setup always runs at 256 Hz
    n_samples_pulled = int(stream_hz * pull_interval) # N samples gotten per pull

    # DataSet parameters
    dataset = 'GIPSA-lab'
    participant = 0
    channel = 0

    # LOAD DATA
    stream = dataloader.DataLoader(dataset, channels, participant)
    samp_data = stream.pull_sample(n_samples_pulled)

    # Init Data Buffer and Count for Amount of Samples Pulled and pipeline
    data_buffer = np.zeros(1024 * 5)
    assert n_samples_pulled < data_buffer.shape[0], "Sample pull size is larger then sample buffer size"
    pull_iters = 0
    pre_process, extract_features, classify, classifcation_size = pipeline


    while True:
        output = stream.pull_sample(n_samples_pulled)
        assert output.shape[0] == n_samples_pulled
        output = output[:, channel] # change this in GIPSA-lab code
        
        data_buffer = update_buffer(data_buffer, output)

        # Send data to pipe
        connection.send(data_buffer)

        pull_iters += 1
        if pull_iters * n_samples_pulled == classification_size:
            pull_iters = 0
            # PRE-PROCESS
            pp_data = pre_process(data_buffer)
            # FEATURE EXTRACTION
            fe_data = extract_features(pp_data)
            # CLASSIFER
            _class = classify(fe_data)

def data_vis(connection):
    def animate(i):
        # Pull sample from pipe
        sample = connection.recv()
        xs = np.arange(0, sample.shape[0])

        plt.cla()
        plt.plot(xs, sample, '--', label='Channel 1')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=125)    
    plt.show()
  
def update_buffer(buffer, new_sample):
    """
    Removes older sample from start whilst adding newer sample to an end, buffer size stays consistent
    Returns immutable array
    """
    buffer.setflags(write=True) # Make buffer unwriteable
    samp_len = new_sample.shape[0]
    buffer = np.roll(buffer, -samp_len)
    buffer[-samp_len:] = new_sample
    buffer.setflags(write=False) # Make buffer writeable
    return buffer

if __name__ == "__main__":  
    # Init Pipeline, set duplex to False to make it unidirectional
    conn1, conn2 = Pipe(duplex=False)

    datastream_process = Process(target = datastream, args = (conn2,pipeline))
    datastream_process.start()

    datavis_process = Process(target = data_vis, args = (conn1,))
    datavis_process.start()




