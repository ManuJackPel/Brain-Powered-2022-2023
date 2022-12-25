from datetime import datetime
import pandas as pd
import time
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from helper_functions import init_vars, filter_sig, pwelch
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


    # Import vars
    # Fs, time = init_vars()
    # channel = 1 

    # main loop
    data = np.zeros(9)
    looptime = starttime
    while True: 
        # get a new sample
        sample, timestamp = inlet.pull_sample()
        sample = np.array(sample)
        sample = np.ndarray.transpose(sample)
        data = np.column_stack((data, sample))
        # print(sample)

        # # Filter
        # filtered_sample = filter_sig(sample[channel], Fs)
        # # Pwelch
        # power = pwelch(filtered_sample, Fs)
        # # Alpha Mean


        # Check loopstate
        if time.time() - looptime > .3:
            looptime = time.time()
            print('SAVE')
            np.savetxt("data/data.csv", data, delimiter = ",")
            ani = FuncAnimation(plt.gcf(), animate, interval=1000)
            
            # plt.show()
        
        if time.time()-starttime > 100:
            break
       
def animate(i):
    plot_data =  np.array(pd.read_csv('data.csv'))
    x = plot_data[0]

    plt.cla()

    plt.plot(x)
    plt.tight_layout()

if __name__ == '__main__':
    main()
    #task.LoopingCall(main).start(0.00390625)
    #reactor.run()

