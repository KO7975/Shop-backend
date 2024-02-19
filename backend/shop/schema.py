from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiExample
)


QUANTITY_PARAMETER =OpenApiParameter(
    name='quantity',
    required=True,
    description='Product Quantity',
)

ORDER_STATUS_POST_PARAM = OpenApiParameter(
    name='order_key',
    type=dict,
    examples=[
        OpenApiExample(
            name='order_key',
            request_only=True,
            value={'order_key': 'int'}
        )
    ]
)

ORDER_STATUS_PUT_PARAM = OpenApiParameter(
    name='data',
    type=dict,
    examples=[
        OpenApiExample(
            name='data',
            request_only=True,
            value={'order_key': 'int', 'status': 'str'}
        )                       
    ]
)

CITY_PARAMETER = OpenApiParameter(
    name='city',
    type=dict,
    examples=[
    OpenApiExample('city', value={'city': 'str'})
    ]
)

PAY_DATA_PARAMS = OpenApiParameter(
    name='data',
    type=dict,
    examples=[
        OpenApiExample(
            description='Order information',
            name='data',
            value={'amount':'int', 'order_id': 'int', 'carrency': 'str'},
            request_only=True
        )
    ]
)

