from rest_framework import serializers
from .models import (
    Students, StudentDemographics, StudentGoal, StudentPathways,
    StudentTarget, College, Course, Program, EducationPlan,
    CounselorProfile, AIRecommendation, Document, Department,
    CounselingSession, StudentTranscripts, TranscriptWebhookCourses
)
from django.contrib.auth.models import User


class StudentsSerializer(serializers.ModelSerializer):
    """
    Serializer for Students model.
    Used for GET/POST/PUT /backend/api/gluideme/student_info/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1014-1094
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Students
        fields = [
            'id', 'full_name', 'first_name', 'last_name', 'student_id',
            'email', 'phone', 'enrollment_status', 'program', 'major',
            'gpa', 'academic_standing', 'stage', 'pathway', 'advisor',
            'target_graduation', 'transfer_target', 'skills', 'goals',
            'last_contact', 'next_followup', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class StudentDemographicsSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentDemographics model.
    Used for GET/POST/PUT /backend/api/gluideme/student-demographics/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1014-1066
    """
    class Meta:
        model = StudentDemographics
        fields = [
            'id', 'student', 'pers_info_age',
            'pers_info_primary_language_spoken_at_home',
            'pers_info_other_language_spoken_at_home',
            'edu_back_first_in_family_to_attent_college',
            'edu_back_parent_education',
            'edu_back_have_attended_college_fefore',
            'fin_info_eligible_for_pell_grant',
            'fin_info_expected_primary_funding_source',
            'fin_info_other_funding_source',
            'life_employment_status',
            'life_have_dependents',
            'life_current_living_situation',
            'geo_how_travel_distance_willing_for_classes',
            'geo_primary_transport',
            'sched_units_per_semester',
            'sched_class_schedule_best_fits',
            'support_services_helpful',
            'back_ethnic_background',
            'back_other_ethnic',
            'back_veteran_status',
            'back_disability_status',
            'goals_primary_goal_to_attend_college',
            'goals_other',
            'goals_timeline_to_complete_goal',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class StudentGoalSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentGoal model.
    Used for GET/POST/PUT /backend/api/gluideme/student-goal/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1098-1126
    """
    class Meta:
        model = StudentGoal
        fields = [
            'goal_id', 'student', 'goal_type', 'goal_description',
            'target_date', 'priority', 'status', 'progress_notes'
        ]
        read_only_fields = ['goal_id']


class StudentPathwaysSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentPathways model.
    Used for GET/POST /backend/api/gluideme/student-pathways/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1128-1158
    """
    class Meta:
        model = StudentPathways
        fields = [
            'pathway_id', 'student', 'education_plan', 'pathway_type',
            'pathway_name', 'interest_level', 'priority',
            'target_institutions', 'target_start_date', 'notes'
        ]
        read_only_fields = ['pathway_id']


class CollegeSerializer(serializers.ModelSerializer):
    """
    Serializer for College model.
    Used for GET/POST /backend/api/gluideme/colleges/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1162-1189
    """
    class Meta:
        model = College
        fields = [
            'id', 'name', 'short_name', 'type', 'location',
            'website', 'parent_college', 'course_db_school_id'
        ]
        read_only_fields = ['id']


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model (gluideme app).
    Used for GET/POST /backend/api/gluideme/courses/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1191-1225
    """
    class Meta:
        model = Course
        fields = [
            'id', 'course_code', 'course_name', 'level', 'units',
            'prerequisites', 'is_transferrable', 'transfer_universities',
            'department', 'college'
        ]
        read_only_fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""
    class Meta:
        model = Department
        fields = ['department_id', 'department_name', 'college']
        read_only_fields = ['department_id']


class ProgramSerializer(serializers.ModelSerializer):
    """
    Serializer for Program model.
    Used for GET/POST /backend/api/gluideme/programs/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1227-1257
    """
    class Meta:
        model = Program
        fields = [
            'program_id', 'program_code', 'program_name', 'program_type',
            'program_description', 'degree_url', 'college', 'department',
            'total_credits_required', 'duration_years', 'year',
            'is_active', 'course_db_program_id', 'academic_year_id'
        ]
        read_only_fields = ['program_id']


class EducationPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for EducationPlan model.
    Used for GET/POST /backend/api/gluideme/education-plan/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1259-1288
    """
    class Meta:
        model = EducationPlan
        fields = [
            'plan_id', 'student', 'plan_name', 'plan_type', 'status',
            'target_completion', 'advisor', 'is_approved',
            'approval_date', 'total_credits', 'notes'
        ]
        read_only_fields = ['plan_id']


class StudentTargetSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentTarget model.
    """
    class Meta:
        model = StudentTarget
        fields = [
            'id', 'student', 'college_name', 'program_name', 'priority',
            'target_graduation', 'application_status', 'application_date',
            'decision_date', 'minimum_gpa_required', 'current_gpa_gap',
            'additional_requirements', 'notes', 'is_active',
            'target_college', 'target_program'
        ]
        read_only_fields = ['id']


class CounselorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for CounselorProfile model.
    Used for GET/PUT /backend/api/gluideme/counselor-profile/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1373-1392
    """
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    site_name_detail = serializers.SerializerMethodField()

    class Meta:
        model = CounselorProfile
        fields = [
            'id', 'user', 'full_name', 'email', 'phone_number',
            'office_location', 'preferred_contact_method',
            'email_notifications', 'sms_alerts', 'site_code',
            'site_name', 'site_name_detail', 'site_version',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}".strip()
        return ""

    def get_email(self, obj):
        return obj.user.email if obj.user else ""

    def get_site_name_detail(self, obj):
        if obj.site_name:
            return {
                'id': str(obj.site_name.id),
                'name': obj.site_name.name
            }
        return None


class AIRecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer for AIRecommendation model.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1340-1371
    """
    class Meta:
        model = AIRecommendation
        fields = [
            'id', 'student', 'task_id', 'status',
            'ai_recommendation', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for Document model.
    Used for POST /backend/api/gluideme/documents/upload/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1393-1419
    """
    class Meta:
        model = Document
        fields = [
            'document_id', 'student', 'session', 'title', 'filename',
            'file_type', 'category', 'file_path', 'uploaded_by',
            'document_content', 'created_at'
        ]
        read_only_fields = ['document_id', 'created_at']


class CounselingSessionSerializer(serializers.ModelSerializer):
    """Serializer for CounselingSession model."""
    class Meta:
        model = CounselingSession
        fields = [
            'session_id', 'student', 'counselor', 'session_date',
            'session_type', 'session_notes', 'follow_up_required',
            'follow_up_date', 'created_at'
        ]
        read_only_fields = ['session_id', 'created_at']


class TranscriptWebhookCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for TranscriptWebhookCourses model (nested in transcript list).
    Used for displaying parsed course data in transcript list view.
    """
    class Meta:
        model = TranscriptWebhookCourses
        fields = [
            'id', 'college', 'major', 'semester', 'year',
            'course_code', 'course_title', 'credit', 'grade', 'status'
        ]


class StudentTranscriptSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentTranscripts model.
    Used for transcript upload, status tracking, and list view with nested courses.
    """
    webhook_courses = TranscriptWebhookCourseSerializer(many=True, read_only=True)

    class Meta:
        model = StudentTranscripts
        fields = [
            'id', 'file_name', 'file_url', 'status',
            'uploaded_at', 'webhook_courses'
        ]
        read_only_fields = ['id', 'uploaded_at']


class TranscriptWebhookCoursesSerializer(serializers.ModelSerializer):
    """
    Serializer for TranscriptWebhookCourses model.
    Used for receiving parsed course data from gluideai webhook.
    """
    class Meta:
        model = TranscriptWebhookCourses
        fields = [
            'id', 'transcript', 'college', 'major', 'semester',
            'year', 'course_code', 'course_title', 'credit',
            'grade', 'status', 'received_at'
        ]
        read_only_fields = ['id', 'received_at']
