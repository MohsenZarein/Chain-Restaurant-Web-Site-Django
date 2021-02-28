from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('branch/', include('branches.urls')),
    path('customer/', include('customer.urls')),
    path('order/', include('order.urls')),
    path('perssonel/', include('perssonel.urls')),
    path('reservation/', include('reservation.urls')),
] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
