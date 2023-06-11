import time
import random
import multiprocessing
import matplotlib.pyplot as plt
from collections import deque

def manage_data(queue, max_length, shared_list, lock):
    while True:
        if queue.qsize() >= max_length:
            queue.get()
        # Simulate incoming data
        new_data = random.uniform(0, 10)
        queue.put(new_data)
        with lock:
            if len(shared_list) >= max_length:
                shared_list.pop(0)
            shared_list.append(new_data)
        time.sleep(0.1)  # simulate delay

def plot_data(shared_list, lock):
    plt.ion()  # Interactive mode on
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    while True:
        if len(shared_list) > 0:
            with lock:
                data = list(shared_list)
            line.set_ydata(data)
            line.set_xdata(range(len(data)))
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.1)  # prevent high CPU usage

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        queue = multiprocessing.Queue()
        shared_list = manager.list()
        lock = multiprocessing.Lock()
        max_length = 1000

        data_manager = multiprocessing.Process(target=manage_data, args=(queue, max_length, shared_list, lock))
        data_plotter = multiprocessing.Process(target=plot_data, args=(shared_list, lock))

        data_manager.start()
        data_plotter.start()

        data_manager.join()
        data_plotter.join()

