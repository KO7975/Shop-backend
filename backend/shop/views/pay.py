from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from liqpay import LiqPay
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    )
from shop.schema import PAY_DATA_PARAMS


class PayView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        description='Order payment information',
        parameters=[PAY_DATA_PARAMS],
        responses={
            200: OpenApiResponse(
                description="Return parameters {'signature': signature, 'data': data}"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        amount = request.data['amount']
        order_id = request.data['order_id']
        carrency = request.data['carrency']
        params = {
            'action': 'pay',
            'amount': amount,
            'currency': carrency,
            'description': 'Payment for clothes',
            'order_id': order_id,
            'version': '3',
            'sandbox': 0, # sandbox mode, set to 1 to enable it
            # 'server_url': 'https://test.com/billing/pay-callback/', # url to callback view
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return Response( {'signature': signature, 'data': data})


class PayCallbackView(APIView):
    permission_classes = [permissions.AllowAny]
        
    @extend_schema(
        description='Order payment Callback',
        parameters=[PAY_DATA_PARAMS],
        responses={
            200: OpenApiResponse(description="return {'data': response}")
        }        
    )
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.data['data']
        signature = request.data['signature']

        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)
        
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        return Response({'data': response})