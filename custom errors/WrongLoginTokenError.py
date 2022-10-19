class WrongLoginTokenError(Exception):
    def __init__(self, msg="The login token is invalid."):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}'