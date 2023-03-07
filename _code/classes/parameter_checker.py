from typing import Union, Any
from .errors import ParamterNotRegistered

Part = tuple[str, Any]

class ParameterChecker():
    def __init__(self, parameter_with_types):
        self.valid_parameter_names = tuple(parameter_with_types.keys())
        self.valid_parameter_with_types = parameter_with_types

    def is_valid_parameter_names(self, parameter_names: Union[str, list[str]]) -> bool:
        """Check if passed names exist in list of valid names"""
        # If a string is passed put it in a list
        if type(parameter_names) == str:
            parameter_names = [parameter_names]
        # Check if empty dict of parameters was passed
        if len(parameter_names) == 0:
            return False
        # Check if passed parameters are in the pre-registered parameter names
        for name in parameter_names:
            if name not in self.valid_parameter_names:
                return False
        return True

    def is_valid_parameter_types(self, parameter: Part) -> bool:
        """Check if passed types match parameters"""
        # Iterate through each parameter name
        parameter_name, parameter_value = parameter
        registered_type = self.valid_parameter_with_types[parameter_name] 
        passed_type = type(parameter_value) 
        print(registered_type)
        print(passed_type)
        if passed_type != registered_type:
            return False
        return True
    
    def return_paramter_type(self, parameter_name: str):
        """If a parameter is registered, return the type of its value"""
        if self.is_valid_parameter_names(parameter_name):
            return self.valid_parameter_with_types[parameter_name]
        return ParamterNotRegistered()


