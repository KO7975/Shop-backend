from django.urls import path, include
from .views import RegisterView, EmailVerifyView

app_name = 'authentication'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register' ),
    path('register/veryfy', EmailVerifyView.as_view(), name='register_verify' ),

]