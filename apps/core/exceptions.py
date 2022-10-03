from rest_framework import status
from rest_framework.exceptions import APIException


class GenericException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    code = 1000
    summary = "Error"
    verbose = False
    error_detail = None

    def __init__(self, message=None, status_code=400, error_detail=None):
        if not message:
            message = "Oops! Something went wrong, please try again"
        if status_code:
            self.status_code = status_code
        if error_detail:
            self.error_detail = error_detail
        super().__init__(message)

    def serialize(self):
        data = {
            "status_code": self.status_code,
            "code": self.code,
            "summary": self.summary,
            "message": self.detail,
        }

        if self.error_detail:
            data.update({"error_detail": self.error_detail})
        return data
