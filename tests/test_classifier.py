import os
import sys
import numpy as np
import time
from sklearn.neighbors import KNeighborsClassifier

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

# from _code.classes.classifier import Classifer, method_argument_checker
from _code.classes.classifier import ClassifierBuilder , Classifier
from _code.classes.errors import BuilderIsEmpty, BuilderMissingEssentialParts


def init_basic_builder():
    clf_builder = ClassifierBuilder()
    clf_builder.add(('classifier_name', 'kNN'))
    clf_builder.add(('n_neighbors', 3))
    return clf_builder


def test_builder_added_items_listed():
    clf_builder = init_basic_builder()
    added_parts = clf_builder.return_info()

    valid_parts = {
                'classifier_name' : 'kNN',
                'n_neighbors': 3, 
                }
    assert added_parts == valid_parts, "Add parts are not present in the classifier builder"

def test_clf_builder_parts_return_right_values():
    clf_builder = init_basic_builder()

    clf_name = clf_builder.return_classifier_name()
    assert clf_name == 'kNN', "Returned classifer name is not equal to name passed to builder"
    
    valid_params = {'n_neighbors': 3}
    clf_params = clf_builder.return_classifier_parameters()
    assert clf_params == valid_params, "Returned classifer parameters is not equal to parameters passed to builder"
    
def test_clf_builder_right_params_for_classifier():
    pass
    # what happens when you dont pass the right param
    
def test_clf_builder_builds_right_object():
    clf_builder = init_basic_builder()
    classifier = clf_builder.build()
    assert type(classifier) == Classifier, "Object returned from classifer builder was not of type Classifier"
    assert type(classifier.clf_algo) == KNeighborsClassifier, "Algorithm of returned Classifier does not match name passed to ClassifierBuilder"

def test_clf_builder_builds_right_object():
    clf_builder = init_basic_builder()
    classifier = clf_builder.build()




    













# def test_clf_builder_return_params():

#     added_parts = clf_builder.list_parts()
#     n_parts = len(added_parts.keys())
#     assert n_parts == 2, "The amount of parts does not match the amount of add commands"
#     clf_builder.add(('silliness', 3))

#     added_parts = clf_builder.list_parts()
#     n_parts = len(added_parts.keys())
#     assert n_parts == 2, "An invalid part was added to the builder"

#     clf_builder.add(('algorithm', 'uniform'))
#     added_parts = clf_builder.list_parts()
#     n_parts = len(added_parts.keys())
#     print(added_parts)
#     assert n_parts == 3, "The amount of parts does not match the amount of add commands"

# def test_clf_builder_build():
#     clf_builder = ClassifierBuilder()
#     classifier = clf_builder.build()
#     assert type(classifier) == BuilderIsEmpty(), "An empty classifier builder should return EmptyBuilder"

#     clf_builder.add(('algorithm', 'uniform'))
#     classifier = clf_builder.build()
#     assert type(classifier) == BuilderMissingEssentialParts(), "A classifier without the essential parameters should return BuilderMissingEssentialParameter"
    
#     clf_builder.add(('n_neighbors', 3))
#     classifier = clf_builder.build()
#     assert type(classifer) == Classifer, "A builder with all essential parameters should return a Classifier"
