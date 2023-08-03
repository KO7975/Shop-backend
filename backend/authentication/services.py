from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from email.message import EmailMessage
import smtplib


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
