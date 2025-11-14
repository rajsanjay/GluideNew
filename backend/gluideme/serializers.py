"""
Serializers for GluideMe app.
"""

from rest_framework import serializers
from .models import Counselor, CounselorStudentAssignment, GuidanceSession, Recommendation


class CounselorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Counselor
        fields = ['id', 'username', 'email', 'counselor_id', 'school', 'specialization', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CounselorStudentAssignmentSerializer(serializers.ModelSerializer):
    counselor_name = serializers.CharField(source='counselor.user.username', read_only=True)
    student_name = serializers.CharField(source='student.user.username', read_only=True)

    class Meta:
        model = CounselorStudentAssignment
        fields = ['id', 'counselor', 'counselor_name', 'student', 'student_name', 'assigned_date', 'is_active']
        read_only_fields = ['id', 'assigned_date']


class GuidanceSessionSerializer(serializers.ModelSerializer):
    counselor_name = serializers.CharField(source='counselor.user.username', read_only=True)
    student_name = serializers.CharField(source='student.user.username', read_only=True)

    class Meta:
        model = GuidanceSession
        fields = ['id', 'counselor', 'counselor_name', 'student', 'student_name', 'session_date',
                  'duration_minutes', 'session_type', 'notes', 'follow_up_required', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RecommendationSerializer(serializers.ModelSerializer):
    counselor_name = serializers.CharField(source='counselor.user.username', read_only=True)
    student_name = serializers.CharField(source='student.user.username', read_only=True)

    class Meta:
        model = Recommendation
        fields = ['id', 'counselor', 'counselor_name', 'student', 'student_name', 'recommendation_type',
                  'title', 'description', 'priority', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
