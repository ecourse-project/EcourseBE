from apps.core.exceptions import GenericException

class MissedUsernameOrEmailException(GenericException):
    code = 2000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Username or email is required."
        super().__init__(message=message)


class OldPasswordNotCorrectException(GenericException):
    code = 2001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Old password is not correct."
        super().__init__(message=message)


class PasswordNotMatchException(GenericException):
    code = 2002
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Password fields didn't match."
        super().__init__(message=message)