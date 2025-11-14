"""
Admin configuration for GluideAI app.
"""

from django.contrib import admin
from .models import ParsedTranscriptData, ParsedCourse, AIProcessingLog


@admin.register(ParsedTranscriptData)
class ParsedTranscriptDataAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'student_id', 'school_name', 'gpa', 'total_credits', 'created_at']
    search_fields = ['student_name', 'student_id', 'school_name', 'transcript__file_name']
    list_filter = ['school_name', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ParsedCourse)
class ParsedCourseAdmin(admin.ModelAdmin):
    list_display = ['course_code', 'course_name', 'semester', 'year', 'grade', 'credits']
    search_fields = ['course_code', 'course_name', 'parsed_transcript__student_name']
    list_filter = ['year', 'semester', 'grade']


@admin.register(AIProcessingLog)
class AIProcessingLogAdmin(admin.ModelAdmin):
    list_display = ['transcript', 'processing_type', 'status', 'model_used', 'tokens_used', 'processing_time_seconds', 'created_at']
    search_fields = ['transcript__file_name', 'model_used']
    list_filter = ['processing_type', 'status', 'model_used', 'created_at']
    readonly_fields = ['created_at']
