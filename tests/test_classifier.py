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
from _code.classes.classifier import Classifier, Product1, is_valid_method_arguments
from _code.classes.errors import BuilderIsEmpty, BuilderMissingEssentialParts

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

def test_clf_builder_return_params():
    clf_builder = Product1()
    clf_builder.add(('classifier', 'kNN'))
    clf_builder.add(('n_neighbors', 3))
    added_parts = clf_builder.list_parts()

    valid_parts = {
                'classifier' : 'kNN',
                'n_neighbors': 3, 
                }
    assert added_parts == valid_parts, "Add parts are not present in the classifier builder"

    added_parts = clf_builder.list_parts()
    n_parts = len(added_parts.keys())
    assert n_parts == 2, "The amount of parts does not match the amount of add commands"
    clf_builder.add(('silliness', 3))

    added_parts = clf_builder.list_parts()
    n_parts = len(added_parts.keys())
    assert n_parts == 2, "An invalid part was added to the builder"

    clf_builder.add(('algorithm', 'uniform'))
    added_parts = clf_builder.list_parts()
    n_parts = len(added_parts.keys())
    print(added_parts)
    assert n_parts == 3, "The amount of parts does not match the amount of add commands"

def test_clf_builder_build():
    clf_builder = Product1()
    classifier = clf_builder.build()
    assert type(classifier) == BuilderIsEmpty(), "An empty classifier builder should return EmptyBuilder"

    clf_builder.add(('algorithm', 'uniform'))
    classifier = clf_builder.build()
    assert type(classifier) == BuilderMissingEssentialParts(), "A classifier without the essential parameters should return BuilderMissingEssentialParameter"
    
    clf_builder.add(('n_neighbors', 3))
    classifier = clf_builder.build()
    assert type(classifer) == Classifer, "A builder with all essential parameters should return a Classifier"

    



    
    



