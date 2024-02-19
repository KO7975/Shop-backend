from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
    )
from .models import (
    Product,
    Category,
    Stock,
    Comment,
    ProductAttribute,
    Attribute,
    Like,
    DisLike
    )


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


class AttributeSerializer(ModelSerializer):
    class Meta:
        model= Attribute
        fields = (
            'id',
            'name',
        )


class PropertiesSerializer(ModelSerializer):
    attribute = AttributeSerializer()
    class Meta:
        model = ProductAttribute
        fields =(
            'id',
            'attribute',
            'value',
        )


class ProductSerializer(ModelSerializer):
    categoty_id_id = CategorySerializer()
    properties = PropertiesSerializer(many=True)
    likes = SerializerMethodField()
    dislikes = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'description',
            'image',
            'categoty_id_id',
            'properties',
            'likes',
            'dislikes',
            'created',
            'updated',
            )

    def get_likes(self, obj):
        return obj.likes.count()

    def get_dislikes(self, obj):
        return obj.dislikes.count()
    

class CommentSerializer(ModelSerializer):
    likes = SerializerMethodField()
    dislikes = SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'product',
            'content',
            'created_at',
            'likes',
            'dislikes',
            )

    def get_likes(self, obj):
        return obj.likes.count()

    def get_dislikes(self, obj):
        return obj.dislikes.count()



class StockSerializer(ModelSerializer):

    class Meta:
        model = Stock
        fields = (
            'ptoduct_id_id',
            'quantity',
            'weight',
            'demensions',
            'defective',
            'created',
            'updated',
            )
        

class ProductLikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class ProductDisLikeSerializer(ModelSerializer):
    class Meta:
        model = DisLike
        fields = '__all__'


class TopNew10ProdactsResponseSerializer(ModelSerializer):
    new_10 = ProductSerializer(many=True)
    top_10 = ProductSerializer(many=True)

    class Meta:
        model = Product
        fields = ('new_10', 'top_10')


class CommentRequestSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'product')
