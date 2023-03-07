from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.svm import LinearSVC, NuSVC, SVC
from typing import Any
from copy import deepcopy

Part = tuple[str, Any]

clf_name_to_algo_map = {
        'kNN' : KNeighborsClassifier,
        'rNN' : RadiusNeighborsClassifier,
        'linear_SVC' : LinearSVC,
        'SVC' : SVC,
        'NuSVC' : NuSVC,
        }

class ClassifierBuilder():
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
        # Temporary until we find a good way to implement checkign parameters
        return True

    def return_info(self):
        return deepcopy(self.parts)

    def return_classifier_name(self) -> str:
        return self.parts['classifier_name']
    
    def return_classifier_parameters(self) -> dict:
        clf_params = {key : self.parts[key] for key in self.parts.keys() if key != 'classifier_name'}
        return clf_params

    def build(self) -> None:
        classifier_name = self.return_classifier_name()
        classifier_params = self.return_classifier_parameters()
        classifier_algorithm = clf_name_to_algo_map[classifier_name](**classifier_params)
        return Classifier(classifier_algorithm, classifier_params)

class Classifier():
    """Interface for accessing EEG classification methods"""
    def __init__(self, classifier_algorithm, parameters):
        self.clf_algo =  classifier_algorithm
        self.parameters = parameters

    def fit(self, training_data):
        """Fit model"""
        self.clf_algo.fit(training_data)

    def predict(self, sample):
        return self.clf_algo.predict(sample)

    def list_parameters(self):
        return self.parameters

