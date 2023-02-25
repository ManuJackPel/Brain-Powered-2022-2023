class FeatureExtractor():
    pass

class FeatureExtractorBuilder():
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.parts = []

    def list_parts(self):
        return [part.__name__ for part in self.parts]

    def add(self, filter_params: dict[str,any]) -> None:
        pass


    def build(self) -> PreProcesser:
        return FeatureExtractor(self.parts)
