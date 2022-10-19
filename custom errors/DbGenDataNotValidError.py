class DbGenDataNotValidError(Exception):
    def __init__(self, msg="The data sent to the database generator is not valid"):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}'