from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .serializer import UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
import jwt
import smtplib
from email.message import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.parsers import JSONParser
from .serializer import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class =MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_email_with_token(token, recipient_email):
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    message = EmailMessage()
    message['Subject'] = 'Подтверждение аутентификации'
    message['From'] = smtp_username
    message['To'] = recipient_email

    # Тело сообщения с токеном
    message.set_content(f'Для подтверждения аутентификации перейдите по ссылке: http://127.0.0.1:8000/token/verify?token={token}')

    # Отправка сообщения 
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)




class RegisterView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        email = data['email']

        if len(User.objects.filter(email=email)) == 0:
            user = User.objects.create_user(**data)
            # Создание RefreshToken
            token = RefreshToken.for_user(user) 
            # Отправка RefreshToken на почту
            send_email_with_token(str(token), email)

            return Response({'message': 'Registration saccess.\
                            Пожалуйста, проверьте свою электронную почту для подтверждения.',
                            }, status=status.HTTP_201_CREATED)
        return Response({'message': 'Email allready in db'})


class VerifyView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            refresh = RefreshToken(token)
            access = refresh.access_token

            # Перенаправление пользователя на страницу подтверждения аутентификации с access token
            return Response({'message': 'Valid access', 'token': access}).set_cookie(key='token', value=access)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user =User.objects.filter(email=email).first()

#         if user is None:
#             raise AuthenticationFailed('User not found')
#         # login(request, user)

#         if  check_password(password, user.password) or  password==user.password:
#             token = RefreshToken.for_user(user)
#             response = Response()
#             response.data = {
#                 'message': 'login saccess',
#             }
#             response.set_cookie(key='token', value=token)
#             return response
        
#         raise AuthenticationFailed('Incorrect password')


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self,request):
#         response = Response()
#         response.delete_cookie("token")
#         response.data = {
#             "message": "Logout success"
#         }
#         return response
    

# class GetUser(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         token = request.COOKIES.get('token')

#         payload = jwt.decode(
#             token,
#             settings.SIMPLE_JWT['SIGNING_KEY'],
#             algorithms=[settings.SIMPLE_JWT['ALGORITHM']],
#             )
    
#         user = User.objects.filter(id=payload['user_id']).first()
#         serializer = UserSerializer(user)
#         data = serializer.data

#         return Response({"data":data})
    

#     def put(self, request, pk):        
#         user  =User.objects.filter(id=pk)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
    

#     def delete(self, request, pk):        
#         user = User.objects.filter(id=pk)
#         if user is None:
#             return Response({"message": "User not found"})
#         user.delete()
#         return Response({"message":"User deleted saccess"}, status=status.HTTP_204_NO_CONTENT)

    
# class GetUsers(APIView):
#     permission_classes = (IsAuthenticatedOrReadOnly,)

#     def get(self, request):
#         token = request.COOKIES.get('token')
#         if not token:
#             raise AuthenticationFailed("Unauthenticated")
#         users = User.objects.all().values()
#         return Response({"users": list(users)})
        



