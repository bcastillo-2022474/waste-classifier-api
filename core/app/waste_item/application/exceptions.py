class EmptyImageException(Exception):
    """
    Error when Image size is zero
    """

class UnableToProcessImageException(Exception):
    """
    Error when the repository is unable to process the image
    """

class UnableToSaveImageException(Exception):
    """
    Error when the image repository is unable to save the image
    """
class WasteItemNotFoundException(Exception):
    """
    Error when the waste item is not found in the repository
    """
class UserNotFoundException(Exception):
    """
    Error when the user is not found in the repository
    """