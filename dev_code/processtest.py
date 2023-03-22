from multiprocessing import Process, Pipe
import numpy as np
import random
import time
from pylsl import StreamInlet, resolve_stream # pylsl for lsl streaming, the streaming technology used by openvibe to stream to python (and other environments)
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def datastream(connection):
    # First resolve an EEG stream on the lab network
    print("ls")
    streams = resolve_stream('type', 'EEG')   
    # Create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])


    while True:
        
        #make the EEG data every time
        data, timestamp  = inlet.pull_sample()
        time.sleep(1/256)

        #send data to pipe
        connection.send(np.array(data))

        #print parallel process
        print('parallellepipidum')

def data_vis(connection):
    def animate(i):
        # Pull sample from pipe
        sample = connection.recv()
        xs = np.arange(0, sample.shape[0])

        plt.cla()
        plt.plot(xs, sample, '--', label='Channel 1')
        plt.tight_layout()

    ani = FuncAnimation(plt.gcf(), animate, interval=125)    
    plt.show()



if __name__ == "__main__":  # confirms that the code is under main function
    
    


    #declare pipeline, I declare
    conn1, conn2 = Pipe()

    datastream_process = Process(target=datastream, args = (conn2,))
    datastream_process.start()

    datavis_process = Process(target = data_vis, args = (conn1,))
    datavis_process.start()


