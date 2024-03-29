from apps.core.exceptions import GenericException


class NoDocumentException(GenericException):
    code = 6000
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Document does not exist."
        super().__init__(message=message)


class CheckSaleStatusException(GenericException):
    code = 6001
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Document has been checkout or bought."
        super().__init__(message=message)
