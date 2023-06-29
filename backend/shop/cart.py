from decimal import Decimal
from django.conf import settings
from shop.models import Product
import os
import base64


class Cart(object):

    def __init__(self, request):

        self.session = request.session
        order = self.session.get(settings.SHOP_SESSION_ID)

        if not order:
            order = self.session[settings.SHOP_SESSION_ID] = {}

        self.order = order


    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.order:
            self.order[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        if update_quantity:
            self.order[product_id]['quantity'] = quantity
        else:
            self.order[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.SHOP_SESSION_ID] = self.order
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.order:
            del self.order[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.order.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.order[str(product.id)]['product'] = product

        for item in self.order.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.order.values())
    

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                self.order.values())
    

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.SHOP_SESSION_ID]
        self.session.modified = True


    def secret(self):
        key = os.urandom(32)
        secret_key = base64.b32encode(key).decode('utf-8')
        return secret_key