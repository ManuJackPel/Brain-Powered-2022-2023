import os
import sys
import numpy as np
import time

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

# from _code.classes.classifier import Classifer, method_argument_checker
from _code.classes.classifier import Classifier, is_valid_method_arguments

keyword_to_class = {
        'kNN' : 'KNeighborsClassifier()',
        'rNN' : 'RadiusNeighborsClassifier()',
        }

def test_match_case_methods():
    for keyword, class_ in keyword_to_class.items():
        print(keyword, class_)
        clf = Classifier(keyword)
        print(clf.method)
        assert str(clf.method) == class_

def test_method_argument_checker():
    # Input a keyword and argument
    kNN_args = {
            "n_neighbors" : 3,
            "weights" : "distance",
            "algorithm" : "auto",
            }

    assert is_valid_method_arguments('kNN', kNN_args) == True
    assert is_valid_method_arguments('SVM', kNN_args) == False
    kNN_args['n_neighbors'] = 'three'
    assert is_valid_method_arguments('kNN', kNN_args) == False
    kNN_args['n_neighbors'] = 10
    assert is_valid_method_arguments('kNN', kNN_args) == True
    kNN_args['dummy_argument'] = 'Nonsense'
    assert is_valid_method_arguments('kNN', kNN_args) == False



