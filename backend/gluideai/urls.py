"""
URL configuration for GluideAI app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParsedTranscriptDataViewSet, ParsedCourseViewSet, AIProcessingLogViewSet

router = DefaultRouter()
router.register(r'parsed-transcripts', ParsedTranscriptDataViewSet, basename='parsed-transcript')
router.register(r'parsed-courses', ParsedCourseViewSet, basename='parsed-course')
router.register(r'processing-logs', AIProcessingLogViewSet, basename='processing-log')

urlpatterns = [
    path('', include(router.urls)),
]
