from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class ContestError(APIException):
    pass


class ContestInactiveError(ContestError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    title = 'Contest is not active'


class ContestMissingError(ContestError):
    status_code = status.HTTP_400_BAD_REQUEST
    title = 'Missing contest'
    default_detail = 'Contest must be provided as query parameter.'


class ContestNotFoundError(ContestError):
    status_code = status.HTTP_404_NOT_FOUND
    title = 'Contest not found'


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and isinstance(exc, ContestError):
        response.data = {'error': {'status': str(exc.status_code), 'title': exc.title, 'detail': exc.detail}}
    return response
