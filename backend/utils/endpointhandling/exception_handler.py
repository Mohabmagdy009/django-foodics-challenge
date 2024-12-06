# region Imports
from utils.importinglibs.views import os, Response, exception_handler, status, APIException
from utils.endpointhandling.exceptions import BaseCustomException
# endregion


# Custom exception handler for the Django REST Framework
def custom_exception_handler(exc, context):
    """
        Custom exception handler that extends the default DRF exception handler.

        Args:
            exc (Exception): The exception that was raised.
            context (dict): Additional context provided by DRF, including view information.

        Returns:
            Response: An appropriate DRF Response object with serialized error data.
    """
    # Call the default exception handler provided by DRF
    response = exception_handler(exc, context)

    # Custom handling for exceptions that are instances of BaseCustomException
    if response is not None and isinstance(exc, BaseCustomException):
        return Response(
            data={
                "success": exc.success,  # Custom success flag from the exception
                "errors": exc.errors,  # Custom error details from the exception
                "key": exc.key,  # Custom key identifying the error type
                "message": str(exc)  # String representation of the exception
            },
            status=exc.status_code  # Status code from the exception
        )
    # Handle generic Python exceptions in non-debug mode
    elif not os.getenv("DEBUG") and isinstance(exc, Exception) and not isinstance(exc, APIException):
        response = Response(
            data={
                "errors": exc.args,  # Error arguments from the exception
                "message": "Internal Server Error!",  # Generic error message
                "key": "internal_server_error",  # Custom key for internal server error
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,  # HTTP 500 status code
        )

    # Return the original or custom response
    return response
