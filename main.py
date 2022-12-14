from datetime import datetime
<<<<<<< HEAD
import numpy as np
from pylsl import StreamInlet, resolve_stream

def main():
    # Resolve an EEG stream on the lab network
=======
import time
import numpy as np

# pylsl for lsl streaming, the streaming technology used by openvibe to stream to python (and other environments)
from pylsl import StreamInlet, resolve_stream

# twisteds loopingcall is used to synchronize python loops
from twisted.internet import task
from twisted.internet import reactor

#import classes.insertclasshere

#define main loop
def main():

    # first resolve an EEG stream on the lab network
>>>>>>> 85a9b13460e218918cc4eb92b4ae07ad82106721
    print("ls")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

<<<<<<< HEAD
    # Init Classifier
=======
    #measure starting time
    starttime = time.time()
    print(starttime)
>>>>>>> 85a9b13460e218918cc4eb92b4ae07ad82106721

    # main loop
    data = np.zeros(9)
    while True: 
        # get a new sample
        sample, timestamp = inlet.pull_sample()
        sample = np.array(sample)
<<<<<<< HEAD
        print(sample)    
        # Pass Data to Pipeline
        # Send Command To Drone
        
       
# start main loop
if __name__ == '__main__':
    main()
=======
        data = np.vstack((data, sample))
        #print(data)
        print(sample, timestamp)
        np.savetxt("data.csv", data, delimiter = ",")
        
        #check loopstate
        if time.time()-starttime > 2:
            print("stop")
            break
       
# start main loop
if __name__ == '__main__':
    #main()
    task.LoopingCall(main).start(1.0)
    #reactor.run()
>>>>>>> 85a9b13460e218918cc4eb92b4ae07ad82106721
