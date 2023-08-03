from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .services import get_top_10_products, get_new_added
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample
    )
from .serializer import (
    CommentSerializer,
    ProductSerializer,
    CategorySerializer,
    StockSerializer,
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


class ProductsView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
            description='Get all products',
            responses=ProductSerializer(many=True),
    )
    def get(self, request):
        products = Product.objects.all()
        top_10 = get_top_10_products()
        new_added = get_new_added()

        serializer1 = ProductSerializer(products, many=True)
        serializer2 = ProductSerializer(top_10, many=True) 
        serializer3 = ProductSerializer(new_added, many=True)

        return Response({
            'all_products': serializer1.data,
            'top_10': serializer2.data,
            'new_10': serializer3.data
            })
    

class ProductView(APIView):
    permission_classes = (AllowAny, )

    @extend_schema(
            description = 'Return product details from product_id',
            methods=["GET"],
            responses={
                200:OpenApiResponse(
                    description='Product details',
                    response=ProductSerializer
                ),
                500:OpenApiResponse(description='ProductDoesNotExist')
            },
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.filter(id=product_id)
            serializer = ProductSerializer(product, many=True)

            return Response({'product': serializer.data,})
        
        except Product.DoesNotExist:
            return Response({'message': 'product not found'}, status=500)

        
class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            description="Create comment for product",
            methods=['POST'],
            parameters= [
                OpenApiParameter(
                    name='content',
                    required=True,
                    description='Comment details',
                    type=dict,
                    examples=[ OpenApiExample(
                        'Example',
                        summary='Comment for product',
                        description='Comment for product from request user',
                        value={'content': 'Comment from form'},
                        request_only=True,
                        response_only=False
                    )] 
                )],
            responses={
                200: OpenApiResponse(description='Comment created'),
                500:OpenApiResponse(description= 'error description')
            }           
    )
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=500)
        
        try:
            comment = request.data['content']
            comment, created = Comment.objects.get_or_create(
                user=request.user,
                product=product,
                content= comment,
                )
            return Response({'message': 'comment created'}, status=200)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

    @extend_schema(
            description='Get comment from product_id',
            responses={200:OpenApiResponse(response=CommentSerializer, description= 'Comment from product_id'),}
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=500)
        
        comment = Comment.objects.filter(product=product)
        serializer = CommentSerializer(comment, many=True)

        return Response(serializer.data)
    
           
class CategoryView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
            description='Categories description',
            responses={
                200:OpenApiResponse(
                    response=CategorySerializer,
                    description='All categories'
                )
            }
    )
    def get(self, request):
        categories = Category.objects.all().values()
        cat = []

        for i in categories:
            if i['perent_id_id'] == None:
                cat.append(i['id'])

        category = Category.objects.in_bulk(id_list=cat, field_name='id').values()
        serializer = CategorySerializer(category, many=True)

        return Response(serializer.data)


class ProductCategoryView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
            description='Product from category',
            parameters=[
                OpenApiParameter('sub_categories', ProductSerializer, response=True),
                OpenApiParameter('category_products', ProductSerializer, response=True),
                OpenApiParameter('sub_category_products',  ProductSerializer, response=True)],
            responses={
                200: OpenApiResponse( description='Products from category', response=ProductSerializer,)
            }
    )
    def get(self, request, category_id):
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

    @extend_schema(
            description='Get Product data',
            responses={
                200: StockSerializer,
                500: OpenApiResponse(description='Error description')
            }
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            stock = Stock.objects.filter(ptoduct_id=product).values().first()
            print(stock)
            serializer = StockSerializer(stock)

            return Response({'name':product.name, 'data': serializer.data})
        except Exception as e:
            return Response({'error': f'{e}'}, status=500)


class ProductLikeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            description= 'Product like save',
            responses= {
                200: OpenApiResponse(description="Product liked successfully."),
                500: OpenApiResponse(description="Product not found.")
            }
    )
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            if Like.objects.filter(user=request.user, product=product).exists():
                return Response({"message": "You have already liked this product."})
            
            elif DisLike.objects.filter(user=request.user, product=product).exists():
                DisLike.objects.filter(user=request.user, product=product).delete()
            
            like, created = Like.objects.get_or_create(user=request.user, product=product)

            return Response({"message": "Product liked successfully."}, status=200)

        except Product.DoesNotExist:
            return Response({"message": "Product not found."}, status=500)
        

class ProductDislikeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            description= 'Product disliked ',
            responses= {
                200: OpenApiResponse(description="Product disliked successfully."),
                500: OpenApiResponse(description="Product not found.")
            }
    )
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            if DisLike.objects.filter(user=request.user, product=product).exists():
                return Response({"message": "You have already disliked this product."})
            
            elif Like.objects.filter(user=request.user, product=product).exists():
                Like.objects.filter(user=request.user, product=product).delete()
            
            dislike = DisLike(user=request.user, product=product)
            dislike.save()

            return Response({"message": "Product disliked successfully."})

        except Product.DoesNotExist:
            return Response({"message": "Product not found."})


class LikeCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            description= 'Comment liked ',
            responses= {
                200: OpenApiResponse(description="Comment liked successfully."),
                201: OpenApiResponse(description="You have already liked this comment."),
                500: OpenApiResponse(description="Comment not found.")
            }
    )
    def post(self, request, product_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found."}, status=500)
        
        if CommentLike.objects.filter(user=request.user, comment=comment).exists():  
            return Response({"message": "You have already liked this comment."}, status=201)
        
        elif CommentDislike.objects.filter(user=request.user, comment=comment).exists():
            CommentDislike.objects.filter(user=request.user, comment=comment).delete()

        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)  

        return Response({"message": "Comment liked successfully."}, status=200)



class DislikeCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            description= 'Comment disliked ',
            responses= {
                200: OpenApiResponse(description="Comment disliked successfully."),
                201: OpenApiResponse(description="You have already disliked this comment."),
                500: OpenApiResponse(description="Comment not found.")
            }
    )
    def post(self, request, product_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)

            if CommentDislike.objects.filter(user=request.user, comment=comment).exists():
                return Response({"message": "You have already disliked this comment."}, status=201)
            
            elif CommentLike.objects.filter(user=request.user, comment=comment).exists():
                CommentLike.objects.filter(user=request.user, comment=comment).delete()
            
            dislike = CommentDislike(user=request.user, comment=comment)
            dislike.save()

            return Response({"message": "Comment disliked successfully."}, status=200)

        except Comment.DoesNotExist:
            return Response({"message": "Comment not found."}, status=500)



