from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from typing import Any
from .parameter_checker import ParameterChecker


Part = tuple[str, Any]
valid_classifier_parameters = {
        'classifier' : str,
        'n_neighbors' : int,
        'algorithm' : str,
        }
ClfParCheck = ParameterChecker(valid_classifier_parameters)

class Product1():
    """
    It makes sense to use the Builder pattern only when your products are quite
    complex and require extensive configuration.

    Unlike in other creational patterns, different concrete builders can produce
    unrelated products. In other words, results of various builders may not
    always follow the same interface.
    """

    def __init__(self) -> None:
        self.parts = {}

    def add(self, part: Part) -> None:
        """Add part to builder"""
        if not self.is_valid_part(part):
            return 
        part_name, part_value = part
        self.parts[part_name] = part_value

    def is_valid_part(self, part) -> bool:
        part_name, part_value = part
        if not ClfParCheck.is_valid_parameter_names(part_name):
            print(f"'{part_name}' is not a valid Class parameter name")
            return False
        if not ClfParCheck.is_valid_parameter_types(part):
            print(f"{part_value} has type {type(part_value)}, does not match type for '{part_name}', should be {ClfParCheck.return_paramter_type(part_name)}")
            return False
        return True

    def list_parts(self) -> list:
        return self.parts
    
    def build(self) -> None:
        pass

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

    



    



