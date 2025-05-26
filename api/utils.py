from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_str
from pydantic import ValidationError as PydanticValidationError
from rest_framework import status
from core.app.user.application.exceptions import UserNotFoundException, UnableToCreateUserException, \
    UserAlreadyExistsException, UnauthorizedUserException
from core.app.waste_item.application.exceptions import UnableToProcessImageException, UnableToSaveImageException, \
    EmptyImageException, WasteItemNotFoundException

errors = [
    (DjangoValidationError, status.HTTP_400_BAD_REQUEST),
    (PydanticValidationError, status.HTTP_400_BAD_REQUEST),
    (EmptyImageException, status.HTTP_400_BAD_REQUEST),
    (UnableToProcessImageException, status.HTTP_500_INTERNAL_SERVER_ERROR),
    (UnableToSaveImageException, status.HTTP_500_INTERNAL_SERVER_ERROR),
    (UserNotFoundException, status.HTTP_404_NOT_FOUND),
    (UnableToCreateUserException, status.HTTP_400_BAD_REQUEST),
    (UserAlreadyExistsException, status.HTTP_409_CONFLICT),  # Conflict
    (WasteItemNotFoundException, status.HTTP_404_NOT_FOUND),
    (UnauthorizedUserException, status.HTTP_401_UNAUTHORIZED),

    # THIS 2 MUST BE LAST ALWAYS
    (ValueError, status.HTTP_400_BAD_REQUEST),
    (Exception, status.HTTP_500_INTERNAL_SERVER_ERROR),
]


def _extract_error_detail(error):
    if isinstance(error, DjangoValidationError):
        return error.messages

    if isinstance(error, PydanticValidationError):
        # convert pydantic dict list to str list
        return [f"{e['loc'][0]}: {e['msg']}" for e in error.errors()]

    if hasattr(error, 'message'):
        return [error.message]

    return [force_str(error)]


def _gen_pretty_error(error: Exception):
    return {
        'code': type(error).__name__,
        'detail': _extract_error_detail(error)
    }


def get_error_status_code_from_exception(raised_exception: Exception):
    for exception_class, status_code in errors:
        if isinstance(raised_exception, exception_class):
            return status_code, _gen_pretty_error(raised_exception)

    return status.HTTP_500_INTERNAL_SERVER_ERROR, _gen_pretty_error(raised_exception)
