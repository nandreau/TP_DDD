from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

class APIException(Exception):
    def __init__(self, error_type, detail, status_code=None):
        self.error_type = error_type
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

def create_error_response(error_type, detail, status_code=None):
    """
    Crée une réponse d'erreur standardisée
    """
    if status_code is None:
        if error_type == 'Resource not found':
            status_code = status.HTTP_404_NOT_FOUND
        elif error_type == 'Validation error':
            status_code = status.HTTP_400_BAD_REQUEST
        elif error_type == 'Permission denied':
            status_code = status.HTTP_403_FORBIDDEN
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return Response({
        'error': error_type,
        'detail': detail
    }, status=status_code)

def custom_exception_handler(exc, context):
    """
    Gestionnaire d'exceptions personnalisé pour l'API
    """
    # Appel du gestionnaire d'exceptions par défaut
    response = exception_handler(exc, context)

    if response is not None:
        # Personnalisation des messages d'erreur
        if isinstance(exc, ObjectDoesNotExist):
            response.data = {
                'error': 'Resource not found',
                'detail': str(exc)
            }
        elif isinstance(exc, IntegrityError):
            response.data = {
                'error': 'Database integrity error',
                'detail': str(exc)
            }
        elif isinstance(exc, ValueError):
            response.data = {
                'error': 'Validation error',
                'detail': str(exc)
            }
        elif isinstance(exc, KeyError):
            response.data = {
                'error': 'Missing required field',
                'detail': f"Field '{str(exc)}' is required"
            }
        elif isinstance(exc, PermissionError):
            response.data = {
                'error': 'Permission denied',
                'detail': str(exc)
            }
        elif isinstance(exc, APIException):
            response.data = {
                'error': exc.error_type,
                'detail': exc.detail
            }
            if exc.status_code:
                response.status_code = exc.status_code
        else:
            response.data = {
                'error': 'Unexpected error',
                'detail': str(exc)
            }

    return response

def handle_api_error(func):
    """
    Décorateur pour gérer les exceptions dans les vues API
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist as e:
            return create_error_response('Resource not found', str(e))
        except IntegrityError as e:
            return create_error_response('Database integrity error', str(e))
        except ValueError as e:
            return create_error_response('Validation error', str(e))
        except KeyError as e:
            return create_error_response('Missing required field', f"Field '{str(e)}' is required")
        except PermissionError as e:
            return create_error_response('Permission denied', str(e))
        except APIException as e:
            return create_error_response(e.error_type, e.detail, e.status_code)
        except Exception as e:
            return create_error_response('Unexpected error', str(e))
    return wrapper
