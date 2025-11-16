"""
Gluideme app models for counselor dashboard and student management.
These models use UUID primary keys and work in both test and database modes.
Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1886-2235
"""

import uuid
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class College(models.Model):
    """College model - lines 1893-1911"""
    TYPE_CHOICES = [
        ('UC', 'UC'),
        ('CSU', 'CSU'),
        ('Private', 'Private'),
        ('Community', 'Community'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    short_name = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    parent_college = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    course_db_school_id = models.IntegerField(unique=True, null=True, blank=True)

    class Meta:
        db_table = 'gluideme_colleges'

    def __str__(self):
        return self.name


class Course(models.Model):
    """Course model - lines 1913-1933"""
    LEVEL_CHOICES = [
        ('Junior', 'Junior'),
        ('Graduate', 'Graduate'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=255)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    units = models.DecimalField(max_digits=4, decimal_places=2)
    prerequisites = models.JSONField(default=list, blank=True)
    is_transferrable = models.BooleanField(default=False)
    transfer_universities = models.JSONField(default=list, blank=True)
    department = models.CharField(max_length=100, blank=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    class Meta:
        db_table = 'gluideme_courses'

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Program(models.Model):
    """Program model - lines 1935-1964"""
    PROGRAM_TYPE_CHOICES = [
        ('certificate', 'Certificate'),
        ('associate', 'Associate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('transfer', 'Transfer'),
        ('major', 'Major'),
        ('other', 'Other'),
    ]

    program_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program_code = models.CharField(max_length=50, blank=True)
    program_name = models.CharField(max_length=255)
    program_type = models.CharField(max_length=30, choices=PROGRAM_TYPE_CHOICES)
    program_description = models.TextField(blank=True)
    degree_url = models.URLField(blank=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    total_credits_required = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    duration_years = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    year = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    course_db_program_id = models.IntegerField(null=True, blank=True)
    academic_year_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'gluideme_programs'

    def __str__(self):
        return self.program_name


class Department(models.Model):
    """Department model - lines 1966-1976"""
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department_name = models.CharField(max_length=200, unique=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    class Meta:
        db_table = 'gluideme_departments'

    def __str__(self):
        return self.department_name


class Students(models.Model):
    """Students model - lines 1978-2012"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    enrollment_status = models.CharField(max_length=50)
    program = models.CharField(max_length=200, blank=True)
    major = models.CharField(max_length=200, blank=True)
    gpa = models.CharField(max_length=10, blank=True)
    academic_standing = models.CharField(max_length=50, blank=True)
    stage = models.CharField(max_length=50, blank=True)
    pathway = models.CharField(max_length=200, blank=True)
    advisor = models.CharField(max_length=200, blank=True)
    target_graduation = models.CharField(max_length=50, blank=True)
    transfer_target = models.CharField(max_length=200, blank=True)
    skills = models.JSONField(default=list, blank=True)
    goals = models.JSONField(default=list, blank=True)
    last_contact = models.CharField(max_length=100, blank=True)
    next_followup = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gluideme_students'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentDemographics(models.Model):
    """StudentDemographics model - lines 2014-2066"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    pers_info_age = models.IntegerField(null=True, blank=True)
    pers_info_primary_language_spoken_at_home = models.CharField(max_length=100, blank=True)
    pers_info_other_language_spoken_at_home = models.CharField(max_length=100, blank=True)
    edu_back_first_in_family_to_attent_college = models.CharField(max_length=50, blank=True)
    edu_back_parent_education = models.CharField(max_length=100, blank=True)
    edu_back_have_attended_college_fefore = models.CharField(max_length=50, blank=True)
    fin_info_eligible_for_pell_grant = models.CharField(max_length=50, blank=True)
    fin_info_expected_primary_funding_source = models.CharField(max_length=100, blank=True)
    fin_info_other_funding_source = models.TextField(blank=True)
    life_employment_status = models.CharField(max_length=100, blank=True)
    life_have_dependents = models.CharField(max_length=50, blank=True)
    life_current_living_situation = models.CharField(max_length=100, blank=True)
    geo_how_travel_distance_willing_for_classes = models.CharField(max_length=100, blank=True)
    geo_primary_transport = models.CharField(max_length=100, blank=True)
    sched_units_per_semester = models.CharField(max_length=50, blank=True)
    sched_class_schedule_best_fits = models.JSONField(default=list, blank=True)
    support_services_helpful = models.JSONField(default=list, blank=True)
    back_ethnic_background = models.CharField(max_length=100, blank=True)
    back_other_ethnic = models.TextField(blank=True)
    back_veteran_status = models.CharField(max_length=50, blank=True)
    back_disability_status = models.CharField(max_length=50, blank=True)
    goals_primary_goal_to_attend_college = models.CharField(max_length=200, blank=True)
    goals_other = models.TextField(blank=True)
    goals_timeline_to_complete_goal = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gluideme_student_demographics'

    def __str__(self):
        return f"Demographics for {self.student.first_name} {self.student.last_name}"


class StudentPathways(models.Model):
    """StudentPathways model - lines 2068-2093"""
    PATHWAY_TYPE_CHOICES = [
        ('associate_certificate', 'Associate Certificate'),
        ('transfer', 'Transfer'),
        ('continuing_education', 'Continuing Education'),
    ]
    INTEREST_LEVEL_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    pathway_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    education_plan = models.ForeignKey('EducationPlan', on_delete=models.SET_NULL, null=True, blank=True)
    pathway_type = models.CharField(max_length=50, choices=PATHWAY_TYPE_CHOICES)
    pathway_name = models.CharField(max_length=255)
    interest_level = models.CharField(max_length=20, choices=INTEREST_LEVEL_CHOICES)
    priority = models.IntegerField(null=True, blank=True)
    target_institutions = models.JSONField(default=list, blank=True)
    target_start_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'gluideme_student_pathways'

    def __str__(self):
        return f"{self.student.first_name} - {self.pathway_name}"


class StudentGoal(models.Model):
    """StudentGoal model - lines 2095-2113"""
    GOAL_TYPE_CHOICES = [
        ('academic', 'Academic'),
        ('career', 'Career'),
        ('transfer', 'Transfer'),
        ('personal', 'Personal'),
    ]
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('deferred', 'Deferred'),
        ('cancelled', 'Cancelled'),
    ]

    goal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    goal_description = models.TextField()
    target_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    progress_notes = models.TextField(blank=True)

    class Meta:
        db_table = 'gluideme_student_goals'

    def __str__(self):
        return f"{self.student.first_name} - {self.goal_type}"


class CounselingSession(models.Model):
    """CounselingSession model - lines 2115-2134"""
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    session_date = models.DateTimeField()
    session_type = models.CharField(max_length=50)
    session_notes = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gluideme_counseling_sessions'

    def __str__(self):
        return f"Session with {self.student.first_name} on {self.session_date}"


class EducationPlan(models.Model):
    """EducationPlan model - lines 2136-2159"""
    PLAN_TYPE_CHOICES = [
        ('degree', 'Degree'),
        ('transfer', 'Transfer'),
        ('certificate', 'Certificate'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]

    plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    target_completion = models.DateField(null=True, blank=True)
    advisor = models.ForeignKey(User, on_delete=models.PROTECT)
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    total_credits = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'gluideme_education_plans'

    def __str__(self):
        return f"{self.student.first_name} - {self.plan_name}"


class StudentTarget(models.Model):
    """StudentTarget model - lines 2161-2183"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=200)
    program_name = models.CharField(max_length=200)
    priority = models.IntegerField()
    target_graduation = models.CharField(max_length=50)
    application_status = models.CharField(max_length=50)
    application_date = models.DateField(null=True, blank=True)
    decision_date = models.DateField(null=True, blank=True)
    minimum_gpa_required = models.CharField(max_length=10, blank=True)
    current_gpa_gap = models.CharField(max_length=10, blank=True)
    additional_requirements = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    target_college = models.ForeignKey(College, on_delete=models.CASCADE)
    target_program = models.ForeignKey(Program, on_delete=models.CASCADE)

    class Meta:
        db_table = 'gluideme_student_targets'

    def __str__(self):
        return f"{self.student.first_name} -> {self.college_name}"


class CounselorProfile(models.Model):
    """CounselorProfile model - lines 2185-2203"""
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('phone', 'Phone'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone_number = models.CharField(max_length=20)
    office_location = models.CharField(max_length=255)
    preferred_contact_method = models.CharField(max_length=10, choices=CONTACT_METHOD_CHOICES, default='email')
    email_notifications = models.BooleanField(default=True)
    sms_alerts = models.BooleanField(default=False)
    site_code = models.CharField(max_length=50)
    site_name = models.ForeignKey(College, on_delete=models.CASCADE, null=True, blank=True)
    site_version = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gluideme_counselor_profiles'

    def __str__(self):
        return f"{self.user.get_full_name()} - Counselor"


class AIRecommendation(models.Model):
    """AIRecommendation model - lines 2204-2216"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, default='queued')
    ai_recommendation = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gluideme_ai_recommendations'

    def __str__(self):
        return f"Recommendation for {self.student.first_name} - {self.status}"


class Document(models.Model):
    """Document model - lines 2218-2235"""
    CATEGORY_CHOICES = [
        ('transcript', 'Transcript'),
        ('plan', 'Plan'),
        ('form', 'Form'),
        ('report', 'Report'),
        ('other', 'Other'),
        ('counselling', 'Counselling'),
    ]

    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    session = models.ForeignKey(CounselingSession, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    file_path = models.CharField(max_length=500)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    document_content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gluideme_documents'

    def __str__(self):
        return f"{self.title or self.filename} - {self.student.first_name}"
