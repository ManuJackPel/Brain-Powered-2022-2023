"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import random
import time
import math
from pylsl import StreamInfo, StreamOutlet

# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover).
info = StreamInfo('BioSemi', 'EEG', 9, 100, 'float32', 'myuid34234')

# next make an outlet
outlet = StreamOutlet(info)

print("now sending data...")

x=0

while True: 
    # make a new random 8-channel sample; this is converted into a
    # pylsl.vectorf (the data type that is expected by push_sample)
    
    x=x+0.1
    mysample = [math.sin(x), 0, 0,
            0, 0, 0,
            0, 0, 0]
    
    print(mysample)

    # now send it and wait for a bit
    outlet.push_sample(mysample)

