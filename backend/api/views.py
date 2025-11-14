"""
API views for the main application.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Transcript, SavedCourse
from .models_course_db import Course, CourseOffering
from .serializers import (
    StudentSerializer, TranscriptSerializer, SavedCourseSerializer,
    CourseSerializer, CourseOfferingSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for Student model."""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TranscriptViewSet(viewsets.ModelViewSet):
    """ViewSet for Transcript model."""
    queryset = Transcript.objects.all()
    serializer_class = TranscriptSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Trigger transcript processing."""
        transcript = self.get_object()
        # This will be implemented with Celery task
        transcript.processing_status = 'processing'
        transcript.save()
        return Response({'status': 'processing started'})


class SavedCourseViewSet(viewsets.ModelViewSet):
    """ViewSet for SavedCourse model."""
    queryset = SavedCourse.objects.all()
    serializer_class = SavedCourseSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Course model (read-only from course_db)."""
    queryset = Course.objects.using('course_db').all()
    serializer_class = CourseSerializer
    lookup_field = 'course_code'


class CourseOfferingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for CourseOffering model (read-only from course_db)."""
    queryset = CourseOffering.objects.using('course_db').all()
    serializer_class = CourseOfferingSerializer
