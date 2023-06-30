from django.urls import path

from .views import (
    ProductView,
    ProductsView,
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
    path('from_category/<int:category_id>', ProductCategoryView.as_view(), name='from_category'),
    path('', ProductsView.as_view(), name='products'),

    path('categories', CategoryView.as_view(), name='categories'),
    path('stock/<int:product_id>', StockView.as_view(), name='stock'),

    path('item/<int:product_id>/', ProductView.as_view(), name='product'),

    path('item/<int:product_id>/like', ProductLikeView.as_view(), name='like'),
    path('item/<int:product_id>/dislike', ProductDislikeView.as_view(), name='dislike'),

    path('item/<int:product_id>/comments/', CommentAPIView.as_view(), name='comment'),

    path('item/<int:product_id>/comments/<int:comment_id>/like/', LikeCommentAPIView.as_view(), name='like-comment'),
    path('item/<int:product_id>/comments/<int:comment_id>/dislike/', DislikeCommentAPIView.as_view(), name='dislike-comment'),
]