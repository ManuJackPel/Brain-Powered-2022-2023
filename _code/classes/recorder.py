import numpy as np
import os

class Recorder():
    def __init__(self, file_name, header):
        self.file_name = file_name
        self.header = header

    def append_data(self, data):
        if self.file_name_exists():
            self._append_to_txt(data)
        else:
            self._create_txt()

    def file_name_exists(self):
        return os.path.isfile(self.file_name)

    def _append_to_txt(self, data):
        with open(self.file_name, 'a', encoding='UTF8') as f:
            f.truncate(0)
            np.savetxt(f, data)

    def _create_txt(self):
        with open(self.file_name, 'w', encoding='UTF8') as f:
            f.write(self.header)
            f.close()



