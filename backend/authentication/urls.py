from django.urls import path, include
from .views import (
    RegisterView,
    EmailVerifyView,
    FacebookLogin, 
    GoogleLogin
    )

app_name = 'authentication'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register' ),
    path('register/veryfy', EmailVerifyView.as_view(), name='register_verify' ),
    path('login/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('login/google/', GoogleLogin.as_view(), name='google_login'),
]