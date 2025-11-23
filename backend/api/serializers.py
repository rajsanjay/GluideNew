from rest_framework import serializers
from .models import Session, Message, Question, UserAnswer, UserAttribute
from .models import StudentCourse, StudentTargetCollege, StudentCommunityCollege
from .models import ConnectionRequest, Room, ChatMessage, File, MeetingSchedule
from .models import CounselorAssignedCollege
from .models_course_db import School, Course as CourseDB, Major, AcademicYear
from .models_course_db import SchoolAddress, AcademicSemester
from django.contrib.auth.models import User, Group


class SessionSerializer(serializers.ModelSerializer):
    """
    Serializer for Session model.
    Used for GET /backend/api/session/ and POST /backend/api/session/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 123-165
    """
    class Meta:
        model = Session
        fields = ['session_id', 'session_name', 'created_at', 'user']
        read_only_fields = ['session_id', 'created_at']

    def create(self, validated_data):
        # Auto-set user from request context
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    Used for GET/POST /backend/api/message/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 167-205
    """
    class Meta:
        model = Message
        fields = [
            'message_id', 'session', 'question', 'answer',
            'request_time', 'response_time', 'sql_query',
            'main_intent', 'sub_intent'
        ]
        read_only_fields = ['message_id']


class SchoolSerializer(serializers.ModelSerializer):
    """
    Serializer for School model from course_db.
    Nested in StudentCourse responses.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 405-421
    """
    class Meta:
        model = School
        fields = [
            'school_id', 'name', 'assist_university_id',
            'is_community_college', 'alternate_names'
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model from course_db.
    Nested in StudentCourse responses.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 423-442
    """
    class Meta:
        model = CourseDB
        fields = ['id', 'course_code', 'course_name', 'credits']


class AcademicYearSerializer(serializers.ModelSerializer):
    """
    Serializer for AcademicYear model from course_db.
    Nested in StudentCourse responses.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 462-474
    """
    class Meta:
        model = AcademicYear
        fields = ['id', 'year', 'assist_year_id', 'code']


class MajorSerializer(serializers.ModelSerializer):
    """
    Serializer for Major model from course_db.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 444-460
    """
    class Meta:
        model = Major
        fields = ['id', 'major_name', 'major_slug']


class StudentCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentCourse model.
    Includes nested school, course, and year data.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 207-259
    """
    school = SchoolSerializer(read_only=True)
    course = CourseDetailSerializer(read_only=True)
    year = AcademicYearSerializer(read_only=True)

    # Write fields for creating/updating
    school_id = serializers.IntegerField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)
    year_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StudentCourse
        fields = [
            'id', 'user', 'school', 'course', 'year', 'status',
            'school_id', 'course_id', 'year_id'
        ]
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        # Auto-set user from request
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)


class StudentTargetCollegeSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentTargetCollege model.
    Used for POST /backend/api/student-target-collage/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 261-295
    """
    school = SchoolSerializer(read_only=True)
    major = MajorSerializer(read_only=True)

    school_id = serializers.IntegerField(write_only=True)
    major_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StudentTargetCollege
        fields = [
            'id', 'user', 'school', 'major',
            'school_id', 'major_id'
        ]
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user

        # Get foreign key values
        school_id = validated_data.pop('school_id')
        major_id = validated_data.pop('major_id')

        # Set foreign keys by ID
        validated_data['school_id'] = school_id
        validated_data['major_id'] = major_id

        return super().create(validated_data)


class StudentCommunityCollegeSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentCommunityCollege model.
    Used for POST /backend/api/student-community-collage/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 297-325
    """
    school = SchoolSerializer(read_only=True)
    school_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = StudentCommunityCollege
        fields = ['id', 'user', 'school', 'school_id']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user

        school_id = validated_data.pop('school_id')
        validated_data['school_id'] = school_id

        return super().create(validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model."""
    class Meta:
        model = Question
        fields = ['id', 'question', 'type', 'options']


class UserAnswerSerializer(serializers.ModelSerializer):
    """Serializer for UserAnswer model with nested question."""
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'answer', 'created_at']


class UserAttributeSerializer(serializers.ModelSerializer):
    """Serializer for UserAttribute model."""
    class Meta:
        model = UserAttribute
        fields = [
            'is_verified', 'mobile_number', 'zip_code',
            'latitude', 'longitude'
        ]


