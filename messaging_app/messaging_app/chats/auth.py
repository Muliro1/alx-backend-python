from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomHeaderAuthentication(BaseAuthentication):
    """
    Custom authentication using a custom header 'X-USER-ID'.
    """
    def authenticate(self, request):
        user_id = request.headers.get('X-USER-ID')
        if not user_id:
            return None  # No authentication header, move to next authentication class

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)

# Utility function for manual authentication
def authenticate_user(username, password):
    """
    Authenticate a user by username and password.
    Returns the user if credentials are valid, else None.
    """
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None
    return None
