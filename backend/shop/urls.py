from django.urls import path
from .views import(
    OrderItemDetailView,
    OrderTotalPriceView,
    OrderItemDeleteView,
    OrderShippingAdressView,
)   


urlpatterns = [
    path('', OrderItemDetailView.as_view(), name='cart-detail'),

    path('total-price', OrderTotalPriceView.as_view(), name='cart-total-price'),

    path('remove/<int:pk>', OrderItemDeleteView.as_view(), name='remove'),
    
    path('adress', OrderShippingAdressView.as_view(), name='adress'),
]