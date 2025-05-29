from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger("api")


class CustomDjangoExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if hasattr(exception, "status_code"):
            return None

        logger.error(f"Unhandled exception: {str(exception)}", exc_info=True)

        error_data = {
            "error": str(exception),
            "detail": "An unexpected error occurred.",
            "status_code": 500,
        }

        if isinstance(exception, ObjectDoesNotExist):
            error_data.update(
                {
                    "error": f"{exception.__class__.__name__}: {str(exception)}",
                    "detail": "The requested resource was not found.",
                    "status_code": 404,
                }
            )
        elif isinstance(exception, AssertionError):
            error_data.update(
                {
                    "error": f"AssertionError: {str(exception)}",
                    "detail": "Invalid serializer configuration.",
                    "status_code": 400,
                }
            )

        return JsonResponse(error_data, status=error_data["status_code"])
