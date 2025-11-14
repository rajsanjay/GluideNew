"""
Models for GluideMe counselor features.
"""

from django.db import models
from django.contrib.auth.models import User
from api.models import Student


class Counselor(models.Model):
    """Counselor profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='counselor_profile')
    counselor_id = models.CharField(max_length=50, unique=True)
    school = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'counselors'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.counselor_id}"


class CounselorStudentAssignment(models.Model):
    """Assignment of students to counselors."""
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='student_assignments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='counselor_assignments')
    assigned_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'counselor_student_assignments'
        unique_together = ['counselor', 'student']
        ordering = ['-assigned_date']

    def __str__(self):
        return f"{self.counselor.user.username} -> {self.student.user.username}"


class GuidanceSession(models.Model):
    """Counselor guidance session model."""
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='sessions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='guidance_sessions')
    session_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    session_type = models.CharField(
        max_length=50,
        choices=[
            ('academic', 'Academic Planning'),
            ('career', 'Career Guidance'),
            ('college', 'College Counseling'),
            ('personal', 'Personal Development'),
        ],
        default='academic'
    )
    notes = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'guidance_sessions'
        ordering = ['-session_date']

    def __str__(self):
        return f"{self.counselor.user.username} - {self.student.user.username} ({self.session_date.date()})"


class Recommendation(models.Model):
    """Course or academic recommendations."""
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='recommendations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='recommendations')
    recommendation_type = models.CharField(
        max_length=50,
        choices=[
            ('course', 'Course Recommendation'),
            ('program', 'Program Recommendation'),
            ('activity', 'Extracurricular Activity'),
        ],
        default='course'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=[
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
        ],
        default='medium'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('declined', 'Declined'),
            ('completed', 'Completed'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recommendations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.student.user.username}"
