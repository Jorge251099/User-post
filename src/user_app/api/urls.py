from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegistrationView , LogoutView, LoginAV
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

app_name = 'user-app'

urlpatterns = [
  path('login/',obtain_auth_token , name='login'),
  path('login-app/',LoginAV.as_view(), name='login-app'),
  path('register/',RegistrationView.as_view(), name='register'),
  path('logout/',LogoutView.as_view(),name='logout'),

  path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
  path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]
