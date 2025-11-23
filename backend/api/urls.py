from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SessionViewSet, MessageViewSet,
    StudentCourseViewSet, StudentTargetCollegeViewSet,
    StudentCommunityCollegeViewSet,
    UserProfileView, UserAttributeView,
    SchoolSearchView, CourseSearchView, MajorSearchView,
    AcademicYearListView, AcademicSemesterListView,
    SchoolListView,
    ConnectionRequestViewSet,
    RoomViewSet,
    FileViewSet,
    MeetingScheduleViewSet,
    CounselorAssignedCollegeView,
    SchoolCounselorView,
    LoginWithOTPView,
    ValidateOTPView
)

# Router for ViewSets
router = DefaultRouter()
router.register(r'session', SessionViewSet, basename='session')
router.register(r'message', MessageViewSet, basename='message')
router.register(r'student-courses', StudentCourseViewSet, basename='student-courses')
router.register(r'student-target-collage', StudentTargetCollegeViewSet, basename='student-target-collage')
router.register(r'student-community-collage', StudentCommunityCollegeViewSet, basename='student-community-collage')
router.register(r'connection-requests', ConnectionRequestViewSet, basename='connection-requests')
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'files', FileViewSet, basename='files')
router.register(r'meeting-schedules', MeetingScheduleViewSet, basename='meeting-schedules')

app_name = 'api'

urlpatterns = [
    # ViewSet routes
    path('', include(router.urls)),
    
    # User management
    path('user/', UserProfileView.as_view(), name='user-profile'),
    path('user-info/', UserAttributeView.as_view(), name='user-info'),
    
    # Academic data search
    path('collage/', SchoolSearchView.as_view(), name='school-search'),
    path('course/', CourseSearchView.as_view(), name='course-search'),
    path('major/', MajorSearchView.as_view(), name='major-search'),
    path('academic-years/', AcademicYearListView.as_view(), name='academic-years'),
    path('academic-semesters/', AcademicSemesterListView.as_view(), name='academic-semesters'),
    path('schools/', SchoolListView.as_view(), name='schools'),

    # Counselor management
    path('counselor-assigned-college/', CounselorAssignedCollegeView.as_view(), name='counselor-assigned-college'),
    path('school-counselor/<int:school_id>/', SchoolCounselorView.as_view(), name='school-counselor'),

    # OTP Authentication
    path('login-with-otp/', LoginWithOTPView.as_view(), name='login-with-otp'),
    path('validate-otp/', ValidateOTPView.as_view(), name='validate-otp'),
]
