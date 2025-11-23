from celery import shared_task
import requests
import logging
from django.conf import settings
import json
import time

logger = logging.getLogger(__name__)


@shared_task(bind=True, name='gluideai.parse_transcript_task')
def parse_transcript_task(self, file_path: str, webhook_url: str):
    """
    Parse transcript PDF asynchronously.

    Reference: REWRITE_SPECIFICATION.md lines 522-547

    Args:
        file_path: S3 path to PDF file
        webhook_url: Callback URL for results
    """
    task_id = self.request.id
    logger.info(f"[Task {task_id}] Starting transcript parsing for: {file_path}")

    try:
        # In TEST mode, return mock data
        if getattr(settings, 'USE_TEST_MODE', False):
            logger.info(f"[Task {task_id}] Running in TEST mode - using mock data")
            result = _generate_mock_transcript_data()
            _send_webhook(webhook_url, 'success', file_path, task_id, result)
            return result

        # In DATABASE mode, process real transcript
        logger.info(f"[Task {task_id}] Running in DATABASE mode - processing real PDF")

        # Step 1: Download PDF from S3
        pdf_bytes = _download_pdf_from_s3(file_path)
        logger.info(f"[Task {task_id}] Downloaded PDF: {len(pdf_bytes)} bytes")

        # Step 2: Convert PDF to images
        images = _convert_pdf_to_images(pdf_bytes)
        logger.info(f"[Task {task_id}] Converted to {len(images)} images")

        # Step 3: Parse with LLM
        from .llm.lite_llm import LiteLLM
        from .prompts.prompt_manager import PromptManager
        from .models import Transcript

        llm = LiteLLM()
        prompt_manager = PromptManager()

        # Create prompt with images
        prompt = prompt_manager.render_template('transcript_parser.j2')

        # Build messages with images
        messages = [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt},
                    *[{'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{img}'}}
                      for img in images]
                ]
            }
        ]

        # Call LLM with structured output
        result = llm.generate(
            messages=messages,
            response_format=Transcript,
            temperature=0.0
        )

        logger.info(f"[Task {task_id}] LLM returned {len(result.get('courses', []))} courses")

        # Step 4: Send webhook with results
        _send_webhook(webhook_url, 'success', file_path, task_id, result)

        return result

    except Exception as e:
        logger.error(f"[Task {task_id}] Error processing transcript: {str(e)}")
        error_message = f"Error processing transcript: {str(e)}"
        _send_webhook(webhook_url, 'error', file_path, task_id, None, error_message)
        raise


def _generate_mock_transcript_data():
    """Generate mock transcript data for TEST mode."""
    return {
        "courses": [
            {
                "college": "Test Community College",
                "major": "Computer Science",
                "semester": "Fall",
                "year": "2023",
                "course_code": "CS 101",
                "course_title": "Introduction to Programming",
                "credit": "3.00",
                "grade": "A"
            },
            {
                "college": "Test Community College",
                "major": "Computer Science",
                "semester": "Fall",
                "year": "2023",
                "course_code": "MATH 201",
                "course_title": "Calculus I",
                "credit": "4.00",
                "grade": "B+"
            }
        ]
    }


def _download_pdf_from_s3(file_path: str) -> bytes:
    """
    Download PDF from S3.
    Reference: REWRITE_SPECIFICATION.md lines 581-615
    """
    import boto3
    from botocore.exceptions import ClientError

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        response = s3_client.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=file_path
        )

        return response['Body'].read()

    except ClientError as e:
        raise Exception(f"Failed to download PDF from S3: {str(e)}")


def _convert_pdf_to_images(pdf_bytes: bytes) -> list:
    """
    Convert PDF to base64 encoded images.
    Reference: REWRITE_SPECIFICATION.md lines 617-651
    """
    from pdf2image import convert_from_bytes
    import base64
    from io import BytesIO

    try:
        # Convert PDF pages to images
        images = convert_from_bytes(pdf_bytes, dpi=300)

        # Convert to base64
        base64_images = []
        for img in images:
            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=95)
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            base64_images.append(img_base64)

        return base64_images

    except Exception as e:
        raise Exception(f"Failed to convert PDF to images: {str(e)}")


def _send_webhook(webhook_url: str, status: str, file_path: str, task_id: str, data: dict = None, message: str = None):
    """
    Send results to webhook URL.
    Reference: REWRITE_SPECIFICATION.md lines 653-691
    """
    if status == 'success':
        payload = {
            "status": "success",
            "file_path": file_path,
            "task_id": task_id,
            "data": data,
            "message": "Transcript parsed successfully"
        }
    else:
        payload = {
            "status": "error",
            "file_path": file_path,
            "task_id": task_id,
            "message": message or "Error processing transcript"
        }

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.GLUIDE_ME_BACKEND_TOKEN}'
        }

        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code >= 200 and response.status_code < 300:
            logger.info(f"[Task {task_id}] Webhook delivered successfully")
        else:
            logger.warning(f"[Task {task_id}] Webhook returned status {response.status_code}")

    except Exception as e:
        logger.error(f"[Task {task_id}] Failed to deliver webhook: {str(e)}")
