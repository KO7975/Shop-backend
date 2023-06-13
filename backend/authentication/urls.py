from django.urls import path
from .views import RegisterView, VerifyView#, LoginView, LogoutView, GetUsers, GetUser

app_name = 'authentication'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register' ),
    # path('verifi', VerifyView.as_view(), name='verifi'),
    # path('login', LoginView.as_view(), name='login'),
    # path('logout', LogoutView.as_view(), name='logout'),
    # path('getusers', GetUsers.as_view(), name='get_users'),
    # path('getuser/', GetUser.as_view(), name='user_view'),
    # path('getuser/<int:pk>', GetUser.as_view(), name='user_actions'),
]