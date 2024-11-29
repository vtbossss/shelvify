from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Initialize the middleware with the next response handler

    def __call__(self, request):
        # Retrieve the access token from the cookies. It's assumed the token is stored securely in the cookie.
        access_token = request.COOKIES.get('access_token')
        
        if access_token:
            try:
                # Decode and validate the access token using the simplejwt AccessToken class
                token = AccessToken(access_token)
                user_id = token['user_id']  # Extract the user ID from the decoded token
                
                # Ensure the user exists in the database
                user = get_user_model().objects.get(id=user_id)
                
                # Set the user in the request to be used in views or other middleware
                request.user = user
            except Exception as e:
                # If decoding or validation fails, set the user as AnonymousUser for security
                request.user = AnonymousUser()  # User should not be authenticated in case of errors
                # Log the exception for debugging purposes (important for security)
                print(f"JWT Authentication failed: {e}")
        else:
            # If there's no token in the cookies, set the user as AnonymousUser (unauthenticated)
            request.user = AnonymousUser()

        # Allow the request to continue to the next middleware or view
        response = self.get_response(request)
        return response
