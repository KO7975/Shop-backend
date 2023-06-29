from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import datetime

from .serializer import CommentSerializer, ProductSerializer, CategorySerializer

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



def get_top_10_products():
    top_products = Product.objects.annotate(like_count=Count('like')).order_by('-like_count')[:10]
    return top_products


def get_new_added():
    today = datetime.datetime.now().date()
    start_date = today - datetime.timedelta(days=30)
    new_10 = Product.objects.all().order_by('-updated')[:10]
    days_30 = Product.objects.filter(updated__gte= start_date, updated__lte=today)
    if days_30.count() > new_10.count():
        return days_30
    else:
        return new_10


class ProductsView(APIView):
    permission_classes = (AllowAny,)

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

    def get(self, request, product_id):
        try:
            product = Product.objects.filter(id=product_id)
            serializer = ProductSerializer(product, many=True)

            return Response({'product': serializer.data,})
        
        except Product.DoesNotExist:
            return Response({'message': 'product not found'})

        

class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

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

    def get(self, request, category_id):
        category_products = Product.objects.filter(categoty_id_id=category_id).values()
        category = Category.objects.filter(perent_id=category_id)  
        
        all_categories = [i.id for i in category ]
        all_categories.append(category_id)

        all_products = []
        for id in all_categories:
            for i in Product.objects.filter(categoty_id_id=id).values():
                if i not in all_products:
                    all_products.append(i)

        children_category = {i.name:i.id for i in category if i.id != category_id}
        sub_products = {name:Product.objects.filter(categoty_id_id=id).values() for name,id in children_category.items()}
        
        if category_products or children_category:
            return Response({
                'all_products': all_products,
                'parent': list(category_products),
                'sub_categories': children_category,
                'sub_products': sub_products
                })
        else:
            return Response({'message': 'This category DoesNotExist'})
        


class StockView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        stock = Stock.objects.filter(id=pk).values().first()
        product = Product.objects.get(stock=pk).name

        if len(stock) != 0 :
            return Response({f'{product}': stock})
        else:
            return Response({'message': 'stock not found'})



class ProductLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            if Like.objects.filter(user=request.user, product=product).exists():
                return Response({"message": "You have already liked this product."})
            
            elif DisLike.objects.filter(user=request.user, product=product).exists():
                DisLike.objects.filter(user=request.user, product=product).delete()
            
            like, created = Like.objects.get_or_create(user=request.user, product=product)

            return Response({"message": "Product liked successfully."})

        except Product.DoesNotExist:
            return Response({"message": "Product not found."})
        


class ProductDislikeView(APIView):
    permission_classes = [IsAuthenticated]

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

        return Response({"message": "Comment liked successfully."})





class DislikeCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)

            if CommentDislike.objects.filter(user=request.user, comment=comment).exists():
                return Response({"message": "You have already disliked this comment."})
            
            elif CommentLike.objects.filter(user=request.user, comment=comment).exists():
                CommentLike.objects.filter(user=request.user, comment=comment).delete()
            
            dislike = CommentDislike(user=request.user, comment=comment)
            dislike.save()

            return Response({"message": "Comment disliked successfully."})

        except Comment.DoesNotExist:
            return Response({"message": "Comment not found."})



