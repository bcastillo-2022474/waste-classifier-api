class UserNotFoundException(Exception):
    """
    Error when the user is not found
    """
    pass

class UserAlreadyExistsException(Exception):
    """
    Error when the user already exists
    """
    pass

class UnableToCreateUserException(Exception):
    """
    Error when the user is not created
    """
    pass

class PasswordsDoNotMatchException(Exception):
    """
    Error when the passwords do not match
    """
    