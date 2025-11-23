from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentsViewSet, StudentDemographicsViewSet,
    StudentGoalViewSet, StudentPathwaysViewSet,
    CollegeViewSet, CourseViewSet, ProgramViewSet,
    EducationPlanViewSet, CounselorProfileViewSet,
    AIRecommendationViewSet, DocumentViewSet,
    TranscriptUploadView, TranscriptWebhookView, TranscriptListView
)

router = DefaultRouter()
router.register(r'student_info', StudentsViewSet, basename='student-info')
router.register(r'student-demographics', StudentDemographicsViewSet, basename='student-demographics')
router.register(r'student-goal', StudentGoalViewSet, basename='student-goal')
router.register(r'student-pathways', StudentPathwaysViewSet, basename='student-pathways')
router.register(r'colleges', CollegeViewSet, basename='colleges')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'programs', ProgramViewSet, basename='programs')
router.register(r'education-plan', EducationPlanViewSet, basename='education-plan')
router.register(r'counselor-profile', CounselorProfileViewSet, basename='counselor-profile')
router.register(r'ai-recommendations', AIRecommendationViewSet, basename='ai-recommendations')
router.register(r'documents', DocumentViewSet, basename='documents')

app_name = 'gluideme'

urlpatterns = [
    path('', include(router.urls)),

    # Transcript endpoints
    path('transcripts/list/', TranscriptListView.as_view(), name='transcript-list'),
    path('transcripts/upload/', TranscriptUploadView.as_view(), name='transcript-upload'),
    path('transcript-webhooks/', TranscriptWebhookView.as_view(), name='transcript-webhook'),
]