class DesignationSerializer(serializers.Serializer):
    """Serializer for user designation/group."""
    id = serializers.IntegerField()
    name = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Complete user profile serializer.
    Used for GET /backend/api/user/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 327-362
    """
    user_answer = UserAnswerSerializer(many=True, read_only=True, source='useranswer_set')
    user_attribute = UserAttributeSerializer(read_only=True, source='userattribute')
    designation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_answer', 'user_attribute', 'designation'
        ]

    def get_designation(self, obj):
        """Get user's group/designation."""
        group = obj.groups.first()
        if group:
            return {'id': group.id, 'name': group.name}
        return None


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for PUT /backend/api/user/"""
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password'
        ]
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class SchoolAddressSerializer(serializers.ModelSerializer):
    """
    Serializer for SchoolAddress model with geography data.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 488-515
    """
    class Meta:
        model = SchoolAddress
        fields = [
            'address_id', 'address_type', 'address1', 'address2',
            'city', 'state', 'zip', 'latitude', 'longitude'
        ]


class SchoolWithAddressesSerializer(serializers.ModelSerializer):
    """
    School serializer with nested addresses.
    Used for GET /backend/api/schools/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 488-515
    """
    addresses = SchoolAddressSerializer(many=True, read_only=True, source='schooladdress_set')

    class Meta:
        model = School
        fields = [
            'school_id', 'name', 'assist_university_id',
            'alternate_names', 'is_community_college', 'addresses'
        ]


class AcademicSemesterSerializer(serializers.ModelSerializer):
    """
    Serializer for AcademicSemester model.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 476-486
    """
    class Meta:
        model = AcademicSemester
        fields = ['id', 'name']


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatMessage model.
    Used for nested representation in Room detail view.
    """
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message', 'created_at', 'is_read']


class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for Room model.
    Used for nested representation in ConnectionRequest.
    """
    student = UserProfileSerializer(read_only=True)
    counselor = UserProfileSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'student', 'counselor', 'created_at']
        read_only_fields = ['id', 'created_at']


class RoomDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Room model with chat messages.
    Used for GET /backend/api/rooms/{id}/

    Includes full user profiles and all chat messages in the room.
    """
    student = UserProfileSerializer(read_only=True)
    counselor = UserProfileSerializer(read_only=True)
    chat_messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'student', 'counselor', 'created_at', 'chat_messages']


class ConnectionRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for ConnectionRequest model.
    Used for POST /backend/api/connection-requests/ and GET /backend/api/connection-requests/

    Read fields show full nested objects (users, school, room).
    Write fields accept IDs for creating requests.
    """
    requesting_user = UserProfileSerializer(read_only=True)
    requested_user = UserProfileSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    # Write fields
    requested_user_id = serializers.IntegerField(write_only=True)
    school_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ConnectionRequest
        fields = [
            'id', 'requesting_user', 'requested_user', 'school',
            'status', 'created_at', 'actioned_at', 'room',
            'requested_user_id', 'school_id'
        ]
        read_only_fields = ['id', 'requesting_user', 'status', 'created_at', 'actioned_at', 'room']

    def create(self, validated_data):
        # Auto-set requesting_user from authenticated user
        validated_data['requesting_user'] = self.context['request'].user

        # Extract IDs for foreign key fields
        requested_user_id = validated_data.pop('requested_user_id')
        school_id = validated_data.pop('school_id')

        # Create connection request with foreign key IDs
        return ConnectionRequest.objects.create(
            requesting_user=validated_data['requesting_user'],
            requested_user_id=requested_user_id,
            school_id=school_id
        )


class FileSerializer(serializers.ModelSerializer):
    """
    Serializer for File model.
    Used for GET /backend/api/files/

    Returns full file information including uploader details.
    """
    uploaded_by = UserProfileSerializer(read_only=True)

    class Meta:
        model = File
        fields = ['id', 'name', 'file_path', 'uploaded_at', 'uploaded_by']
        read_only_fields = ['id', 'uploaded_at', 'uploaded_by']


class FileUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading files.
    Used for POST /backend/api/files/

    Accepts file upload and auto-sets uploaded_by from request user.
    """
    class Meta:
        model = File
        fields = ['id', 'name', 'file_path', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

    def create(self, validated_data):
        # Auto-set uploaded_by from authenticated user
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class MeetingScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for MeetingSchedule model.
    Used for managing meeting schedules between students and counselors.

    Includes full creator details and auto-sets created_by from request user.
    """
    created_by = UserProfileSerializer(read_only=True)

    class Meta:
        model = MeetingSchedule
        fields = [
            'id', 'room', 'event_title', 'event_description',
            'schedule_time', 'created_at', 'created_by'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']

    def create(self, validated_data):
        # Auto-set created_by from authenticated user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CounselorAssignedCollegeSerializer(serializers.ModelSerializer):
    """
    Serializer for CounselorAssignedCollege model.
    Used for GET /backend/api/counselor-assigned-college/

    Returns counselor's assigned colleges with nested school details.
    """
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = CounselorAssignedCollege
        fields = ['id', 'user', 'school', 'is_active']
