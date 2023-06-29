from rest_framework import serializers
from django.db import models
from .models import Product, OrderItem, Order, ShippingAddres
from rest_framework.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','complete', 'transaction_id', 'status')


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = OrderSerializer()
    # email = models.CharField(max_length=100)
    # order = OrderSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'order')


class OrderShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddres
        fields = ('id', 'order', 'customer','adress', 'city', 'stat', 'zipcode')


