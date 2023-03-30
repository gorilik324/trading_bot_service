import jwt
from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from apps.users.models import User


class JWTAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            if username is None or password is None:
                return
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return
            if user.check_password(password):
                return user
        else:
            try:
                # Decode the JWT token and extract the user ID from it
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']

                # Return the user with the given ID if it exists
                try:
                    return User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    return None

            except jwt.exceptions.PyJWTError as e:
                # Log the error and return None if there was an issue decoding the token
                print(f'JWT decode error: {e}')
                return None

    def get_user(self, user_id):
        # Return the user with the given ID if it exists
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
