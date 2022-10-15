from apps.core.exceptions import GenericException


class UserHasBeenRateException(GenericException):
    code = 10000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "User has been rate this document."
        super().__init__(message=message)