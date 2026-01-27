#Custom class of exception to handle verification errors.
class VerificationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
