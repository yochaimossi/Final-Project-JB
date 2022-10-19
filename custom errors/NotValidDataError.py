class NotValidDataError(Exception):
    def __init__(self, msg="The data that was sent is not valid"):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}'