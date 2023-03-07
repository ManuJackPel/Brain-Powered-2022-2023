import numpy as np


def get_offset_inx(data, time_row, condition_row, block_duration_sec):
    # Get time of onset
    onset_inx = np.where(data[:,condition_row] == 1)
    onset_time = data[onset_inx, time_row][0]
    # Get time of offset
    offset_time = onset_time + block_duration_sec
    #  Get inx of offset
    offset_inx = np.where(np.isin(data[:, time_row], offset_time))[0]
    return offset_inx

def main():
    data = np.loadtxt('subject_01.csv', delimiter=',')
    
    for condition_row in [17, 18]:
        onset_inx  =  np.where(data[:,condition_row] == 1)[0]
        offset_inx = get_offset_inx(data, time_row=0, condition_row=condition_row, block_duration_sec=10)
        # Change all the values from onset to offset to 1
        for i in range(len(offset_inx)):
            data[onset_inx[i]:offset_inx[i], condition_row] = 1



main()
