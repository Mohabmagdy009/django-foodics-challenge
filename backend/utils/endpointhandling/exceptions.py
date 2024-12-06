# region Imports
from utils.importinglibs.views import status, APIException
# endregion


class BaseCustomException(APIException):
    """
    A base custom exception class that extends DRF's APIException.

    Attributes:
        status_code (int): HTTP status code for the exception.
        success (bool): Indicates the success status, typically False.
        errors (dict or list): Additional error details.
        key (str): A custom key identifying the error type.
    """
    # Default class attributes
    status_code = status.HTTP_400_BAD_REQUEST  # Default HTTP status code
    success = False  # Default success flag
    errors = None  # Placeholder for error details
    key = ""  # Default key for the error type

    def __init__(self, message, code, key="", errors=None):
        """
        Initialize the BaseCustomException with custom attributes.

        Args:
            message (str): The error message.
            code (int): HTTP status code for the exception.
            key (str, optional): Custom key identifying the error type. Defaults to "".
            errors (dict or list, optional): Additional error details. Defaults to None.
        """
        super().__init__(message, code)
        self.status_code = code
        self.success = False
        self.key = key
        self.errors = errors
