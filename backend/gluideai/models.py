"""
Models for GluideAI transcript parsing.
"""

from django.db import models
from api.models import Transcript


class ParsedTranscriptData(models.Model):
    """Parsed transcript data extracted by AI."""
    transcript = models.OneToOneField(Transcript, on_delete=models.CASCADE, related_name='parsed_details')
    student_name = models.CharField(max_length=200, blank=True)
    student_id = models.CharField(max_length=50, blank=True)
    school_name = models.CharField(max_length=200, blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    total_credits = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    courses_data = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'parsed_transcript_data'
        ordering = ['-created_at']

    def __str__(self):
        return f"Parsed data for {self.transcript.file_name}"


class ParsedCourse(models.Model):
    """Individual course parsed from transcript."""
    parsed_transcript = models.ForeignKey(ParsedTranscriptData, on_delete=models.CASCADE, related_name='courses')
    course_code = models.CharField(max_length=50)
    course_name = models.CharField(max_length=200)
    semester = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(null=True, blank=True)
    grade = models.CharField(max_length=5, blank=True)
    credits = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'parsed_courses'
        ordering = ['year', 'semester', 'course_code']

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class AIProcessingLog(models.Model):
    """Log of AI processing attempts and results."""
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, related_name='processing_logs')
    processing_type = models.CharField(
        max_length=50,
        choices=[
            ('extraction', 'Data Extraction'),
            ('validation', 'Data Validation'),
            ('enhancement', 'Data Enhancement'),
        ],
        default='extraction'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('started', 'Started'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='started'
    )
    model_used = models.CharField(max_length=50, default='gpt-4')
    tokens_used = models.IntegerField(null=True, blank=True)
    processing_time_seconds = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    error_message = models.TextField(blank=True)
    result_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_processing_logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.processing_type} - {self.status} ({self.created_at})"
