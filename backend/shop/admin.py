from django.contrib import admin

from .models import Order, OrderItem, ShippingAddres


class ShippingAddresAdmin(admin.ModelAdmin):
    list_display = ['customer', 'city', 'stat', 'zipcode']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','date_order', 'calculate_total_price','complete']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'date_added', 'order']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddres, ShippingAddresAdmin)
