from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('content/', include('aiart_content.urls')),
    path('auth/', include('aiart_auth.urls')),
    path('', include('aiart_main.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
