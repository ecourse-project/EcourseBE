from apps.core.exceptions import GenericException


class NoCourseException(GenericException):
    code = 7000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Course does not exist."
        super().__init__(message=message)
