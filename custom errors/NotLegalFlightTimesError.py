class NotLegalFlightTimesError(Exception):
    def __init__(self, msg="Time must be more than 1 hour"):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}'