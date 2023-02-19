import os 
import sys
import numpy as np
import time

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes import datasets

channels = ['Fp1', 'Fp2', 'Fc5', 'Fz', 'Fc6', 'T7', 'Cz', 'T8']
data_set = datasets.DataSets(
        data_source = 'GIPSA-lab', 
        channels = channels, 
        participant = 20,
        set_type = "train",
        )

def test_time_stamps():
    time_stamps = data_set.return_training_set()[:, 0]
    i = 5
    assert time_stamps[i * 512] % 1 == 0.0, "Time axis of GIPSA-lab data does not match up"

def test_get_index():
    eyes_closed =  data_set.return_training_set()[:, 17]
    eyes_open =  data_set.return_training_set()[:, 18]
    assert (len(np.where(eyes_closed == 1)[0])) == 5 , "Data Set does not have 5 eyes closed conditions"
    assert (len(np.where(eyes_open == 1)[0])) == 5, "Data Set does not have 5 eyes open conditions"

def test_labeled_split():
    data_set.split_by_label()
    # sample, label = data_set.split_by_label()




# def test_train_sample_shape():
#     train_set, train_label = data_set.return_train_samples()
# confirms that the code is under main functiondef datastream(connection):
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




#     assert train_set.shape == (n_samples, n_features), "Training Sample appears to be the wrong shape"
#     assert train_label.shape == (n_samples), "Training Sample appears to be the wrong shape"
#     n_samples_class_zero = len(np.where(train_label == 0)[0])
#     n_samples_class_one = len(np.where(train_label == 1)[0])
#     assert n_samples_class_one == n_samples_class_zero, "Unequal amount of samples in class zero and one"

    

test_labeled_split()





