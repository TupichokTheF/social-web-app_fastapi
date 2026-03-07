

class ServiceException(Exception):
    pass

class WrongEmail(ServiceException):

    def __init__(self, email):
        super().__init__(f"This email already used: {email}")