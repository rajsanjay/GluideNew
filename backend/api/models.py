"""
Main database models for the Gluide application.
These models use the 'default' database (gluide_me).
"""

from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """Student profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=50, unique=True)
    grade_level = models.IntegerField()
    school = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"


class Transcript(models.Model):
    """Student transcript model."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transcripts')
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(max_length=500, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    processing_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    parsed_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transcripts'
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.student.user.username} - {self.file_name}"


class SavedCourse(models.Model):
    """Student saved courses."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='saved_courses')
    course_code = models.CharField(max_length=50)
    course_name = models.CharField(max_length=200)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'saved_courses'
        unique_together = ['student', 'course_code']
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.student.user.username} - {self.course_code}"
