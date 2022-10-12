from apps.core.exceptions import GenericException


class CheckContentLengthException(GenericException):
    code = 8000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Content cannot be empty and must be less than 500 characters."
        super().__init__(message=message)