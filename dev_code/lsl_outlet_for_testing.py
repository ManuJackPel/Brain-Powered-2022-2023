import time
from pylsl import StreamInfo, StreamOutlet
import math
from datetime import datetime
import numpy as np

def get_time_format():
    time_now = datetime.now()
    minute = time_now.minute * 100
    second = round(time_now.second / 60 * 100)
    mili = round(time_now.microsecond / 10**6, 3)
    return minute + second + mili

if __name__ == "__main__":
    # Create a new stream info with the name 'MyStream', one channel, and a sample rate of 100 Hz
    info = StreamInfo('MyStream', 'MySignal', 3, 512, 'float32', 'bpid12345')

    # Create a new stream outlet with the stream info
    outlet = StreamOutlet(info)

    while True:
        # Generate a sine wave signal
        # sample = [0.5 * math.sin(i / 10.0)]
        time_now = get_time_format()
        
        y = (0.5 * math.sin(time_now) )
        z = (0.5 * math.cos(time_now) )

        outlet.push_sample([time_now, y, z])
        print(time_now)
        time.sleep(1/512)

