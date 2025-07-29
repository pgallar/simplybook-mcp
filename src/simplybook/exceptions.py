from typing import Optional, Dict, Any

class SimplyBookException(Exception):
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class AuthenticationError(SimplyBookException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)

class ResourceNotFoundError(SimplyBookException):
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", status_code=404)