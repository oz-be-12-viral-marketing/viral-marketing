from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # First, try to get the token from the cookie
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            # If not in cookie, fall back to the default method (Authorization header)
            return super().authenticate(request)

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
