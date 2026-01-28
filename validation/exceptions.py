#Custom class of exception to handle verification errors.
class VerificationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
