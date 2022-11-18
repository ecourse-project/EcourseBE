from apps.core.exceptions import GenericException


class UserHasBeenRateException(GenericException):
    code = 10000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "User has rated this document."
        super().__init__(message=message)


class EmptyFeedbackException(GenericException):
    code = 10001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Feedback cannot be empty."
        super().__init__(message=message)
