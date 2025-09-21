from datetime import datetime
from typing import Optional, Dict, Any

class CustomHTTPException(Exception):
    """Custom HTTP exception with additional details"""
    def __init__(
        self,
        status_code: int,
        error_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.utcnow()

class ValidationException(CustomHTTPException):
    """Validation error exception"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=422,
            error_type="validation_error",
            message=message,
            details=details
        )

class AuthenticationException(CustomHTTPException):
    """Authentication error exception"""
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=401,
            error_type="authentication_error",
            message=message,
            details=details
        )

class AuthorizationException(CustomHTTPException):
    """Authorization error exception"""
    def __init__(self, message: str = "Insufficient permissions", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=403,
            error_type="authorization_error",
            message=message,
            details=details
        )

class NotFoundException(CustomHTTPException):
    """Not found error exception"""
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=404,
            error_type="not_found",
            message=message,
            details=details
        )

class ConflictException(CustomHTTPException):
    """Conflict error exception"""
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=409,
            error_type="conflict",
            message=message,
            details=details
        )

class RateLimitException(CustomHTTPException):
    """Rate limit exceeded exception"""
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=429,
            error_type="rate_limit_exceeded",
            message=message,
            details=details
        )

class ServiceUnavailableException(CustomHTTPException):
    """Service unavailable exception"""
    def __init__(self, message: str = "Service temporarily unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=503,
            error_type="service_unavailable",
            message=message,
            details=details
        )