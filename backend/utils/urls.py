from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView

app_name = 'urls'

token_generation = [
    # JWT Token generation endpoint
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Token refresh endpoint
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = (
        token_generation
)
