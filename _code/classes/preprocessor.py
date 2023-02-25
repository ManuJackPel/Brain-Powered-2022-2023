import mne
import numpy as np
from copy import deepcopy

class PreProcesser():
    def __init__(self, parts: list):
        self.processes = parts
        
    def process_data(self, data: np.ndarray) -> np.ndarray:
        for process in self.processes:
            data = process(data)
        return data
    def list_processes():
        return self.processes

class PreProcessorBuilder():
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.parts = []

    def list_parts(self):
        return [part.__name__ for part in self.parts]

    def add_filter(self, filter_params: dict[str,any]) -> None:
        def fir_filter(data: np.ndarray) -> np.ndarray:
            filt_params = filter_params
            filt_params['data'] = data
            return mne.filter.filter_data(**filt_params)
            
        self.parts.append(fir_filter)


    def build(self) -> PreProcesser:
        return PreProcesser(self.parts)
        


            


    


        
