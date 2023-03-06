import os 
import sys
import numpy as np
import time
from tkinter import filedialog as fd

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes import recorder
from _code.classes.dataloader import MobiLab

def main():
    stream = MobiLab()
    while True:
        print(stream.pull_sample())

    # file_name = fd.askopenfilename()
    # header = None
    # record  = recorder.Recorder(file_name, header)
    
    # output = stream.pull_sample(n_samples_pulled)
    # output = output # change this in GIPSA-lab code
    # record.append_data(output)


main()


