# Typehinting
# Easier API to implement prediction

class Decoder:
    """
    A wrapper class for making use of all the steps to decode EEg data into Drone Commands.
    """
    
    def __init__(self, steps: dict[str, any]):
        self.filter = steps['filter']
        self.feature_extraction = steps['feature_extraction']
        self.classifier = steps['classifier']

    def predict(data: ndarray):
        """ Run the steps to return prediction"""
        filtered_data = self.filter.filter(data)
        extracted_data = self.feature_extraction.extract(filtered_data)
        prediction = self.classifier.classify(extracted_data)
        return prediction
        

        



   

