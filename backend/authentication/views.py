import jwt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import psa
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)
from django.conf import settings

from authentication.serializer import UsersSerializer, SocialAuthSerializer
from authentication.models import User
from authentication.services import get_tokens_for_user, send_email_with_token
from authentication.schemas import *


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UsersSerializer,
        methods=["POST"],
        description = REGISTER_VIEW_DESCRIPTION,
        responses={
            200: OpenApiResponse(
                description='Registration saccess.User get email with attached link for access'),
            400: OpenApiResponse(description='User allready in db')
        }
    )
    def post(self, request):
        data = request.data
        email = data.get('email')
        phone = data.get('phone')
        data = dict(data)
        data2 = { key: value[0] for key, value in data.items() if type(value)==list}

        if len(data2)>0:
            data = data2

        if not User.objects.filter(email=email, phone=phone).exists():
            data['is_active'] = False
            user = User.objects.create_user(**data)
            token = get_tokens_for_user(user)
            # Send RefreshToken to email
            server_path = request.build_absolute_uri()
            send_email_with_token(str(token['refresh']), email, server_path)

            return Response({'message': 'Registration saccess. Check mail.'}, status.HTTP_200_OK)
        return Response({'message': 'User allready in db'}, status.HTTP_400_BAD_REQUEST)


class EmailVerifyView(APIView):
        permission_classes = [AllowAny]

        @extend_schema(
                parameters=[EMAIL_VERIFY_PARAMETER],
                description='User mail upproved from email. Make user is_active = True',
                methods=["GET"],
                responses={
                    200:OpenApiResponse( description='return token: refresh, access',),
                    400:OpenApiResponse(description='Token not valid'),
                    404:OpenApiResponse(description='UserDoesNotExist')
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
                return Response({'message': 'Valid access', 'token': data}, status.HTTP_200_OK)
            
            except User.DoesNotExist as e:
                user = User.objects.get(email = email)
                user.delete()
                return Response({'message': f'{e}'}, status.HTTP_404_NOT_FOUND)



class FacebookLogin(APIView):
    @psa()
    @extend_schema(request=SocialAuthSerializer,
                   responses={200: "Success", 400: "Invalid token"})
    def post(self, request, backend):
        token = request.data.get('access_token')
        user = request.backend.do_auth(token)

        if user:
            return Response(get_tokens_for_user(user), status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token'}, status.HTTP_400_BAD_REQUEST)
        

class GoogleLogin(APIView):
    @psa()
    @extend_schema(request=SocialAuthSerializer,
                   responses={200: "Success", 400: "Invalid token"})
    def post(self, request, backend):
        token = request.data.get('access_token')
        user = request.backend.do_auth(token)

        if user:
            return Response(get_tokens_for_user(user), status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token'}, status.HTTP_400_BAD_REQUEST)
        