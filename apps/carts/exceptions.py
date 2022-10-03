from apps.core.exceptions import GenericException


class DocumentExistException(GenericException):
    code = 4000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Document already exist in cart or favorite list."
        super().__init__(message=message)


class DocumentNotExistException(GenericException):
    code = 4001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Document does not exist in cart or favorite list."
        super().__init__(message=message)


class CourseExistException(GenericException):
    code = 4002
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Course already exist in cart or favorite list."
        super().__init__(message=message)


class CourseNotExistException(GenericException):
    code = 4003
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Course does not exist in cart or favorite list."
        super().__init__(message=message)


class ListDocumentsEmptyException(GenericException):
    code = 4004
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "List documents is empty."
        super().__init__(message=message)


class ListCoursesEmptyException(GenericException):
    code = 4005
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "List courses is empty."
        super().__init__(message=message)
