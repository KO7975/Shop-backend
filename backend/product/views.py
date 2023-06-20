from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import (
    Product,
    Stock, 
    Category
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

    def get(self, request, category_pk):
        category_products = Product.objects.filter(categoty_id_id=category_pk).values()

        if category_products:
            return Response({'products': list(category_products)})
        else:
            return Response({'message': 'no selected intems in this category'})
        

class StockView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        stock = Stock.objects.filter(id=pk).values()

        if len(stock) != 0 :
            return Response({'stock': stock[0]})
        else:
            return Response({'message': 'stock not found'})

