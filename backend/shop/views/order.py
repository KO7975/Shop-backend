from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from shop.models import OrderItem, Order, ShippingAddres
from shop.serializers import OrderItemSerializer, OrderShippingSerializer
from product.models import Product, Stock
from shop.cart import Cart
from drf_spectacular.utils import (
    inline_serializer,
    extend_schema,
    OpenApiResponse,
)
from shop.schema import *


class AddToOrderView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    @extend_schema(
        description='Add product to cart',
        parameters=[QUANTITY_PARAMETER]
    )
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)

        quantity = request.data['quantity']
        stoke = Stock.objects.get(ptoduct_id=product)

        if not stoke.quantity >= int(quantity):
            return Response(
                {'message': f'Stock quantyti = {stoke.quantity} lover than order quantity = {quantity}'},
                status.HTTP_400_BAD_REQUEST
            )  
        
        if request.user.is_authenticated:
            order, create = Order.objects.get_or_create(
                customer_id=request.user.id,
                complete=False
                )

            if not OrderItem.objects.filter(order=order).exists():
                order_item,  _ = OrderItem.objects.get_or_create(order=order, product=product, quantity=quantity)

            else:
                order_item = OrderItem.objects.filter(order=order, product=product).values()
                quantit = int(order_item[0]['quantity']) + int(quantity)
                order_item.update(quantity=quantit) 

            return Response(
                {'message':'Product added to cart'},
                status.HTTP_200_OK
            )
        
        else:
            product = get_object_or_404(Product, id=product_id)
            cart = Cart(request)
            cart.add(product=product, quantity=int(quantity))

            return Response(
                {'message': f'Product added to cart.'},
                status.HTTP_200_OK
            )
        

class OrderItemDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    ser = inline_serializer(
        name='Cart', 
        fields={'price':'product price', 'total_price': 'total cart price'}
    )

    @extend_schema(
            description=' Show products in users cart',
            responses={
                200: OpenApiResponse(description='Return cart data for authenticated user', response=serializer_class),
                201: OpenApiResponse(description='Return cart data for non authenticated user', response=ser ),
                400: OpenApiResponse(description='This order DoesNotExist')
            }
    )
    def get(self, request):
        try:
            if request.user.is_authenticated:
                order = Order.objects.filter(customer_id=request.user.id, complete=False )
                order_item = OrderItem.objects.filter(order=order.first()).values()
                product = Product.objects.filter(id__in=order_item.values_list('product_id')).values()
                data = order_item.first()

                data['order_id'] = list(order.values())
                data['product_id'] = list(product)

                serializer = OrderItemSerializer(data)
                return Response(serializer.data, status=200)
            
            else:
                order = Cart(request)
                order1 = order.__iter__()
                return Response({'data': order.order}, status=201)
              
        except Order.DoesNotExist:
            return Response(
                {'message':'This order DoesNotExist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        

    @extend_schema(
            description='Delete Cart'
    )
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
            return Response(
                {'message':'This order DoesNotExist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        

class OrderItemQuantityChangeView(APIView):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
            description='Change quantity of product by product_id and new quantity',
            methods=['POST'],
            parameters=[QUANTITY_PARAMETER],
            responses={
                200: OpenApiResponse(
                    response=OrderItemSerializer,
                    description='Return item with apdated quantity for auth user '),
                201: OpenApiResponse(
                    description='Return new price for non auth user "new_price":"int"'),
            }
    )
    def post(self, request, product_id):

        quantity = request.data['quantity'] 

        if request.user.is_authenticated:
            product = Product.objects.filter(id=product_id).values().first()
            order = Order.objects.filter(customer_id=request.user.id, complete=False ).first()
            item = OrderItem.objects.filter(order=order, product=product_id).values()

            item.update(quantity=quantity) 

            data=item.first()
            data['order_id'] = order
            data['product_id']= product
            serializer = OrderItemSerializer(data)
            # serializer.is_valid(raise_exception=True)
            return Response(
                serializer.data, 
                status.HTTP_200_OK
            )
        
        else:
            cart = Cart(request)
            product = Product.objects.get(id=product_id)
            cart.add(product=product, quantity=int(quantity), update_quantity=True)
            cart.save()

            return Response(
                {'new_price': cart.get_total_price()},
                status.HTTP_201_CREATED)

    
class OrderTotalPriceView(APIView):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
            description='Get order total price',
            responses={
                200: OpenApiResponse(description="total_price")
            }
    )
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = Order.objects.get(customer=request.user, complete=False )
            total_price = order.calculate_total_price()

            return Response({'total_price': total_price})
        
        else:
            cart = Cart(request) 
            return Response({'total_price': cart.get_total_price()})

    
class OrderItemDeleteView(APIView):
    permission_classes = [permissions.AllowAny]
        
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
            return Response(
                {'message':e},
                status.HTTP_400_BAD_REQUEST
            )
                

class OrderShippingAdressView(APIView):
    serializer_class = OrderShippingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description='Order adress information save from form',
        request=OrderShippingSerializer,
        responses={
            201: OpenApiResponse(description='Created'),
            400: OpenApiResponse(description='HTTP_400_BAD_REQUEST'),
            400: OpenApiResponse(description='Adress already exists in db'),            
        }
    )
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
            return Response(
                {'message': 'Adress already exists in db'},
                status.HTTP_400_BAD_REQUEST
            )
        
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
            description='Confirm order',
            methods=['PUT']
    )
    def put(self, request):
        if request.user.is_authenticated:
            order = Order.objects.get(customer=request.user, complete=False)
            order_items = OrderItem.objects.filter(order=order).values()

            if order.status is not None:
                return Response(
                    {'message': 'Order already confirmed'},
                    status.HTTP_400_BAD_REQUEST
                )

            if len(order_items)> 0:

                for i in order_items:
                    id = i['product_id']
                    iquantity = i['quantity']
                    stoke = Stock.objects.filter(ptoduct_id_id=id).first()

                    if stoke.quantity < iquantity :
                        return Response(
                            {'message': f'Stock quantyti = {stoke.quantity} lover than order quantity = {iquantity}'}, 
                            status.HTTP_400_BAD_REQUEST
                        )                  
                    quantity = stoke.quantity - iquantity
                    res_quantity = stoke.reserved_quantity + iquantity
                    cart = Cart(request)

                    stoke.__setattr__('quantity', quantity)
                    stoke.__setattr__('reserved_quantity', res_quantity)
                    stoke.save()

                    order.__setattr__('status', 'VC')
                    order.__setattr__('transaction_id', cart.secret())
                    order.save()

                return Response(
                    {'message': f'Order status changed on {order.status}','order_key':order.transaction_id},
                    status.HTTP_200_OK)   
                          
            else:
                return Response(
                    {'message':'No products chosen'},
                    status.HTTP_400_BAD_REQUEST
                )                
        else:
            cart = Cart(request)
            ids = cart.order.keys()
            if len(ids)>0:
                for i in list(ids):
                    stoke = Stock.objects.filter(ptoduct_id_id=i).first()
                    stock_q = stoke.quantity
                    quantity1 = cart.order[i]['quantity']

                    if not stock_q >= quantity1 :
                        return Response(
                            {'message': f'Stock quantyti = {stock_q} lover than order quantity {quantity1}'},
                            status.HTTP_400_BAD_REQUEST
                        )  
                    
                    quantity = stock_q - quantity1
                    res_quantity = stock_q + quantity1

                    stoke.__setattr__('quantity', quantity)
                    stoke.__setattr__('reserved_quantity', res_quantity)
                    stoke.save()
                    cart.remove(Product.objects.get(id=i))

                order_id = cart.secret()
                return Response(
                    {'message': 'Product reserved .', 'order_key': order_id},
                    status.HTTP_200_OK
                    )    
            else:
                return Response(
                    {'message':'No products chosen'},
                    status.HTTP_400_BAD_REQUEST
                )


class OrderStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description='order status',
        methods=['POST'],
        parameters=[ORDER_STATUS_POST_PARAM]
    )
    def post(self,request):
        order_id = request.data['order_key']
        order = Order.objects.get(transaction_id=order_id)

        return Response({
            'order_status':order.status,
            'completed': order.complete
            })
    
    @extend_schema(
        description='Change order status',
        methods=['PUT'],
        parameters=[ORDER_STATUS_PUT_PARAM],
        responses={
            200: OpenApiResponse(description="Order status WC changed on F")
        }
    )
    def put(self, request):
        order_id = request.data.get('order_key')
        order_status = request.data.get('status')

        order = Order.objects.get(transaction_id=order_id)
        order_status = order.status
        order.__setattr__('status', order_status)
        order.save()
        return Response(
            {'message': f'Order status {order_status} changed on {order.status}'},
            status.HTTP_200_OK
        )
