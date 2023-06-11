import numpy as ntrial
from pylsl import StreamInlet, resolve_stream
from multiprocessing import Process, Queue
from collections import deque
import time
import numpy as np


from classifiers import detect_blinks

SAMPLE_FREQ_HZ = 250
BUFFER_MEMORY_SEC = 2
BUFFER_SIZE = SAMPLE_FREQ_HZ * BUFFER_MEMORY_SEC


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
            # print()
            # print(f'Queue size reader before: {queue.qsize()}')
            queue.put(data)
            # print(f'Queue size reader after: {queue.qsize()}')

            elapsed_time = time.time()
            
def classify_data(queue):
    def get_Fp1_channel(trial: np.ndarray):
        return trial[:, 0]
    drone_movement_axis = 'front-back'

    while True:
        # Checkif Queue is not empty
        if queue.qsize() > 0:
            # Determine the number of eyeblinks
            queue.get()
            trial = get_Fp1_channel(np.array(queue.get()))
            num_eyeblinks = np.sum(detect_blinks(trial, std_dev=2))
            
            # Switch drone movement between front-back and left-right
            if num_eyeblinks >= 3: 
                drone_movement_axis = 'front-back' if drone_movement_axis == 'left-right' else 'left-right'
                print(f'Drone is moving {drone_movement_axis}')

def main():
    streams = resolve_stream('name', 'Brandon Stream')
    inlet = StreamInlet(streams[0])

    # Create a queue for communication between the processes
    queue = Queue(maxsize=5)

    # Create the processes
    p1 = Process(target=acquire_data, args=(queue, inlet))
    p2 = Process(target=classify_data, args=(queue, ))

    # Start the processes
    p1.start()
    p2.start()

    # # Wait for the processes to finish
    # p1.join()
    # p2.join()

if __name__ == "__main__":
    main()

