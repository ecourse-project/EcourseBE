from apps.core.exceptions import GenericException


class FileEmptyException(GenericException):
    code = 3000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "File is not valid"
        super().__init__(message=message)


class FolderNameEmptyException(GenericException):
    code = 3001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Folder name can not be empty."
        super().__init__(message=message)


class FileNameOrFileTypeIsNotValidException(GenericException):
    code = 3002
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "File name or file type is not valid.."
        super().__init__(message=message)


class LargeFileException(GenericException):
    code = 3003
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "File is too large"
        super().__init__(message=message)
