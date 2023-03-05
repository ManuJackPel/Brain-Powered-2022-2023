import os
import sys
import numpy as np
import time
import pickle
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.svm import LinearSVC, NuSVC, SVC

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

# from _code.classes.classifier import Classifer, method_argument_checker
from _code.classes.builder import ProcessBuilder, Part, Process

clf_part_to_process_map = {
        'classifier': {
            'kNN' : KNeighborsClassifier,
            'rNN' : RadiusNeighborsClassifier,
            'linear_SVC' : LinearSVC,
            'SVC' : SVC,
            'NuSVC' : NuSVC,
            }
        }
            
# Helper Functions
def init_clf_builder():
    clf_builder = ProcessBuilder(clf_part_to_process_map)
    clf_part = Part('classifier', 'kNN', {'n_neighbors': 3})
    clf_builder.add_part(clf_part)
    return clf_builder

def assert_objs_equal(object_one, object_two):
    serial_object_one = pickle.dumps(object_one)
    serial_object_two = pickle.dumps(object_two)
    return serial_object_one == serial_object_two

# Test Functions
def test_builder_should_return_process():
    clf_builder = init_clf_builder()
    err_msg = "Process returned from builder does not match the added part"
    for process in clf_builder.list_processes() :
        assert assert_objs_equal(process, KNeighborsClassifier(n_neighbors=3)),err_msg

def test_builder_should_return_added_parts():
    clf_builder = init_clf_builder()
    err_msg = 'Parts listed by builder do not match, part added to builder'
    assert clf_builder.list_parts() == [Part(name='classifier', variant='kNN', variant_params={'n_neighbors': 3})], err_msg

def test_builder_should_return_process_object():
    builder = init_clf_builder()
    process = builder.build()
    assert type(process) == Process, "ProcessBuilder did not return a Process object"

def test_classifier_process_should_have_single_process():
    clf_builder = init_clf_builder()
    dummy_part = Part('filter', 'butterworth', {'l': 8, 'h' : 12})

    
    clf_builder.add_part(dummy_part)

    building_was_allowed = True

    try:
        clf_builder.build()
    except:
        building_was_allowed = False

    err_msg = "A Builder should raise an error when a Classifier Part is added alongside other Parts"
    assert building_was_allowed == False, err_msg
        

def test_classifier_process_should_not_use_process():
    pass

def test_non_classifier_process_should_not_use_predict():
    pass
                    
