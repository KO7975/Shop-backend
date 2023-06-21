from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import (
    Product,
    Stock, 
    Category,
    Attribute,
)


class ProductsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        products = Product.objects.all().values()

        return Response({'products': list(products)})
    

class ProductView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, pk):
        product = Product.objects.filter(id=pk).values()

        if len(product) != 0:
            return Response({'product':product[0]})
        else:
            return Response({'message': 'product not found'})
           

class CategoryView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        categories = Category.objects.all().values()

        return Response({'categories': list(categories)})


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
        stock = Stock.objects.filter(id=pk).values()
        product = Product.objects.get(stocke_id=pk).name

        if len(stock) != 0 :
            return Response({f'{product}': stock[0]})
        else:
            return Response({'message': 'stock not found'})
        


