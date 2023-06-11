import matplotlib.pyplot as plt
import pylsl
from collections import deque
import subprocess
import multiprocessing as mp
import signal

WINDOW_SIZE = 100
parent_should_wait_on_child = False

def pull_data(inlet, data_queue):
    while True:
        sample, timestamp = inlet.pull_sample()
        data_queue.put(sample)

def plot_data(data_queue):
    plt.ion()  # enable interactive plotting
    fig, ax = plt.subplots()

    data = deque(maxlen=1250)

    while True:
        while not data_queue.empty():
            sample = data_queue.get()
            data.append(sample)

        ax.clear()
        ax.plot(data)
        plt.pause(1/250)


if __name__ == "__main__":
    streams = pylsl.resolve_stream('name', 'Brandon Stream')  # replace 'Name' with your data LSL stream name
    inlet = pylsl.StreamInlet(streams[0])

    data_queue = mp.Queue()

    pull_process = mp.Process(target=pull_data, args=(inlet, data_queue))
    plot_process = mp.Process(target=plot_data, args=(data_queue,))

    pull_process.start()
    plot_process.start()

    plt.show()



