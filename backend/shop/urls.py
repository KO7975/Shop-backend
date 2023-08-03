from django.urls import path
from .views.order import (
    OrderItemDetailView,
    OrderTotalPriceView,
    OrderItemDeleteView,
    OrderShippingAdressView,
    OrderItemQuantityChangeView,
    AddToOrderView,
    OrderConfirmView,
    OrderStatusView,
)
from .views.NP import (
    NPCity,
    NPAreas,
    NPWarehouses,
)
from .views.pay import(
    PayView,
    PayCallbackView,
)   


urlpatterns = [
    path('', OrderItemDetailView.as_view(), name='cart-detail'),
    path('new-quantity/<int:product_id>', OrderItemQuantityChangeView.as_view(), name='change_quantity'),
    path('add-to-cart/<int:product_id>', AddToOrderView.as_view(), name='add_to_cart'),
    path('total-price', OrderTotalPriceView.as_view(), name='cart_total_price'),
    path('remove/<int:pk>', OrderItemDeleteView.as_view(), name='remove'),
    path('adress', OrderShippingAdressView.as_view(), name='adress'),
    path('confirm', OrderConfirmView.as_view(), name='order_confirm'),
    path('status', OrderStatusView.as_view(), name='order_status'),

    path('np/areas', NPAreas.as_view(), name='np_areas'),
    path('np/city', NPCity.as_view(), name='np_city'),
    path('np/warehouses', NPWarehouses.as_view(), name='np_warehouses'),

    path('pay/', PayView.as_view(), name='pay_view'),
    path('pay-callback/', PayCallbackView.as_view(), name='pay_callback'),

]