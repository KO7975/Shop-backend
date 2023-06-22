from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OrderItem, Order, ShippingAddres
from .serializers import OrderItemSerializer, OrderShippingSerializer



class OrderItemDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get(self, request):
        try:
            order = Order.objects.get(customer_id=request.user.id, complete=False )
            order_item = OrderItem.objects.filter(order=order).values()

            return Response({'data':list(order_item)})
        except:
            return Response({'message':'This order DoesNotExist'})


    def delete(self, request):
        try:
            items = OrderItem.objects.filter(
                order__customer=request.user,
                order__complete=False
                ) 
            for i in items:
                i.delete()

            order = Order.objects.get(customer=request.user, complete=False)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
        
        except:
            return Response({'message':'This order DoesNotExist'})

    

class OrderTotalPriceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(customer=request.user, complete=False )
        total_price = order.calculate_total_price()

        response_data = {
            'total_price': total_price
        }
        return Response(response_data)
    


class OrderItemDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            item = OrderItem.objects.filter(
                order__customer=request.user,
                order__complete=False,
                product_id=pk
                ) 
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
        
        except:
            return Response({'message':'This order DoesNotExist'})
        


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