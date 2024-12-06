# region Standard Library Imports
import json  # For working with JSON data
import os  # For interacting with the operating system
import warnings  # For issuing warning messages
import mimetypes  # For handling MIME types
from datetime import date, datetime, timedelta  # For working with dates and times

# Third-Party Library Imports
import requests  # For making HTTP requests

# Django REST Framework Imports
from rest_framework.decorators import (
    api_view,  # For creating API views
    authentication_classes,  # For setting authentication classes
    permission_classes,  # For setting permission classes
    parser_classes  # For setting parser classes
)
from rest_framework.permissions import IsAuthenticated, AllowAny  # For setting permissions
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
