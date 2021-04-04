from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('product.urls')),
    path('', include('order_management.urls')),

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
