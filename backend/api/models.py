"""
Primary database models for the Gluide application.
These models use the 'default' database and have managed=True.
Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1430-1643
"""

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Import course_db models so Django can resolve foreign key references
# These models are used for foreign key relationships from this module
from api import models_course_db  # noqa: F401


class Session(models.Model):
    """Session model - lines 1433-1440"""
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sessions'

    def __str__(self):
        return f"{self.session_name} - {self.user.username}"


class Message(models.Model):
    """Message model - lines 1443-1455"""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    request_time = models.DateTimeField()
    response_time = models.DateTimeField(null=True, blank=True)
    sql_query = models.TextField(null=True, blank=True)
    main_intent = models.CharField(max_length=100, null=True, blank=True)
    sub_intent = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'messages'

    def __str__(self):
        return f"Message {self.message_id}"


class Question(models.Model):
    """Question model - lines 1458-1466"""
    TYPE_CHOICES = [
        ('text', 'Text'),
        ('multiple_choice', 'Multiple Choice'),
        ('single_select', 'Single Select'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    # Use JSONField in test mode (SQLite), ArrayField in database mode (PostgreSQL)
    options = models.JSONField(null=True, blank=True) if getattr(settings, 'USE_TEST_MODE', False) else models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'questions'

    def __str__(self):
        return self.question[:50]


class UserAnswer(models.Model):
    """UserAnswer model - lines 1468-1476"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_answers'

    def __str__(self):
        return f"{self.user.username} - {self.question.question[:30]}"


class UserAttribute(models.Model):
    """UserAttribute model - lines 1478-1489"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'user_attributes'

    def __str__(self):
        return f"{self.user.username} attributes"


class StudentCourse(models.Model):
    """StudentCourse model - lines 1491-1502"""
    STATUS_CHOICES = [
        ('COMPLETE', 'Complete'),
        ('INPROGRESS', 'In Progress'),
        ('PLANNED', 'Planned'),
    ]

    school = models.ForeignKey('School', on_delete=models.CASCADE, db_column='school_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, db_column='course_id')
    year = models.ForeignKey('AcademicYear', on_delete=models.DO_NOTHING, db_column='year_id')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'student_courses'
        unique_together = ['school', 'user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.status}"


class StudentTargetCollege(models.Model):
    """StudentTargetCollege model - lines 1504-1513"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey('School', on_delete=models.CASCADE, db_column='school_id')
    major = models.ForeignKey('Major', on_delete=models.CASCADE, db_column='major_id')

    class Meta:
        db_table = 'student_target_colleges'
        unique_together = ['school', 'user', 'major']

    def __str__(self):
        return f"{self.user.username} target"


class StudentCommunityCollege(models.Model):
    """StudentCommunityCollege model - lines 1515-1523"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey('School', on_delete=models.CASCADE, db_column='school_id')

    class Meta:
        db_table = 'student_community_colleges'
        unique_together = ['school', 'user']

    def __str__(self):
        return f"{self.user.username} community college"


class CounselorDefaultCollege(models.Model):
    """CounselorDefaultCollege model - lines 1525-1532"""
    school = models.ForeignKey('School', on_delete=models.CASCADE, db_column='school_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'counselor_default_colleges'

    def __str__(self):
        return f"Default college"


class CounselorAssignedCollege(models.Model):
    """CounselorAssignedCollege model - lines 1534-1542"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey('School', on_delete=models.CASCADE, db_column='school_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'counselor_assigned_colleges'

    def __str__(self):
        return f"{self.user.username} assigned college"


class ConnectionRequest(models.Model):
    """ConnectionRequest model - lines 1544-1556"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    requesting_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='requested_connections')
    requested_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='incoming_connections')
    school = models.ForeignKey('School', on_delete=models.PROTECT, db_column='school_id')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    actioned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'connection_requests'

    def __str__(self):
        return f"{self.requesting_user.username} -> {self.requested_user.username}"


class File(models.Model):
    """File model - lines 1558-1568"""
    name = models.CharField(max_length=256)
    file_path = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'files'

    def __str__(self):
        return self.name


class Room(models.Model):
    """Room model - lines 1570-1579"""
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='student_rooms')
    counselor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='counselor_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rooms'

    def __str__(self):
        return f"Room: {self.student.username} - {self.counselor.username}"


class StudentDocument(models.Model):
    """StudentDocument model - lines 1581-1589"""
    file = models.ForeignKey(File, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)

    class Meta:
        db_table = 'student_documents'

    def __str__(self):
        return f"Document in room {self.room.id}"


class ChatMessage(models.Model):
    """ChatMessage model - lines 1591-1603"""
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"


class MeetingSchedule(models.Model):
    """MeetingSchedule model - lines 1605-1617"""
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    event_title = models.CharField(max_length=256)
    event_description = models.TextField()
    schedule_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'meeting_schedules'

    def __str__(self):
        return self.event_title


class UserRequestResponse(models.Model):
    """UserRequestResponse model - lines 1619-1629"""
    TYPE_CHOICES = [
        ('schedule_builder', 'Schedule Builder'),
        ('student_guide', 'Student Guide'),
    ]

    request = models.JSONField()
    response = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    class Meta:
        db_table = 'user_requests'

    def __str__(self):
        return f"{self.user.username} - {self.type}"


class StudentCourseSchedule(models.Model):
    """StudentCourseSchedule model - lines 1631-1643"""
    name = models.CharField(max_length=255)
    schedule = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'studet_course_schedule'  # Note: typo preserved from original schema

    def __str__(self):
        return f"{self.user.username} - {self.name}"
