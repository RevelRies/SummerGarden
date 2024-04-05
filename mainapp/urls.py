from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = ([
    path('summer_garden/admin/', admin.site.urls),
    path('summer_garden/', include('summer_garden.urls', namespace='summer_garden')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
