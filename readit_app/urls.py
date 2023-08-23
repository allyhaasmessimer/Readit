from django.urls import path
from . import views
# from .views import UserProfile
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("hello/", views.HelloView.as_view(), name="hello"),
    # path("api-token-auth/", views.CustomAuthToken.as_view(), name="api_token_auth"),
    # path("signup/", views.SignUpView.as_view(), name="signup"),
    # path('user/profile/<str:username>/', UserProfile.as_view(), name='user-profile'),
]
