"""
URL configuration for the API app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet, TranscriptViewSet, SavedCourseViewSet,
    CourseViewSet, CourseOfferingViewSet
)

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'transcripts', TranscriptViewSet, basename='transcript')
router.register(r'saved-courses', SavedCourseViewSet, basename='saved-course')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'course-offerings', CourseOfferingViewSet, basename='course-offering')

urlpatterns = [
    path('', include(router.urls)),
]
