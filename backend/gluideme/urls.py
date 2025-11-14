"""
URL configuration for GluideMe app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CounselorViewSet, CounselorStudentAssignmentViewSet,
    GuidanceSessionViewSet, RecommendationViewSet
)

router = DefaultRouter()
router.register(r'counselors', CounselorViewSet, basename='counselor')
router.register(r'assignments', CounselorStudentAssignmentViewSet, basename='assignment')
router.register(r'sessions', GuidanceSessionViewSet, basename='session')
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),
]
