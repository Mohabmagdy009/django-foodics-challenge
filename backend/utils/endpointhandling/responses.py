# region Imports
from rest_framework.response import Response  # DRF class for constructing HTTP responses
from rest_framework import status  # Provides standard HTTP status codes
from django.http import FileResponse  # Django class for serving files over HTTP
# endregion


def standard_response(success, message, data=None, status_code=status.HTTP_200_OK, key="", errors=None):
    """
    Creates a standard HTTP response with a custom structure.

    Parameters:
    - success (bool): Indicates if the operation was successful.
    - message (str): Message to be included in the response.
    - data (dict, optional): Data to be included in the response.
    - status_code (int): HTTP status code for the response.
    - key (str, optional): A key for additional context in the response.
    - errors (dict, optional): Errors to be included in the response.

    Returns:
    - Response: A DRF Response object with the custom structure.
    """
    response = {
        "success": success,
        "message": message,
        "data": data,
        "key": key,
        "errors": errors,
    }
    return Response(response, status=status_code)


def success_response(data=None, message="Data Retrieved Successfully!", status_code=status.HTTP_200_OK):
    """
    Creates a successful HTTP response with a standard success message.

    Parameters:
    - data (dict, optional): Data to be included in the response.
    - message (str): Message to be included in the response.
    - status_code (int): HTTP status code for the response.

    Returns:
    - Response: A DRF Response object indicating success.
    """
    return standard_response(success=True, message=message, data=data, status_code=status_code)


def saved_successfully_response(message, status_code=status.HTTP_201_CREATED, key="", errors=None):
    """
    Creates a successful HTTP response indicating that something was saved.

    Parameters:
    - message (str): Message to be included in the response.
    - status_code (int): HTTP status code for the response.
    - key (str, optional): A key for additional context in the response.
    - errors (dict, optional): Errors to be included in the response.

    Returns:
    - Response: A DRF Response object indicating success.
    """
    return standard_response(success=True, message=message, status_code=status_code, key=key, errors=errors)


def update_successful_response(message="Updated Successfully!", data=None, status_code=status.HTTP_200_OK, key="",
                               errors=None):
    """
    Creates a successful HTTP response indicating that a resource was updated.

    Parameters:
    - message (str): Message to be included in the response.
    - data (dict, optional): Data to be included in the response.
    - status_code (int): HTTP status code for the response.
    - key (str, optional): A key for additional context in the response.
    - errors (dict, optional): Errors to be included in the response.

    Returns:
    - Response: A DRF Response object indicating successful update.
    """
    return standard_response(success=True, message=message, data=data, status_code=status_code, key=key, errors=errors)


def file_response(file_path, filename, status_code=status.HTTP_200_OK, as_attachment=True):
    """
    Creates a response to serve a file over HTTP.

    Parameters:
    - file_path (str): Path to the file to be served.
    - filename (str): Name of the file to be served.
    - status_code (int): HTTP status code for the response.
    - as_attachment (bool): Whether to serve the file as an attachment.

    Returns:
    - Response: A Django FileResponse object if the file exists, or a standard error response.
    """
    try:
        response = FileResponse(open(file_path, 'rb'), as_attachment=as_attachment, filename=filename)
        response['success'] = True
        response['message'] = "File downloaded successfully."
        return response
    except FileNotFoundError:
        return standard_response(success=False, message="File not found.", status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return standard_response(success=False, message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def deletion_successful_response(message="Deleted Successfully!", status_code=status.HTTP_204_NO_CONTENT, key=""):
    """
    Creates a successful HTTP response indicating that a resource was deleted.

    Parameters:
    - message (str): Message to be included in the response.
    - status_code (int): HTTP status code for the response.
    - key (str, optional): A key for additional context in the response.

    Returns:
    - Response: A DRF Response object indicating successful deletion.
    """
    return standard_response(success=True, message=message, status_code=status_code, key=key)


def error_response(message, data=None, status_code=status.HTTP_400_BAD_REQUEST, key="", errors=None):
    """
    Creates an error HTTP response indicating that a request failed.

    Parameters:
    - message (str): Error message to be included in the response.
    - status_code (int): HTTP status code for the response.
    - key (str, optional): A key for additional context in the response.
    - errors (dict, optional): Additional error details to be included in the response.

    Returns:
    - Response: A DRF Response object indicating failure.
    """
    return standard_response(success=False, message=message, data=data, status_code=status_code, key=key, errors=errors)
