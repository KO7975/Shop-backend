from rest_framework.serializers import ModelSerializer
from .models import Product, Category, Stock


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'categoty_id', 'atr', 'created', 'updated' ]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'products', 'perent_id']


class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = ['ptoduct_id', 'quantity', 'weight', 'demensions', 'price', 'defective', 'created', 'updated']