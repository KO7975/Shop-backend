from rest_framework import serializers
from .models import Product, OrderItem, Order, ShippingAddres
from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','complete', 'transaction_id', 'status', 'calculate_total_price')


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer(many=True)
    order_id = OrderSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product_id', 'quantity', 'order_id')


class OrderShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddres
        fields = ('id', 'order', 'customer','adress', 'city', 'stat', 'zipcode')


