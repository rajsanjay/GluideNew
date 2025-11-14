"""
Admin configuration for the API app.
"""

from django.contrib import admin
from .models import Student, Transcript, SavedCourse


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'user', 'grade_level', 'school', 'created_at']
    search_fields = ['student_id', 'user__username', 'user__email', 'school']
    list_filter = ['grade_level', 'school', 'created_at']


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ['student', 'file_name', 'upload_date', 'processing_status']
    search_fields = ['student__user__username', 'file_name']
    list_filter = ['processing_status', 'upload_date']
    readonly_fields = ['upload_date', 'parsed_data']


@admin.register(SavedCourse)
class SavedCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course_code', 'course_name', 'saved_at']
    search_fields = ['student__user__username', 'course_code', 'course_name']
    list_filter = ['saved_at']
