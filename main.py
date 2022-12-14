from datetime import datetime
import time
import numpy as np

# pylsl for lsl streaming, the streaming technology used by openvibe to stream to python (and other environments)
from pylsl import StreamInlet, resolve_stream

# twisteds loopingcall is used to synchronize python loops
from twisted.internet import task
from twisted.internet import reactor

#define main loop
def main():

    # first resolve an EEG stream on the lab network
    print("ls")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    #measure starting time
    starttime = time.time()
    print(starttime)

    # main loop
    data = np.zeros(9)
    while True: 
        # get a new sample
        sample, timestamp = inlet.pull_sample()
        
        #Onderstaande line doet pull_samnple() maar zonder te wachten op een nieuwe sample. Voor volgende keer testen of hij dan niet meer synchroon loopt met de datastream
        #sample, timestamp = inlet.pull_sample(timeout = 0.0)
        
        sample = np.array(sample)
        data = np.hstack((data, sample))
        #print(data)
        print(sample, timestamp)
        #np.savetxt("data.csv", data, delimiter = ",")
        
        #check loopstate
        if time.time()-starttime > 10:
            print(len(data))
            np.savetxt("data.csv", data, delimiter = ",")
            break
       
# start main loop
if __name__ == '__main__':
    main()
    #task.LoopingCall(main).start(0.00390625)
    #reactor.run()
