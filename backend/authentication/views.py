from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from .models import User
from .serializer import UserSerializer, EmailVerifySerializer
from rest_framework.permissions import AllowAny
import jwt
import smtplib
from email.message import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample, OpenApiRequest



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
    message['Subject'] = 'Підтвердженя аутентифікації PINI PINO'
    message['From'] = smtp_username
    message['To'] = recipient_email

    message.set_content(f'Для підтвердженря аутентифікації перейдіть за посиланням: http://127.0.0.1:8000/auth/register/apruve?token={token}&email={recipient_email}')

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)



class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserSerializer,
        methods=["POST"],
        parameters=[
            OpenApiParameter(name='email', description='Email adress', required=True),
            OpenApiParameter(name='password', description='Password', required=True),
            ],
        description="Registration form.\
        Takes a set of user credentials and sent message to user email adress\
        with refresh JSON web token to prove the authentication of those credentials.",
        responses={200: OpenApiResponse(description='Registration saccess. User get email with attached link for access'),
                   201: OpenApiResponse(description='Email allready in db')}
    )
    def post(self, request):
        data = request.data
        email = data['email']
        data = dict(data)
        data2 = { key: value[0] for key, value in data.items() if type(value)==list}

        if len(data2)>0:
            data = data2

        if not User.objects.filter(email=email).exists():
            data['is_active'] = False
            user = User.objects.create_user(**data)
            token = get_tokens_for_user(user)
            # Send RefreshToken to email
            send_email_with_token(str(token['refresh']), email)

            return Response({'message': 'Registration saccess. Check mail.'})
        
        return Response({'message': 'Email allready in db'}, status=201)
    


class EmailVerifyView(APIView):
        permission_classes = [AllowAny]

        @extend_schema(
                parameters=[
                    OpenApiParameter(
                        name='data',
                        type=dict,
                        examples=[
                            OpenApiExample(
                                'data',
                                value={'token': 'token data', 'email': 'user@email.com'},
                                request_only=True,
                            ),
                        ]
                    ),
                ],
                description='User mail upproved from email. Make user is_active = True',
                methods=["GET"],
                responses={
                    200:OpenApiResponse( description='return token: refresh, access',),
                    400:OpenApiResponse(description='Token not valid'),
                    500:OpenApiResponse(description='UserDoesNotExist')
                }
        )
        def get(self, request):
            token = request.GET.get('token')
            email = request.GET.get('email' )

            try:
                refresh = RefreshToken(token)
                access = refresh.access_token
                data = {
                    "refresh" :str(refresh),
                    "access": str(access)
                    }
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=payload['user_id'])
                user.is_active = True
                user.save()
                return Response({'message': 'Valid access', 'token': data})
            
            except User.DoesNotExist as e:
                user = User.objects.get(email = email)
                user.delete()
                return Response({'message': f'{e}'}, status=500)




# class FacebookLogin(APIView):
#     @psa()
#     def post(self, request, backend):
#         token = request.data.get('access_token')
#         user = request.backend.do_auth(token)

#         if user:
#             return Response(get_tokens_for_user(user))
#         else:
#             return Response({'error': 'Invalid token'}, status=400)
        

# class GoogleLogin(APIView):
#     @psa()
#     def post(self, request, backend):
#         token = request.data.get('access_token')
#         user = request.backend.do_auth(token)

#         if user:
#             return Response(get_tokens_for_user(user))
#         else:
#             return Response({'error': 'Invalid token'}, status=400)
        



