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
from _code.classes.builder import Builder


clf_builder = Builder(clf_parts_dict, display_method)
fe_buidler = Builder(fe_parts_dict)

clf.builder.add(('classifier', 'kNN', knn_params))

clf_parts = clf.list_parts 




