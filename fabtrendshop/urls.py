from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets


urlpatterns = [
                path('admin/', admin.site.urls),
                path('', include('fabtrendapp.urls')),
                path('cart/', include('cart.urls')),
                path('orders/', include('orders.urls')),
                path('paytm/', include(('paytm.urls','paytm'),namespace='paytm')),
                path('coupons/', include(('coupons.urls','coupons'),namespace='coupons')),
                path('wishlists/', include(('wishlists.urls','wishlists'),namespace='wishlists')),
        ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)