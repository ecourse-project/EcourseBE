from django.urls import path
from apps.users_auth.api import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("registration/", views.RegisterUserAPIView.as_view(), name="custom_register"),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]