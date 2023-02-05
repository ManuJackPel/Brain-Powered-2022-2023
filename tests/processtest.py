from multiprocessing import Process, Pipe
import multiprocessing
import numpy as np
import random
import time
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#multiprocessing.freeze_support()



def datastream(connection):
    iterationnumber = 0
    while True:
        
        #make the EEG data every time
        data  = np.random.random_sample(size = 8)
        time.sleep(1/256)

        #send data to pipe
        connection.send(data)

        #print parallel process
        print(data)

        iterationnumber = iterationnumber + 1

        print(iterationnumber)

def datavos(connection):

    while True:

        # receive data from pipe
        data = connection.recv()

        #print data
        print('poep')

def datavis(connection):

    plt.style.use('fivethirtyeight')

    x_vals = []
    y_vals = []

    index = count()

    def animate(i):
        
        data = connection.recv()
        
        x = i
        y1 = data[0]


        plt.cla()

        plt.plot(x, y1, 'go--', label='Channel 1')


        plt.legend(loc='upper left')
        plt.tight_layout()
    
    ani = FuncAnimation(plt.gcf(), animate, interval=1)    
    plt.show()
    
  

if __name__ == "__main__":  # confirms that the code is under main function
    
    #declare pipeline, I declare
    conn1, conn2 = Pipe()

    datastream_process = Process(target = datastream, args = (conn2,))
    datastream_process.start()


    datavis_process = Process(target = datavis, args = (conn1,))
    datavis_process.start()




