from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('content/', include('aiart_content.urls')),
    path('auth/', include('aiart_auth.urls')),
    path('', include('aiart_main.urls')),
    path('admin/', admin.site.urls),
]
