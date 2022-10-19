class WrongLoginDataError(Exception):
    def __init__(self, msg="Wrong username or password."):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}'