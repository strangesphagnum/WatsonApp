class TooManyAttemptsError(Exception):
    def __init__(self):
        self.message = "User should wait for 24 hours before the next genome scan"
