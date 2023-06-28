from pylsl import StreamInlet, resolve_stream
from multiprocessing import Process, Queue
from collections import deque
import time
import numpy as np
import sys
import sklearn
from sklearn.neighbors import KNeighborsClassifier
from scipy.signal import butter, sosfiltfilt
import socket

from get_training_data import get_filtered_matrices
from _code.classifiers import detect_blinks, butter_bandpass_filter
from _code.data_import import import_csv
from _code.feature_extraction import CSP

SAMPLE_FREQ_HZ = 250
BUFFER_MEMORY_SEC = 2
BUFFER_SIZE = SAMPLE_FREQ_HZ * BUFFER_MEMORY_SEC
cl1 = 'left'
cl2 = 'right'

# get local machine name (replace with your manually set IP)
host = "192.168.4.20" 
port = 9999

def bandpass(x):
    return sosfiltfilt(sos, x)

def main():
    """Main"""

    # Load data
    bandpassed_data = get_filtered_matrices()
    # Fit the CSP
    csp = CSP(bandpassed_data[cl1], bandpassed_data[cl2])
    csp_data  = {cl1: csp(bandpassed_data[cl1]), 
                 cl2: csp(bandpassed_data[cl2])}
    # Only select last first and last components
    comp = np.array([0, -1])
    comp_data = {cl1 : csp_data[cl1][comp,:,:],
                 cl2: csp_data[cl2][comp,:,:]}
    # Calculate the log-var
    logvar_data = {cl1 : np.log(np.var(comp_data[cl1], axis=1)),
                        cl2: np.log(np.var(comp_data[cl2], axis=1))}

    # Fit data
    train_data = np.transpose(np.concatenate((logvar_data[cl1], logvar_data[cl2]), axis=1))
    train_labels = np.concatenate((np.zeros(logvar_data[cl1].shape[1]), np.ones(logvar_data[cl2].shape[1])))
    
    clf = KNeighborsClassifier(n_neighbors=3)
    clf.fit(train_data, train_labels)

    # Load inlet
    streams = resolve_stream('name', 'Brandon Stream')
    inlet = StreamInlet(streams[0])

    # Create a queue for communication between the processes
    data_queue = Queue(maxsize=5)

    # Create the processes
    p1 = Process(target=acquire_data, args=(data_queue, inlet))
    p2 = Process(target=classify_data, args=(data_queue, clf, csp))

    # Start the processes
    p1.start()
    p2.start()

    # # Wait for the processes to finish
    # p1.join()
    # p2.join()



def acquire_data(queue, inlet):
    # Set up a deque to store the last 5 seconds of data
    data_buffer = deque(maxlen=BUFFER_SIZE)
    elapsed_time = time.time()

    while True:
        # Get a new sample
        sample, timestamp = inlet.pull_sample()
        # Append the sample to the data buffer
        data_buffer.append(sample)

        # Check if we have enough data
        if len(data_buffer) == BUFFER_SIZE and (time.time() - elapsed_time) > 1.0:
            data = np.array(data_buffer)
            queue.put(data)

            elapsed_time = time.time()
            
def classify_data(queue, clf, csp):
    get_Fp1_channel = lambda trial: trial[:, 0]
    drone_movement_axis = 'front-back'
    results_queue = deque(maxlen=5)
    sos = butter(N=2, Wn=[8, 15], btype='band', fs=250, output='sos')

    # def connect():
    #     # create a socket object
    #     global serversocket
    #     serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #     # bind to the port
    #     serversocket.bind((host, port))
            
    #     # queue up to 5 requests
    #     serversocket.listen(5)

    #     # establish a connection
    #     global clientsocket
    #     clientsocket, addr = serversocket.accept()

    #     print("Got a connection from %s" % str(addr))

    #     global msg
    #     msg = 'Thank you for connecting'+ "\r\n"
    # connect()

    while True:
        # Check if queue has trial
        if queue.qsize() > 0:
            start_time = time.time()
            trial = queue.get()
            
            # Filter
            trial_filt = sosfiltfilt(sos, trial)
            # CSP
            trial_csp = csp(trial_filt)
            # Logvar
            trial_logvar = np.log(np.var(trial_csp, axis=1))
            # Classify
            result = clf.predict(trial_logvar)
            results_queue.append(result)
            # If all results are the same send the command to drone
            if results_queue.count(results_queue[0]) == len(results_queue):
                pass
                # try:
                #     clientsocket.send(repr(results).encode('ascii'))

                # except ConnectionResetError:
                #     print('Client got me shy. Reconnecting now.')
                #     connect()

                
            print(f'Drone Command :{result}')
            print(f'Classification Duration: {time.time() - start_time}')
            print(f'Queue Size: {queue.qsize()}')
            print()


if __name__ == "__main__":
    main()
