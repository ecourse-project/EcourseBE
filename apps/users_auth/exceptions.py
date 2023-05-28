from apps.core.exceptions import GenericException


class PermissionException(GenericException):
    code = 11000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Địa chỉ IP của bạn không được phép truy cập."
        super().__init__(message=message)