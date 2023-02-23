class InvalidPart(Exception):
    "Raised when part is not registered in the builder"
    pass

class ParamterNotRegistered(Exception):
    "Raised when parameter is not registered in the ParameterChecker"
    pass


class BuilderIsEmpty(Exception):
    "Raised when a Builder is empty"
    pass

class BuilderMissingEssentialParts(Exception):
    "Raised when a Builder is missing essential parts"
    pass


