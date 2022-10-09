from apps.core.exceptions import GenericException


class NoItemException(GenericException):
    code = 7000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Course does not exist."
        super().__init__(message=message)


class CheckElementExistException(GenericException):
    code = 7001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Document is not in course."
        super().__init__(message=message)
