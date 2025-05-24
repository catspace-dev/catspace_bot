class AppException(Exception):

    def __init__(self, reason: str):
        self.reason = reason

