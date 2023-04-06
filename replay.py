import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
import tkinter.filedialog as fd

file_path = fd.askopenfilename()
eeg = pd.read_csv(file_path)


sfreq = 256 # sampling frequency
visible = 2000 # time shown in plot (in samples) --> 4 seconds

# initialize deques 
dy1 = deque(np.zeros(visible), visible)
dx = deque(np.zeros(visible), visible)

# get interval of entire time frame 
interval = np.linspace(0, eeg.shape[0], num=eeg.shape[0])
interval /= sfreq # from samples to seconds

print(eeg.head())

# define channels to plot
ch1 = 'CH1'

# define figure size
fig = plt.figure(figsize=(20,12))

# define axis1, labels, and legend
ah1 = fig.add_subplot(211)
ah1.set_ylabel("Voltage [\u03BCV]", fontsize=14)
l1, = ah1.plot(dx, dy1, color='rosybrown', label=ch1)
ah1.legend(loc="upper right", fontsize=12, fancybox=True, framealpha=0.5)

start = 0
plt.ion()
while start+visible <= eeg.shape[0]: 
    print('started loop')
    # extend deques (both x and y axes)
    dy1.extend(eeg[ch1].iloc[start:start+visible])
    dx.extend(interval[start:start+visible])

    # update plot 
    l1.set_ydata(dy1)  
    l1.set_xdata(dx)

    # set x- and y-limits based on their mean
    ah1.set_ylim(-0.5, 0.5)
    ah1.set_xlim(interval[start], interval[start+visible])

    # control speed of moving time-series
    start += 100

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.0001)
