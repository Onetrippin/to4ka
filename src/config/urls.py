from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.internal.api import ninja_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', ninja_api.urls),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
