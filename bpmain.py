#-----------------------------------------------------
#IMPORT LIBRARIES
#-----------------------------------------------------
from datetime import datetime

import numpy as np

from pylsl import StreamInlet, resolve_stream






#-----------------------------------------------------
#MAIN LOOP
#-----------------------------------------------------

#define main loop
def main():
        
    # first resolve an EEG stream on the lab network
    print("ls")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    # main loop
    while True:
        # get a new sample
        sample, timestamp = inlet.pull_sample()
        sample = np.array(sample)
        print(sample)    
       
# start main loop
if __name__ == '__main__':
    main()