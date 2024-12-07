# region Imports
from utils.endpointhandling.responses import (
    success_response,
    saved_successfully_response,
    error_response,
    update_successful_response,
    deletion_successful_response,
)
from utils.importinglibs.views import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import APIException
from django.db import IntegrityError


# endregion


# region Base Classes ==============================================================================
class CustomResponseViewSet(GenericViewSet, mixins.CreateModelMixin,
                            mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    A base viewset that tracks the user who created an object &
    applies consistent response formats for success and errors, with no option to delete.
    """

    def perform_create(self, serializer):
        """
        Sets the user who created the object during a POST request.

        Parameters:
        - serializer: Serializer instance used to save the object.
        """
        try:
            serializer.save(user_id_create=self.request.user, user_id_update=self.request.user)
        except IntegrityError as e:
            raise APIException(f"Duplicate entry error: {str(e)}")

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Overrides the finalize_response to return custom responses based on HTTP method.
        """
        if response.status_code < 299:
            if request.method == "GET":
                return super().finalize_response(request, success_response(response.data), *args, **kwargs)
            elif request.method == "POST":
                return super().finalize_response(request, saved_successfully_response(response.data), *args, **kwargs)
            elif request.method in ["PUT", "PATCH"]:
                return super().finalize_response(request, update_successful_response(response.data), *args, **kwargs)
            else:
                return super().finalize_response(request, deletion_successful_response(), *args, **kwargs)
        else:
            return super().finalize_response(request, error_response(response.data, status_code=response.status_code), *args, **kwargs)


# endregion
