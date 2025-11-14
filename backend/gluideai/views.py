"""
Views for GluideAI app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ParsedTranscriptData, ParsedCourse, AIProcessingLog
from .serializers import ParsedTranscriptDataSerializer, ParsedCourseSerializer, AIProcessingLogSerializer
from .tasks import process_transcript_task


class ParsedTranscriptDataViewSet(viewsets.ModelViewSet):
    """ViewSet for ParsedTranscriptData model."""
    queryset = ParsedTranscriptData.objects.all()
    serializer_class = ParsedTranscriptDataSerializer


class ParsedCourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ParsedCourse model (read-only)."""
    queryset = ParsedCourse.objects.all()
    serializer_class = ParsedCourseSerializer


class AIProcessingLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AIProcessingLog model (read-only)."""
    queryset = AIProcessingLog.objects.all()
    serializer_class = AIProcessingLogSerializer

    @action(detail=False, methods=['post'])
    def trigger_processing(self, request):
        """Trigger AI processing for a transcript."""
        transcript_id = request.data.get('transcript_id')
        if not transcript_id:
            return Response({'error': 'transcript_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Trigger async Celery task
        task = process_transcript_task.delay(transcript_id)

        return Response({
            'status': 'processing started',
            'task_id': task.id,
            'transcript_id': transcript_id
        })
