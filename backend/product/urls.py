from django.urls import path
from .views import (
    ProductView,
    ProductsView,
    TopNew10ProdactsView,
    ProductLikeView,
    ProductDislikeView,
    CategoryView,
    StockView,
    ProductCategoryView,
    CommentAPIView,
    LikeCommentAPIView,
    DislikeCommentAPIView,
)


urlpatterns = [
    path('from_category', ProductCategoryView.as_view(), name='from_category'),
    path('', ProductsView.as_view(), name='products'),
    path('top_new_10', TopNew10ProdactsView.as_view(), name='top_new_10'),

    path('categories', CategoryView.as_view(), name='categories'),
    path('stock/', StockView.as_view(), name='stock'),

    path('item/', ProductView.as_view(), name='product'),
    path('item/like', ProductLikeView.as_view(), name='like'),
    path('item/dislike', ProductDislikeView.as_view(), name='dislike'),

    path('item/comments', CommentAPIView.as_view(), name='comment'),
    path('item/comments/like', LikeCommentAPIView.as_view(), name='like-comment'),
    path('item/comments/dislike', DislikeCommentAPIView.as_view(), name='dislike-comment'),
]