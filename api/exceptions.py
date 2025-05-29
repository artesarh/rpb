from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException


def custom_drf_exception_handler(exc, context):
    # Call DRF's default exception handler to get the standard error response
    response = exception_handler(exc, context)

    if response is not None:
        # Format the response as a consistent JSON structure
        error_data = {
            "error": str(exc),
            "detail": response.data.get("detail", response.data),
            "status_code": response.status_code,
        }
        return Response(error_data, status=response.status_code)

    # If DRF doesn't handle the exception, let Django handle it
    return None
