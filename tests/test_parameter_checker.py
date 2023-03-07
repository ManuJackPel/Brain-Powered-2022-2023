import os
import sys
import numpy as np
import time

# Change sys path to be able to import from Brain Powered Classes
cwd = os.getcwd()
pard = os.path.dirname(cwd)
targetd = pard + '/Brain-Powered-2022-2023'
sys.path.append(pard)

from _code.classes.parameter_checker import ParameterChecker

param_types = {
        'filter_bounds' : tuple,
    }

parameter_checker = ParameterChecker(param_types)

def test_param_checker_valid_names():
    valid_param_names = {
            'filter_bounds' :  (0.5, 5),
            }

    invalid_param_names = {
            'filter_bounds' :  (0.5, 5),
            'non_existant_parameter' : (0),
            }

    empty_param_names = {}

    assert parameter_checker.is_valid_parameter_names(valid_param_names), "A valid parameter name is not passing"
    assert not parameter_checker.is_valid_parameter_names(invalid_param_names), "A invalid parameter name is passing"
    assert not parameter_checker.is_valid_parameter_names(empty_param_names), "A empty parameter is passing"

def test_param_checker_valid_types():
    valid_param_types = {
            'filter_bounds' :  (0.5, 5),
            }

    invalid_param_types = {
            'filter_bounds' :  "a string",
            }

    assert parameter_checker.is_valid_parameter_types(valid_param_types), "A valid parameter type is not passing"
    assert not parameter_checker.is_valid_parameter_types(invalid_param_types), "A invalid parameter type is passing"


    

    



