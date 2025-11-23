"""
URL configuration for Gluide consolidated application.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gluideai.views import HealthCheck
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health check (no auth required)
    path('api/health', HealthCheck.as_view(), name='health'),

    # Transcript parser API
    path('api/v1/', include('api.v1.urls')),

    # Main backend API
    path('backend/api/', include('api.urls')),

    # Gluideme app API
    path('backend/api/gluideme/', include('gluideme.urls')),

    # Django Allauth headless authentication
    path('_allauth/', include('allauth.headless.urls')),

    # JWT authentication
    path('backend/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('backend/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
