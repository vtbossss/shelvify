from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Retrieve the access token from cookies
        access_token = request.COOKIES.get('access_token')
        
        if access_token:
            try:
                # Decode and validate the access token
                token = AccessToken(access_token)
                user_id = token['user_id']
                user = get_user_model().objects.get(id=user_id)
                request.user = user  # Set the user from the token
            except Exception as e:
                # If there's an issue with the token, set user as AnonymousUser
                request.user = AnonymousUser()
                # Optional: Log or handle the error here
                print(f"JWT Authentication failed: {e}")
        else:
            request.user = AnonymousUser()  # No token, set user as AnonymousUser

        # Proceed with the request
        response = self.get_response(request)
        return response
