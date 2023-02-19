class ParameterChecker():
    def __init__(self, parameter_with_types):
        self.valid_parameter_names = tuple(parameter_with_types.keys())
        self.valid_parameter_with_types = parameter_with_types

    def is_valid_parameter_names(self, parameter_names) -> bool:
        """Check if passed names exist in list of valid names"""
        # Check if empty dict of parameters was passed
        if len(parameter_names) == 0:
            return False
        # Check if passed parameters are in the pre-registered parameter names
        for name in parameter_names:
            if name not in self.valid_parameter_names:
                return False
        return True

    def is_valid_parameter_types(self, parameters) -> bool:
        """Check if passed types match parameters"""
        # Iterate through each parameter name
        for parameter_name in parameters.keys():
            # See if the type of passed parameter matched pre-registered parameters
            registered_type = self.valid_parameter_with_types[parameter_name] 
            passed_type = type(parameters[parameter_name])
            if passed_type != registered_type:
                return False
        return True

