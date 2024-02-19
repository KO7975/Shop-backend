from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .services import get_top_10_products, get_new_added
from drf_spectacular.utils import extend_schema
from product.serializer import (
    CommentSerializer,
    ProductSerializer,
    CategorySerializer,
    StockSerializer,
    CommentRequestSerializer,
)
from .models import (
    Product,
    Stock, 
    Category,
    Like,
    DisLike,
    Comment,
    CommentLike,
    CommentDislike,
)
from product.schemas import *


class ProductsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductsView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    pagination_class = ProductsPagination

    @extend_schema(
            description='Get all products',
            responses=ProductSerializer(many=True),
    )
    def get(self, request):
        products = self.paginate_queryset(self.get_queryset())

        serializer1 = ProductSerializer(products, many=True)

        return self.get_paginated_response(serializer1.data)


class TopNew10ProdactsView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny, )

    @extend_schema(
        description = 'Return new 10 products and top 10 products',
        methods=["GET"],
        responses={200:TOP_NEW_10_PRODUCTS_200_RESPONSE}        
    )
    def get(self, request, *args, **kwargs):
        top_10 = get_top_10_products()
        new_10 = get_new_added()
        data = {}
        data['new_10'] = self.get_serializer(new_10, many=True).data
        data['top_10'] = self.get_serializer(top_10, many=True).data

        return Response(
            data,
            status=status.HTTP_200_OK
        )


class ProductView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = ProductSerializer


    @extend_schema(
            description = 'Return product details from product_id',
            methods=["GET"],
            parameters=[PRODUCT_ID_PARAMETER],
            responses=PRODUCT_GET_RESPONSES
    )
    def get(self, request):
        try:
            product_id = request.query_params.get('product_id')
            product = Product.objects.filter(id=product_id)
            serializer = ProductSerializer(product, many=True)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        except Product.DoesNotExist:
            return Response(
                {'message': 'product not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        
class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer


    @extend_schema(
            description="Create comment for product",
            methods=['POST'],
            request=CommentRequestSerializer,
            responses=COMMENT_POST_RESPONSES           
    )
    def post(self, request):
        product_id = request.data.get('product')
        product = Product.objects.filter(id=product_id)

        if not product.exists():
            return Response(
                {"message": "Product not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        comment = request.data.get('content')
        comment = Comment.objects.create(
            user=request.user,
            product=product.first(),
            content= comment,
            )
        return Response(
            {'message': 'comment created'},
            status=status.HTTP_201_CREATED
        )
        

    @extend_schema(
            description='Get comment from product_id',
            parameters=[PRODUCT_ID_PARAMETER],
            responses=COMMENT_GET_RESPONSES
    )
    def get(self, request):
        try:
            product_id = request.query_params.get('product_id')
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comment = Comment.objects.filter(product=product)
        serializer = CommentSerializer(comment, many=True)

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )
    
           
class CategoryView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

    @extend_schema(
            description='Categories description',
            responses={200:CATEGORY_200_RESPONSE}
    )
    def get(self, request):
        categories = Category.objects.all().values()
        cat = []

        for i in categories:
            if i['perent_id_id'] == None:
                cat.append(i['id'])

        category = Category.objects.in_bulk(id_list=cat, field_name='id').values()
        serializer = CategorySerializer(category, many=True)

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )


class ProductCategoryView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

    @extend_schema(
            description='Product from category',
            parameters=PRODUCT_CATEGORY_PARAMS,
            responses={
                200: PRODUCT_CATEGORY_200_RESPONSE
            }
    )
    def get(self, request):
        category_id = request.query_params.get('category_id')
        category_products = Product.objects.filter(categoty_id_id=category_id)
        category = Category.objects.filter(perent_id_id=category_id)

        sub_categories = {i.id: i.name for i in category}
        sub_category_products = {i.id: ProductSerializer(Product.objects.filter(categoty_id_id=i.id), many=True).data
                                  for i in category if i.id != category_id}
                                           
        serializer1 = ProductSerializer(category_products, many=True)

        return Response({
            'sub_categories': sub_categories,
            'category_products': serializer1.data,
            'sub_category_products': sub_category_products,
            })
        

class StockView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = StockSerializer

    @extend_schema(
            description='Get Product data',
            parameters=[PRODUCT_ID_PARAMETER],
            responses=STOCK_RESPONSES
    )
    def get(self, request):
        try:
            product_id = request.query_params.get('product_id')
            product = Product.objects.get(id=product_id)
            stock = Stock.objects.filter(ptoduct_id=product).values().first()
            serializer = StockSerializer(stock)

            return Response(
                {'name':product.name, 'data': serializer.data},
                status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'{e}'},
                status.HTTP_400_BAD_REQUEST
            )


class ProductLikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    @extend_schema(
            description= 'Product like save',
            parameters=[PRODUCT_ID_PARAMETER],
            responses= PRODUCT_LIKE_RESPONSES
    )
    def post(self, request):
        try:
            product_id = request.query_params.get('product_id')
            product = Product.objects.get(id=product_id)

            if Like.objects.filter(user=request.user, product=product).exists():
                return Response({"message": "You have already liked this product."})
            
            elif DisLike.objects.filter(user=request.user, product=product).exists():
                DisLike.objects.filter(user=request.user, product=product).delete()
            
            like, created = Like.objects.get_or_create(user=request.user, product=product)

            return Response(
                {"message": "Product liked successfully."},
                status.HTTP_201_CREATED
            )

        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found."},
                status.HTTP_400_BAD_REQUEST
            )
        

class ProductDislikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    @extend_schema(
            description= 'Product disliked ',
            parameters=[PRODUCT_ID_PARAMETER],
            responses= PRODUCT_DISLIKE_RESPONSES
    )
    def post(self, request):
        try:
            product_id = request.query_params.get('product_id')
            product = Product.objects.get(id=product_id)

            if DisLike.objects.filter(user=request.user, product=product).exists():
                return Response({"message": "You have already disliked this product."})
            
            elif Like.objects.filter(user=request.user, product=product).exists():
                Like.objects.filter(user=request.user, product=product).delete()
            
            dislike = DisLike(user=request.user, product=product)
            dislike.save()

            return Response(
                {"message": "Product disliked successfully."},
                status=status.HTTP_200_OK
            )

        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found."},
                status=status.HTTP_400_BAD_REQUEST
            )


class LikeCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    @extend_schema(
            description= 'Comment liked ',
            parameters=[COMMENT_ID_PARAMETER],
            responses= LIKE_COMMENT_RESPONSES
    )
    def post(self, request):
        try:
            comment_id = request.query_params.get('comment_id')
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"message": "Comment not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if CommentLike.objects.filter(user=request.user, comment=comment).exists():  
            return Response(
                {"message": "You have already liked this comment."},
                status=status.HTTP_200_OK
            )     
        elif CommentDislike.objects.filter(user=request.user, comment=comment).exists():
            CommentDislike.objects.filter(user=request.user, comment=comment).delete()

        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)  

        return Response(
            {"message": "Comment liked successfully."},
            status=status.HTTP_201_CREATED
        )



class DislikeCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    @extend_schema(
            description= 'Comment disliked ',
            parameters=[COMMENT_ID_PARAMETER],
            responses= DISLIKE_COMMENT_RESPONSES
    )
    def post(self, request):
        try:
            comment_id = request.query_params.get('comment_id')
            comment = Comment.objects.get(id=comment_id)

            if CommentDislike.objects.filter(user=request.user, comment=comment).exists():
                return Response(
                    {"message": "You have already disliked this comment."},
                    status=status.HTTP_200_OK
                )
            
            elif CommentLike.objects.filter(user=request.user, comment=comment).exists():
                CommentLike.objects.filter(user=request.user, comment=comment).delete()
            
            dislike = CommentDislike(user=request.user, comment=comment)
            dislike.save()

            return Response(
                {"message": "Comment disliked successfully."},
                status=status.HTTP_201_CREATED
            )

        except Comment.DoesNotExist:
            return Response(
                {"message": "Comment not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
