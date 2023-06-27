from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import OrderItem, Order, ShippingAddres
from .serializers import OrderItemSerializer, OrderShippingSerializer
from product.models import Product
from authentication.models import User
from django.conf import settings
from .cart import Cart



class AddToOrderView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)

        product_id = request.data['product_id']
        quantity = request.data['quantity']

        if request.user.is_authenticated:
            order, create = Order.objects.get_or_create(
                customer_id=request.user.id,
                complete=False
                )
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                quantity=quantity,
                )
            order_item.save()
 
            return Response({'message':'Product added to cart'},status=200)
        
        else:
            email = request.data.get('email')
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity')

            product = get_object_or_404(Product, id=product_id)
            cart = Cart(request)
            cart.add(product=product, quantity=quantity)

            return Response({'message': f'Product added to cart successfully.'})
        


class OrderItemDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get(self, request):
        try:
            if request.user.is_authenticated:
                order = Order.objects.get(customer_id=request.user.id, complete=False )
                order_item = OrderItem.objects.filter(order=order)
                serializer =self.serializer_class(order_item, many=True)

                return Response({'data':serializer.data})
            else:
                order = Cart(request)
                order.__iter__()
                return Response(self.serializer_class(order, many=True).data)
        
        
        except Order.DoesNotExist:
            return Response({'message':'This order DoesNotExist'},status=status.HTTP_404_NOT_FOUND)


    def delete(self, request):
        try:
            if request.user.is_authenticated:
                order = Order.objects.get(customer=request.user, complete=False)
                order_items = OrderItem.objects.filter(order=order)
                order_items.delete()
                order.delete()

                return Response(status=status.HTTP_204_NO_CONTENT) 
            
            else:
                order = Cart(request)
                order.clear()
                return Response(status=status.HTTP_204_NO_CONTENT) 
                    
        except Order.DoesNotExist:
            return Response({'message':'This order DoesNotExist'},status=status.HTTP_404_NOT_FOUND)
        


class OrderItemQuantityChangeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, product_id):

        quantity = request.data['quantity'] 

        if request.user.is_authenticated:
            order = Order.objects.get(customer_id=request.user.id, complete=False )
            item = OrderItem.objects.filter(order=order, product_id=product_id).values()

            item.update(quantity=quantity)

            return Response({'item_quantity': item.values().first()['quantity']}, status=200)
        else:
            cart = Cart(request)
            product = Product.objects.get(id=product_id)
            cart.add(product=product,quantity=int(quantity), update_quantity=True)
            cart.save()

            return Response({'new_price': cart.get_total_price()}, status=200)

    

class OrderTotalPriceView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = Order.objects.get(customer=request.user, complete=False )
            total_price = order.calculate_total_price()

            response_data = {
                'total_price': total_price
            }
            return Response(response_data)
        
        else:
            cart = Cart(request) 
            return Response({'total_price': cart.get_total_price()})

    


class OrderItemDeleteView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderItemSerializer
        
    def delete(self, request, pk):
        try:
            if request.user.is_authenticated:
                item = OrderItem.objects.filter(
                    order__customer=request.user,
                    order__complete=False,
                    product_id=pk
                    ) 
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT) 
            
            else:
                cart = Cart(request)
                product = Product.objects.get(id=pk)
                cart.remove(product=product)
                
                return Response(status=status.HTTP_204_NO_CONTENT) 

        except OrderItem.DoesNotExist as e:
            return Response({'exception':e}, status=500)
        

        


class OrderShippingAdressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data=request.data
        data['customer'] = request.user.pk
        data['order'] = Order.objects.get(customer=request.user, complete=False).pk
        serializer = OrderShippingSerializer(data=data)

        adress = ShippingAddres.objects.filter(
            order=data['order'],
            adress=data['adress'],
            city=data['city'] 
            )
        if serializer.is_valid() and not adress.exists():

            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        
        elif serializer.is_valid() and adress.exists():
            return Response({'message': 'Adress already exists in db'})
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

