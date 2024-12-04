class ExternalServiceError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(f"{message} (Status code: {status_code})")


__all__ = ["ExternalServiceError"]
