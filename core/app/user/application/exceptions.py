class UserNotFoundException(Exception):
    """
    Error when the user is not found
    """
    pass

class UserAlreadyExists(Exception):
    """
    Error when the user already exists
    """
    pass

class UnableToCreateUser(Exception):
    """
    Error when the user is not created
    """
    pass