from apps.core.exceptions import GenericException


class CompletedQuizException(GenericException):
    code = 9000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Quiz is completed."
        super().__init__(message=message)
