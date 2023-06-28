from pylsl import StreamInlet, resolve_stream
from multiprocessing import Process, Queue
from collections import deque
import time
import numpy as np
import sys
import sklearn

from _code.classifiers import detect_blinks, butter_bandpass_filter
from _code.data_import import import_csv

SAMPLE_FREQ_HZ = 250
BUFFER_MEMORY_SEC = 2
BUFFER_SIZE = SAMPLE_FREQ_HZ * BUFFER_MEMORY_SEC

def main():
    """Main"""
    # streams = resolve_stream('name', 'Brandon Stream')
    # inlet = StreamInlet(streams[0])

    # Create a queue for communication between the processes
    queue = Queue(maxsize=5)

    # Import Training Data
    task_data_dir = '../eventide_data/base_report.csv'
    raw_data_dir = '../eventide_data/raw_data.csv'
    task_data, task_condition = import_csv(task_data_dir, raw_data_dir)

    # Turn task_data into a list
    task_data = np.array(list(task_data.values()))
    features = np.mean(task_data, axis=1)
    clf = sklearn.svm.SVC()
    clf.fit(features, labels)

    exit()

    # Filter the DataFrame based on conditions
    for condition in conditions:
        column, value = condition
        data = data[data[column] == value]

    # Assume that the target column is 'target' and all other columns are features
    features = data.drop('target', axis=1)
    target = data['target']


    

    # Prepare CSP
    csp = CSP(training_data)
     
    

    # Create the processes
    p1 = Process(target=acquire_data, args=(queue, inlet))
    p2 = Process(target=classify_data, args=(queue, ))

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
            
def classify_data(queue, classifier, csp):
    get_Fp1_channel = lambda trial: trial[:, 0]
    drone_movement_axis = 'front-back'
    results_queue = deque(maxlen=5)

    while True:
        # Check if queue has trial
        if queue.qsize() > 0:
            start_time = time.time()
            trial = queue.get()
            # Determine the number of eyeblinks
            eog_trial = get_Fp1_channel(trial)
            num_eyeblinks = np.sum(detect_blinks(eog_trial, std_dev=2))
            
            # Switch drone movement between front-back and left-right
            if num_eyeblinks >= 3: 
                drone_movement_axis = 'front-back' if drone_movement_axis == 'left-right' else 'left-right'
                print(f'Drone is moving {drone_movement_axis}')

            trial_filt = butter_bandpass_filter(trial, 8, 15, SAMPLE_FREQ_HZ, order=1) # 
            trial_csp = csp.apply(trial_filt)
            trial_logvar = np.log(np.var(trial_csp, axis=1))
            
            # Get result and append to queue
            result = classifier(trial_logvar)
            results_queue.append(result)

            # If all results are the same send the command to drone
            if results_queue.count(results_queue[0]) == len(results_queue):
                send_command_to_drone(result)
                print(f'Drone Command :{result}')

            print(f'Classification Duration: {time.time() - start_time}')
            print(f'Queue Size: {queue.qsize()}')
            print()

def send_command_to_drone(command):
    pass

if __name__ == "__main__":
    main()
