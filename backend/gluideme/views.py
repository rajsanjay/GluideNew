"""
Views for GluideMe app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Counselor, CounselorStudentAssignment, GuidanceSession, Recommendation
from .serializers import (
    CounselorSerializer, CounselorStudentAssignmentSerializer,
    GuidanceSessionSerializer, RecommendationSerializer
)


class CounselorViewSet(viewsets.ModelViewSet):
    """ViewSet for Counselor model."""
    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students assigned to this counselor."""
        counselor = self.get_object()
        assignments = CounselorStudentAssignment.objects.filter(
            counselor=counselor, is_active=True
        )
        serializer = CounselorStudentAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)


class CounselorStudentAssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for CounselorStudentAssignment model."""
    queryset = CounselorStudentAssignment.objects.all()
    serializer_class = CounselorStudentAssignmentSerializer


class GuidanceSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for GuidanceSession model."""
    queryset = GuidanceSession.objects.all()
    serializer_class = GuidanceSessionSerializer


class RecommendationViewSet(viewsets.ModelViewSet):
    """ViewSet for Recommendation model."""
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update recommendation status."""
        recommendation = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['pending', 'accepted', 'declined', 'completed']:
            recommendation.status = new_status
            recommendation.save()
            return Response({'status': 'updated'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
