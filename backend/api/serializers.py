"""
Serializers for the API app.
"""

from rest_framework import serializers
from .models import Student, Transcript, SavedCourse
from .models_course_db import Course, CourseOffering


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'student_id', 'grade_level', 'school', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TranscriptSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)

    class Meta:
        model = Transcript
        fields = ['id', 'student', 'student_name', 'file_name', 'file_url', 'upload_date',
                  'processing_status', 'parsed_data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'upload_date', 'processing_status', 'parsed_data', 'created_at', 'updated_at']


class SavedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedCourse
        fields = ['id', 'student', 'course_code', 'course_name', 'saved_at']
        read_only_fields = ['id', 'saved_at']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'description', 'credits', 'department', 'level', 'prerequisites']


class CourseOfferingSerializer(serializers.ModelSerializer):
    course_info = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = CourseOffering
        fields = ['id', 'course', 'course_info', 'section', 'semester', 'year',
                  'instructor', 'capacity', 'enrolled', 'schedule']
