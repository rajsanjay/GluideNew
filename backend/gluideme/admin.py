"""
Admin configuration for GluideMe app.
"""

from django.contrib import admin
from .models import Counselor, CounselorStudentAssignment, GuidanceSession, Recommendation


@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ['counselor_id', 'user', 'school', 'specialization', 'created_at']
    search_fields = ['counselor_id', 'user__username', 'user__email', 'school']
    list_filter = ['school', 'created_at']


@admin.register(CounselorStudentAssignment)
class CounselorStudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ['counselor', 'student', 'assigned_date', 'is_active']
    search_fields = ['counselor__user__username', 'student__user__username']
    list_filter = ['is_active', 'assigned_date']


@admin.register(GuidanceSession)
class GuidanceSessionAdmin(admin.ModelAdmin):
    list_display = ['counselor', 'student', 'session_date', 'session_type', 'duration_minutes', 'follow_up_required']
    search_fields = ['counselor__user__username', 'student__user__username']
    list_filter = ['session_type', 'follow_up_required', 'session_date']


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'counselor', 'recommendation_type', 'priority', 'status', 'created_at']
    search_fields = ['title', 'student__user__username', 'counselor__user__username']
    list_filter = ['recommendation_type', 'priority', 'status', 'created_at']
