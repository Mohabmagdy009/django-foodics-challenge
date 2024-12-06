# Django ORM utilities and query operations
from django.db.models import F, Sum, OuterRef, Max, Subquery, Value, Func, CharField, Q, Avg, Window, Exists
from django.db import transaction
from django.shortcuts import get_object_or_404  # Retrieve an object or return a 404 error
from django.utils import timezone  # Handle time-related operations, including time zones
from django.conf import settings  # Access project settings

# Standard libraries
import os  # Interact with the operating system (file system operations)
from datetime import datetime, timedelta  # Work with dates and times
import json  # Parse and serialize JSON data

# Django REST Framework utilities
from rest_framework import serializers  # Create serializers for data validation and transformation
from rest_framework.exceptions import ValidationError  # Handle validation errors in APIs
from rest_framework.validators import UniqueValidator
