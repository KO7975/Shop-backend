from rest_framework.fields import empty
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
    )

from .models import (
    Product,
    Category,
    Stock,
    Comment
    )


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'image',
            'categoty_id',
            'atr',
            'created',
            'updated',
            )



class CommentSerializer(ModelSerializer):
    likes_count = SerializerMethodField()
    dislikes_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'product',
            'content',
            'created_at',
            'likes_count',
            'dislikes_count',
            )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_dislikes_count(self, obj):
        return obj.dislikes.count()



class CategorySerializer(ModelSerializer):

    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        children = Category.objects.filter(children=obj)
        serializer = CategorySerializer(children, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = (
            'id',
            'slug',
            'children',
            'image',
            )


class StockSerializer(ModelSerializer):

    class Meta:
        model = Stock
        fields = (
            'ptoduct_id',
            'quantity',
            'weight',
            'demensions',
            'price',
            'defective',
            'created',
            'updated',
            )