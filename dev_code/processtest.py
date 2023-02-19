from multiprocessing import Process, Pipe
import numpy as np
import random
import time


def datastream(connection):
    
    while True:
        
        #make the EEG data every time
        data  = np.random.random_sample(size = 8)
        time.sleep(1/256)

        #send data to pipe
        connection.send(data)

        #print parallel process
        print('parallellepipidum')

def datavis(connection):

    while True:

        # receive data from pipe
        data = connection.recv()

        #print data
        print(data)



if __name__ == "__main__":  # confirms that the code is under main function
    
    #declare pipeline, I declare
    conn1, conn2 = Pipe()

    datastream_process = Process(target=datastream, args = (conn2,))
    datastream_process.start()

    datavis_process = Process(target = datavis, args = (conn1,))
    datavis_process.start()


