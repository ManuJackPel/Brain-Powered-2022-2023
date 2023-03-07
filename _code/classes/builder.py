from typing import Any
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Part:
    name: str
    variant: str
    variant_params: dict[str, Any] = field(default_factory=dict)

class Process():
    def __init__(self, processes):
        pass
    def fit(self, training_data):
        pass
    def predict(self, sample_data):
        pass
    def process(self, input_data):
        pass

class ProcessBuilder():
    def __init__(self, part_to_process_map):
        self.part_to_process_map = part_to_process_map
        self.parts = []

    def reset(self) -> None:
        self.parts = []

    def list_parts(self):
        return [part for part in self.parts]

    def list_processes(self):
        return self.map_part_to_process(self.parts)

    def add_part(self, part:Part) -> None:
        self._add_part_to_builder(part)

    def _add_part_to_builder(self, process):
        self.parts.append(process)

    def map_part_to_process(self, part: Part):
        return [self.part_to_process_map[part.name][part.variant](**part.variant_params) for part in part]

    def build(self) -> Process:
        self.check_parts_are_valid()
        print('building was allowed')
        return Process(self.parts)

    def check_parts_are_valid(self):
        if not self.check_classifier_part_is_exclusive():
            raise Exception('Builder with a Classifier Part cannot have other Parts')

    def check_classifier_part_is_exclusive(self):
        n_classifier_parts = 0
        n_parts = 0
        for part in self.parts:
            if part.name == 'classifier':
                n_classifier_parts += 1
            n_parts += 1
            if n_parts > 1 & n_classifier_parts > 0:
                return False
        return True





    
    
