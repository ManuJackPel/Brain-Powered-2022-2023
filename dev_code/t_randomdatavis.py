import random
import numpy as np
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os 
import sys

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes import dataloader, preprocessor

plt.style.use('fivethirtyeight')

channels = ['Fp1', 'Fp2', 'Fc5', 'Fz', 'Fc6', 'T7', 'Cz', 'T8']
n_pulled_samples = 64
dataset = 'GIPSA-lab'
participant = 20

# LOAD DATA
stream = dataloader.DataLoader(dataset, channels, participant)
_data = stream.pull_sample(n_pulled_samples)
x_vals = []
y_vals = []

def animate(i):
    _data = np.append(data, stream.pull_sample(n_pulled_samples))
    x = list(range(round(len(data) - n_pulled_samples/2) , round(len(data) + n_pulled_samples/2)))
    y1 = data[-n_pulled_samples:]

    plt.cla()

    plt.plot(x, y1[:,1], label='Channel 1')
    plt.legend(loc='upper left')


ani = FuncAnimation(plt.gcf(), animate, interval=1/128)

plt.tight_layout()
plt.show()
