import os 
import sys
import numpy as np
import time

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes import dataloader, preprocessor

def main():
    # Parameter
    channels = ['Fp1', 'Fp2', 'Fc5', 'Fz', 'Fc6', 'T7', 'Cz', 'T8']
    n_samples_pulled = 256 * 5
    dataset = 'GIPSA-lab'
    participant = 0
    Fs = 256 
    filter_range = (4,6)
    
    # Paramter Classes
    pp_params = {
            "filt_range" : filter_range,
            "samp_freq" : Fs,
            }
    pre_processor = preprocessor.Preprocess(pp_params)
    

    
    # LOAD DATA
    stream = dataloader.DataLoader(dataset, channels, participant)
    samp_data = stream.pull_sample(n_samples_pulled)
    start_time = time.time()
    while True:
        output = stream.pull_sample(n_samples_pulled)
        # PRE-PROCESS
        output = pre_processor.transform(output)
        
        print(output.shape[0])
        print(time.time() - start_time)

if __name__ == '__main__':
    main()
