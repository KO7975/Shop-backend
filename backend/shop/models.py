from django.db import models
from django.conf import settings
from authentication.models import User
from product.models import Product


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    STATUS = [
        ('WC', 'Waiting Confirmation'),
        ('F', 'Formed'),
        ('IW', 'In Way'),
        ('FD', 'Final Destination')
    ]
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True )
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default=None, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.customer.email)

    def calculate_total_price(self):
        total_price = OrderItem.objects.filter(order=self).values()
             
        total_price =sum([Product.objects.get(id=i['product_id']).price * i['quantity'] for i in total_price])
       
        return total_price or 0
    

class ShippingAddres(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    adress = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    stat = models.CharField(max_length=200, null=False)   
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adress




