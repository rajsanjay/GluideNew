"""
Views for GluideAI app.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import TranscriptParseSerializer
from .tasks import parse_transcript_task
from .authentication import StaticTokenAuthentication
import time
from datetime import datetime


class HealthCheck(APIView):
    """
    Health check endpoint.
    GET /api/health
    Reference: REWRITE_SPECIFICATION.md lines 54-75
    """
    authentication_classes = []  # Public endpoint
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "status": "ok",
            "message": "Application is healthy."
        }, status=status.HTTP_200_OK)


class TranscriptParseViewSet(viewsets.ViewSet):
    """
    Transcript parsing endpoint.
    POST /api/v1/gluideai/parse-transcript/
    Reference: REWRITE_SPECIFICATION.md lines 79-217
    """
    authentication_classes = [StaticTokenAuthentication]

    def create(self, request):
        """
        Queue a transcript parsing task.

        Request body:
        {
            "file_path": "documents/transcript.pdf",
            "webhook_url": "https://api.example.com/webhook"
        }
        """
        start_time = time.time()

        # Validate input
        serializer = TranscriptParseSerializer(data=request.data)
        if not serializer.is_valid():
            execution_time = time.time() - start_time
            return Response({
                "location": request.path,
                "body": {
                    "error": serializer.errors,
                    "message": "Invalid query",
                    "status": "error"
                },
                "metadata": {
                    "execution_time": f"{execution_time:.3f}s",
                    "timestamp": datetime.utcnow().isoformat() + '+00:00',
                    "status_code": 400
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Queue task
        file_path = serializer.validated_data['file_path']
        webhook_url = serializer.validated_data['webhook_url']

        task = parse_transcript_task.delay(file_path, webhook_url)

        execution_time = time.time() - start_time

        # Return success response
        return Response({
            "location": request.path,
            "body": {
                "message": "Transcript parsing task has been queued successfully",
                "task_id": str(task.id),
                "file_path": file_path,
                "webhook_url": webhook_url,
                "status": "queued"
            },
            "metadata": {
                "execution_time": f"{execution_time:.3f}s",
                "timestamp": datetime.utcnow().isoformat() + '+00:00',
                "status_code": 202
            }
        }, status=status.HTTP_202_ACCEPTED)
