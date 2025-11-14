"""
Serializers for GluideAI app.
"""

from rest_framework import serializers
from .models import ParsedTranscriptData, ParsedCourse, AIProcessingLog


class ParsedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsedCourse
        fields = ['id', 'course_code', 'course_name', 'semester', 'year', 'grade', 'credits', 'created_at']
        read_only_fields = ['id', 'created_at']


class ParsedTranscriptDataSerializer(serializers.ModelSerializer):
    courses = ParsedCourseSerializer(many=True, read_only=True)
    transcript_file_name = serializers.CharField(source='transcript.file_name', read_only=True)

    class Meta:
        model = ParsedTranscriptData
        fields = ['id', 'transcript', 'transcript_file_name', 'student_name', 'student_id', 'school_name',
                  'graduation_date', 'gpa', 'total_credits', 'courses_data', 'courses', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AIProcessingLogSerializer(serializers.ModelSerializer):
    transcript_file_name = serializers.CharField(source='transcript.file_name', read_only=True)

    class Meta:
        model = AIProcessingLog
        fields = ['id', 'transcript', 'transcript_file_name', 'processing_type', 'status', 'model_used',
                  'tokens_used', 'processing_time_seconds', 'error_message', 'result_data', 'created_at']
        read_only_fields = ['id', 'created_at']
