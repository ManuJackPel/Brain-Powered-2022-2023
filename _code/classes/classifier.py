from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from typing import Any

class Classifier():
    """Interface for accessing EEG classification methods"""
    def __init__(self, method: str, meth_args: dict=None):
        if is_valid_method_arguments == False:
            assert False, "Invalid arguents passed for given method"

        match method:
            case 'kNN':
                self.method = KNeighborsClassifier()
            case 'rNN':
                self.method = RadiusNeighborsClassifier()

    def fit(self, training_sample):
        """Fit model"""
        self.method.fit(training_sample)

    def predict(self, sample):
        return self.predict(sample)

def is_valid_method_arguments(method: str, args: dict[str, Any]):
    """Check that argument passed for a method are valid"""
    kNN_types = {
            "n_neighbors" : int,
            "weights" : str,
            "algorithm" : str
            }
    
    rNN_type = {
            "n_neighbors" : int,
            "weights" : str,
            "algorithm" : str
            }

    # Match keyword to type dictionary 
    # Check that keyword exist
    match method:
        case "kNN":
            type_dict = kNN_types
        case other: 
            print("Passed a method which does not exist")
            return False
    
    # Check that all arguments are present
    if list(args.keys()) != list(type_dict.keys()):
        return False

    # Check that types are correct
    for keyword in type_dict.keys():
        if type_dict[keyword] != type(args[keyword]):
            return False
    return True

    



    



