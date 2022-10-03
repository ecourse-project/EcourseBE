from apps.core.exceptions import GenericException


class NoItemsException(GenericException):
    code = 5000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "There are no any items to checkout."
        super().__init__(message=message)
