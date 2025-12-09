class LogicError(Exception):
    """Base exception for all API logic errors"""
    status_code = 500


class ResourceNotFoundError(LogicError):
    """Raised when attempting to access a resource that does not exist"""
    status_code = 404


class DuplicateResourceError(LogicError):
    """Raised when attempting to create a resource that already exists"""
    status_code = 409


def get_error_response(exception: Exception) -> tuple[int, dict]:
    """
    Convert an exception to an appropriate HTTP status code and error response.

    Args:
        exception: The exception that was raised

    Returns:
        tuple: (status_code, error_response_dict)
    """
    try:
        status_code = getattr(exception.__class__, "status_code")
    except Exception:
        return (500, {"error": "An unexpected error occurred"})

    return (status_code, {"error": str(exception)})
