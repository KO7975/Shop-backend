from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    )
from product.serializer import (
    ProductSerializer,
    StockSerializer,
    CategorySerializer,
    CommentSerializer,
    TopNew10ProdactsResponseSerializer,
)


PRODUCT_ID_PARAMETER = OpenApiParameter(
    name='product_id',
    required=True,
    description='Product ID',
    type=int,
)

COMMENT_ID_PARAMETER = OpenApiParameter(
    name='comment_id',
    required=True,
    description='Comment ID',
    type=int,
)

CATEGORY_200_RESPONSE = OpenApiResponse(
    response=CategorySerializer(many=True),
    description='All categories'
)

PRODUCT_CATEGORY_200_RESPONSE = OpenApiResponse(
    description='Products from category',
    response=ProductSerializer
)

TOP_NEW_10_PRODUCTS_200_RESPONSE = OpenApiResponse(
    description='Details',
    response=TopNew10ProdactsResponseSerializer
)

PRODUCT_CATEGORY_PARAMS = [
    OpenApiParameter(name='category_id', required=True, description='Category ID', type=int),
    OpenApiParameter('sub_categories', ProductSerializer, response=True),
    OpenApiParameter('category_products', ProductSerializer, response=True),
    OpenApiParameter('sub_category_products',  ProductSerializer, response=True)
]

DISLIKE_COMMENT_RESPONSES = {
    201: OpenApiResponse(description="Comment disliked successfully."),
    200: OpenApiResponse(description="You have already disliked this comment."),
    400: OpenApiResponse(description="Comment not found.")
}

LIKE_COMMENT_RESPONSES = {
    201: OpenApiResponse(description="Comment liked successfully."),
    200: OpenApiResponse(description="You have already liked this comment."),
    400: OpenApiResponse(description="Comment not found.")
}

PRODUCT_DISLIKE_RESPONSES = {
    200: OpenApiResponse(description="Product disliked successfully."),
    400: OpenApiResponse(description="Product not found.")
}

PRODUCT_LIKE_RESPONSES = {
    200: OpenApiResponse(description="Product liked successfully."),
    400: OpenApiResponse(description="Product not found.")
}

STOCK_RESPONSES = {
    200: StockSerializer,
    400: OpenApiResponse(description='Product not exists')
}

COMMENT_GET_RESPONSES = {
    200:OpenApiResponse(response=CommentSerializer(many=True), description= 'Comment from product_id'),
    400:OpenApiResponse(description="Product not found."),
}

COMMENT_POST_RESPONSES = {
    201: OpenApiResponse(description='Comment created'),
    400:OpenApiResponse(description='Product not found'),
}

PRODUCT_GET_RESPONSES = {
    200:OpenApiResponse(
        description='Product details',
        response=ProductSerializer
    ),
    400:OpenApiResponse(description='ProductDoesNotExist')
}