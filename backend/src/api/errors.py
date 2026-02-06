from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


class TaskException(HTTPException):
    """Base exception for task-related errors."""
    def __init__(self, status_code: int, detail: str, code: str):
        super().__init__(status_code=status_code, detail=detail)
        self.code = code


class TaskNotFoundException(TaskException):
    """Exception raised when a task is not found."""
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found.",
            code="TASK_NOT_FOUND"
        )


class TaskOwnershipException(TaskException):
    """Exception raised when a user does not own a task."""
    def __init__(self, task_id: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User does not have ownership of task with ID {task_id}.",
            code="TASK_OWNERSHIP_FORBIDDEN"
        )


def http_exception_handler(request, exc: HTTPException):
    """Custom handler for FastAPI HTTPExceptions."""
    error_message = exc.detail
    error_code = None

    if isinstance(exc.detail, dict):
        error_message = exc.detail.get("message", "An unexpected error occurred.")
        error_code = exc.detail.get("code")
    
    if error_code is None:
        if isinstance(error_message, str):
            error_code = error_message.replace(" ", "_").upper()
        else:
            error_code = "UNKNOWN_ERROR" # Fallback if message is not a string either

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": error_code,
                "message": error_message,
                "details": getattr(exc, "details", None)
            }
        }
    )


def task_exception_handler(request, exc: TaskException):
    """Custom handler for Task-related exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.detail,
                "details": getattr(exc, "details", None)
            }
        }
    )