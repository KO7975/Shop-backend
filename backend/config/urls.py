from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path("", include("main.urls")),

    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('product/', include('product.urls')),

    path('auth/', include('djoser.urls.jwt')),
    path('account/', include('djoser.urls')),
    # path('account/', include('djoser.social.urls')),

    path('cart/', include('shop.urls')),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view( url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
