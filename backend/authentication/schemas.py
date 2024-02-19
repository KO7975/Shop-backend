from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiExample
)

REGISTER_VIEW_DESCRIPTION = "Registration form.\
        Takes a set of user credentials and sent message to user email adress\
        with refresh JSON web token to prove the authentication of those credentials."

EMAIL_VERIFY_PARAMETER = OpenApiParameter(
        name='data',
        type=dict,
        examples=[
                OpenApiExample(
                'data',
                value={'token': 'token data', 'email': 'user@email.com'},
                request_only=True,
                )
        ]
)