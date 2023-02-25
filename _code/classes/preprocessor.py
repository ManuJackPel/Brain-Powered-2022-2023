from mne.filter import filter_data

class PreProcessorBuilder():
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.parts = []

    def add_filter(self, filter_params: dict[str,any]) -> None:
        self.parts.append(filter_data(**filter_params))

    def build(self) -> PreProcesser:
        return PreProcesser(self.parts)
        


class PreProcesser():
    def __init__(self, parts: list):
        self.processes = parts
        
    def process_data(self, data: ndarray) -> ndarray:
        for process in self.processes:
            data = process(data)
        return data
    def list_processes():
        return self.processes
            


    


        
