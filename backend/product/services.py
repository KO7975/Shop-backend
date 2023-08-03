import datetime
from django.db.models import Count
from product.models import Product


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
    
    
