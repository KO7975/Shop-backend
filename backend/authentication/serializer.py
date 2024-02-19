from rest_framework import serializers
from .models import User
from django.db import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        token['email'] = user.email
        return token


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'email',
            'phone',
            'password'
        ]


class EmailVerifySerializer(serializers.ModelSerializer):
    token = models.CharField(max_length=555)
    email = models.CharField(max_length=100)

    class Meta():
        model = User
        fields = ['token', 'email']


class SocialAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()
