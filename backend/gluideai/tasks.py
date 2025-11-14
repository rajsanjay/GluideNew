"""
Celery tasks for GluideAI transcript processing.
"""

from celery import shared_task
from django.conf import settings
import time


@shared_task(bind=True, max_retries=3)
def process_transcript_task(self, transcript_id):
    """
    Process a transcript using AI to extract course and student data.

    Args:
        transcript_id: ID of the Transcript to process

    Returns:
        dict: Processing results
    """
    from api.models import Transcript
    from .models import AIProcessingLog, ParsedTranscriptData

    try:
        transcript = Transcript.objects.get(id=transcript_id)

        # Create processing log
        log = AIProcessingLog.objects.create(
            transcript=transcript,
            processing_type='extraction',
            status='started'
        )

        start_time = time.time()

        # Update transcript status
        transcript.processing_status = 'processing'
        transcript.save()

        # TODO: Implement actual AI processing logic
        # This is a placeholder for the AI integration
        # In production, this would call OpenAI API, parse results, etc.

        if settings.USE_TEST_MODE:
            # Test mode: create synthetic parsed data
            parsed_data, created = ParsedTranscriptData.objects.get_or_create(
                transcript=transcript,
                defaults={
                    'student_name': 'Test Student',
                    'student_id': 'TEST123',
                    'school_name': 'Test High School',
                    'gpa': 3.75,
                    'total_credits': 24.0,
                    'courses_data': []
                }
            )
        else:
            # Database mode: actual AI processing
            # This would integrate with OpenAI, extract data, etc.
            pass

        # Update processing time
        processing_time = time.time() - start_time
        log.processing_time_seconds = processing_time
        log.status = 'completed'
        log.save()

        # Update transcript status
        transcript.processing_status = 'completed'
        transcript.save()

        return {
            'status': 'success',
            'transcript_id': transcript_id,
            'processing_time': processing_time
        }

    except Transcript.DoesNotExist:
        return {'status': 'error', 'message': f'Transcript {transcript_id} not found'}

    except Exception as exc:
        # Log the error
        if 'log' in locals():
            log.status = 'failed'
            log.error_message = str(exc)
            log.save()

        # Update transcript status
        if 'transcript' in locals():
            transcript.processing_status = 'failed'
            transcript.save()

        # Retry the task
        raise self.retry(exc=exc, countdown=60)


@shared_task
def batch_process_transcripts(transcript_ids):
    """
    Process multiple transcripts in batch.

    Args:
        transcript_ids: List of Transcript IDs to process

    Returns:
        dict: Batch processing results
    """
    results = []
    for transcript_id in transcript_ids:
        result = process_transcript_task.delay(transcript_id)
        results.append({'transcript_id': transcript_id, 'task_id': result.id})

    return {'status': 'batch started', 'results': results}
