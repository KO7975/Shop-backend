from django.urls import path

from .views import (
    ProductView,
    ProductsView,
    CategoryView,
    StockView,
    ProductCategoryView,
)


urlpatterns = [
    path('from_category/<int:category_id>', ProductCategoryView.as_view(), name='from_category'),
    path('', ProductsView.as_view(), name='products'),
    path('item/<int:pk>', ProductView.as_view(), name='product'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('stock/<int:pk>', StockView.as_view(), name='stock'),
]