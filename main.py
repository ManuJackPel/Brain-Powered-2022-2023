from datetime import datetime
import time
import numpy as np
import matplotlib as plt
from pylsl import StreamInlet, resolve_stream # pylsl for lsl streaming, the streaming technology used by openvibe to stream to python (and other environments)

def main():

    # First resolve an EEG stream on the lab network
    print("ls")
    streams = resolve_stream('type', 'EEG')
   
    # Create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    # Measure starting time
    starttime = time.time()
    print(starttime)

    # main loop
    data = np.zeros(9)
    #while True: 
    for i in range(10000):
        # get a new sample
        sample, timpesta = inlet.pull_sample()
        
        #Onderstaande line doet pull_samnple() maar zonder te wachten op een nieuwe sample. 
        #Voor volgende keer testen of hij dan niet meer synchroon loopt met de datastream
        #sample, timestamp = inlet.pull_sample(timeout = 0.0)
        
        sample = np.array(sample)
        data = np.column_stack((data, sample))
        print(data.shape)
 
        print(len(data))
        np.savetxt("data.csv", data, delimiter = ",")
        


      
if __name__ == '__main__':
    main()
    #task.LoopingCall(main).start(0.00390625)
    #reactor.run()
