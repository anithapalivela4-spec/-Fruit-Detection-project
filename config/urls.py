from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from detection.views import HomeView, AboutView, ContactView, GalleryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('accounts/', include('accounts.urls')),
    path('fruits/', include('fruits.urls')),
    path('diseases/', include('diseases.urls')),
    path('detection/', include('detection.urls')),
    # Direct short routes for intuitive viva navigation
    path('dashboard/', include('detection.urls_dashboard')),
    path('api/', include('detection.urls_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
