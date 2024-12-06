from utils.importinglibs.views import *
from django.contrib.auth import authenticate


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Extract email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user using provided credentials
        user = authenticate(email=email, password=password)

        if user is None:
            # Return an error response if authentication fails
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Proceed with token generation
        response = super().post(request, *args, **kwargs)

        # Include user information in the response
        return Response({
            'access': response.data['access'],
            'refresh': response.data['refresh'],
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.first_name + ' ' + user.last_name,
            }
        }, status=status.HTTP_200_OK)


# Standard TokenRefreshView for refreshing tokens
class CustomTokenRefreshView(TokenRefreshView):
    pass  # Using default behavior from SimpleJWT
