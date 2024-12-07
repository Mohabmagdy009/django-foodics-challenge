# region Standard Library Imports
import os  # For interacting with the operating system

from rest_framework.response import Response  # For creating API responses
from rest_framework import status  # For HTTP status codes
from rest_framework import viewsets, permissions
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

# Django REST Framework Simple JWT Imports
from rest_framework_simplejwt.tokens import RefreshToken  # For handling JWT tokens
from rest_framework_simplejwt.authentication import JWTAuthentication  # For JWT authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# endregion
