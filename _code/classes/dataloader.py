"Class for choosing what data to import into the classification progam"

import os 
import scipy 
import numpy as np 
import matplotlib.pyplot as plt
import time
from pylsl import StreamInlet, resolve_stream

class DataStream:
    def __init__(self, name):
        # Resolve EEG stream on lab networ
        if name == 'mobilab':
            streams = resolve_stream('type', 'EEG')
        else:
            streams = resolve_stream('name', 'dummy_sinewave')
        # Create a new inlet to read from 
        self.inlet = StreamInlet(streams[0])

    def pull_sample(self):
        return self.inlet.pull_sample()
        
