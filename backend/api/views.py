from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.db.models import Q
from django.db import models
from django.utils import timezone
from .models import Session, Message, Question, UserAnswer, UserAttribute
from .models import StudentCourse, StudentTargetCollege, StudentCommunityCollege
from .models import ConnectionRequest, Room, File, MeetingSchedule, CounselorAssignedCollege
from .models_course_db import (
    School, Course as CourseDB, Major,
    AcademicYear, AcademicSemester
)
from .serializers import (
    SessionSerializer, MessageSerializer,
    StudentCourseSerializer, StudentTargetCollegeSerializer,
    StudentCommunityCollegeSerializer,
    UserProfileSerializer, UserUpdateSerializer, UserAttributeSerializer,
    SchoolSerializer, CourseDetailSerializer, MajorSerializer,
    AcademicYearSerializer, AcademicSemesterSerializer,
    SchoolWithAddressesSerializer,
    ConnectionRequestSerializer, RoomSerializer, RoomDetailSerializer,
    FileSerializer, FileUploadSerializer,
    MeetingScheduleSerializer,
    CounselorAssignedCollegeSerializer
)


class SessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Session management.

    Endpoints:
    - GET /backend/api/session/ - List all sessions for user
    - POST /backend/api/session/ - Create new session
    - GET /backend/api/session/{id}/ - Retrieve session
    - PUT /backend/api/session/{id}/ - Update session
    - DELETE /backend/api/session/{id}/ - Delete session

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 123-165
    """
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        # Only return sessions for authenticated user
        return Session.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message management.

    Endpoints:
    - GET /backend/api/message/ - List all messages
    - POST /backend/api/message/ - Create new message
    - GET /backend/api/message/{id}/ - Retrieve message

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 167-205
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Message.objects.all()


class StudentCourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for student course management.

    Endpoints:
    - GET /backend/api/student-courses/ - List all courses for user
    - POST /backend/api/student-courses/ - Add a course
    - GET /backend/api/student-courses/{id}/ - Retrieve course
    - PUT /backend/api/student-courses/{id}/ - Update course
    - DELETE /backend/api/student-courses/{id}/ - Remove course

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 207-259
    """
    serializer_class = StudentCourseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return StudentCourse.objects.filter(user=self.request.user).select_related(
            'school', 'course', 'year'
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudentTargetCollegeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for student target college management.

    Endpoints:
    - GET /backend/api/student-target-collage/ - List target colleges
    - POST /backend/api/student-target-collage/ - Add target college
    - DELETE /backend/api/student-target-collage/{id}/ - Remove target college

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 261-295
    """
    serializer_class = StudentTargetCollegeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    http_method_names = ['get', 'post', 'delete']  # No PUT/PATCH

    def get_queryset(self):
        return StudentTargetCollege.objects.filter(user=self.request.user).select_related(
            'school', 'major'
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudentCommunityCollegeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for student community college management.

    Endpoints:
    - GET /backend/api/student-community-collage/ - List community colleges
    - POST /backend/api/student-community-collage/ - Add community college
    - DELETE /backend/api/student-community-collage/{id}/ - Remove community college

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 297-325
    """
    serializer_class = StudentCommunityCollegeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return StudentCommunityCollege.objects.filter(user=self.request.user).select_related('school')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileView(APIView):
    """
    User profile view.

    Endpoints:
    - GET /backend/api/user/ - Get user profile
    - PUT /backend/api/user/ - Update user profile

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 327-375
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAttributeView(APIView):
    """
    User attribute view.

    Endpoints:
    - GET /backend/api/user-info/ - Get user attributes
    - PUT /backend/api/user-info/ - Update user attributes

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 376-398
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        try:
            user_attr = request.user.userattribute
            serializer = UserAttributeSerializer(user_attr)
            return Response(serializer.data)
        except UserAttribute.DoesNotExist:
            return Response({
                'is_verified': False,
                'mobile_number': None,
                'zip_code': None,
                'latitude': None,
                'longitude': None
            })

    def put(self, request):
        user_attr, created = UserAttribute.objects.get_or_create(
            user=request.user
        )

        # Handle geolocation from zip code
        if 'zip_code' in request.data:
            # In TEST mode, use mock coordinates
            if getattr(settings, 'USE_TEST_MODE', False):
                request.data['latitude'] = 37.7749
                request.data['longitude'] = -122.4194
            else:
                # In DATABASE mode, use real geolocation
                from geopy.geocoders import Nominatim
                try:
                    geolocator = Nominatim(user_agent="gluide-me")
                    location = geolocator.geocode(request.data['zip_code'])
                    if location:
                        request.data['latitude'] = location.latitude
                        request.data['longitude'] = location.longitude
                except Exception:
                    pass  # Keep existing or null values

        serializer = UserAttributeSerializer(
            user_attr,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolSearchView(APIView):
    """
    Search schools/colleges.

    GET /backend/api/collage/?search=<query>&limit=<n>
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 404-421
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        search = request.query_params.get('search', '')
        limit = int(request.query_params.get('limit', 10))

        # Query course_db using correct database
        db_name = 'course_db'

        queryset = School.objects.using(db_name).filter(
            Q(name__icontains=search)
        )[:limit]

        serializer = SchoolSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseSearchView(APIView):
    """
    Search courses.

    GET /backend/api/course/?search=<query>&school_id=<id>&limit=<n>
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 423-442
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        search = request.query_params.get('search', '')
        school_id = request.query_params.get('school_id')
        limit = int(request.query_params.get('limit', 10))

        db_name = 'course_db'

        queryset = CourseDB.objects.using(db_name).filter(
            Q(course_code__icontains=search) |
            Q(course_name__icontains=search)
        )

        if school_id:
            # Filter by school if provided
            from .models_course_db import SchoolCourse
            course_ids = SchoolCourse.objects.using(db_name).filter(
                school_id=school_id
            ).values_list('course_id', flat=True)
            queryset = queryset.filter(id__in=course_ids)

        queryset = queryset[:limit]
        serializer = CourseDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class MajorSearchView(APIView):
    """
    Search majors.

    GET /backend/api/major/?search=<query>&limit=<n>
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 444-460
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        search = request.query_params.get('search', '')
        limit = int(request.query_params.get('limit', 10))

        db_name = 'course_db'

        queryset = Major.objects.using(db_name).filter(
            major_name__icontains=search
        )[:limit]

        serializer = MajorSerializer(queryset, many=True)
        return Response(serializer.data)


class AcademicYearListView(APIView):
    """
    List all academic years.

    GET /backend/api/academic-years/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 462-474
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        db_name = 'course_db'
        queryset = AcademicYear.objects.using(db_name).all()
        serializer = AcademicYearSerializer(queryset, many=True)
        return Response(serializer.data)


class AcademicSemesterListView(APIView):
    """
    List all academic semesters.

    GET /backend/api/academic-semesters/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 476-486
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        db_name = 'course_db'
        queryset = AcademicSemester.objects.using(db_name).all()
        serializer = AcademicSemesterSerializer(queryset, many=True)
        return Response(serializer.data)


class SchoolListView(APIView):
    """
    List all schools with addresses.

    GET /backend/api/schools/
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 488-515
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        db_name = 'course_db'
        queryset = School.objects.using(db_name).prefetch_related(
            'schooladdress_set'
        ).all()
        serializer = SchoolWithAddressesSerializer(queryset, many=True)
        return Response(serializer.data)


class ConnectionRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing connection requests between students and counselors.

    Endpoints:
        POST   /backend/api/connection-requests/        - Create connection request
        GET    /backend/api/connection-requests/        - List connection requests (sent and received)
        GET    /backend/api/connection-requests/{id}/   - Get specific request
        PUT    /backend/api/connection-requests/{id}/   - Update status (ACCEPTED, REJECTED, CANCELLED)
        DELETE /backend/api/connection-requests/{id}/   - Delete connection request

    Status transitions:
        - PENDING → ACCEPTED (creates Room)
        - PENDING → REJECTED
        - PENDING → CANCELLED (by requesting user)
    """
    serializer_class = ConnectionRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        """
        Return connection requests where user is either requesting or requested user.

        Filters based on authenticated user and optimizes queries with select_related.
        """
        user = self.request.user
        return ConnectionRequest.objects.filter(
            models.Q(requesting_user=user) | models.Q(requested_user=user)
        ).select_related('requesting_user', 'requested_user', 'school', 'room')

    def update(self, request, *args, **kwargs):
        """
        Update connection request status.

        When status is changed to ACCEPTED, creates a Room for chat between
        student and counselor.

        Args:
            request: HTTP request with 'status' field

        Returns:
            Response with updated connection request data
        """
        instance = self.get_object()
        new_status = request.data.get('status')

        # Validate status transition
        if new_status not in [
            ConnectionRequest.ACCEPTED,
            ConnectionRequest.REJECTED,
            ConnectionRequest.CANCELLED
        ]:
            return Response(
                {'error': 'Invalid status. Must be ACCEPTED, REJECTED, or CANCELLED.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create room on acceptance
        if new_status == ConnectionRequest.ACCEPTED:
            # Check if room already exists
            if not instance.room:
                room = Room.objects.create(
                    student=instance.requesting_user,
                    counselor=instance.requested_user
                )
                instance.room = room

        # Update status and actioned_at timestamp
        instance.status = new_status
        instance.actioned_at = timezone.now()
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class RoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing chat rooms between students and counselors.

    Endpoints:
        GET    /backend/api/rooms/        - List all rooms for user
        POST   /backend/api/rooms/        - Create new room
        GET    /backend/api/rooms/{id}/   - Get room details with chat messages
        PUT    /backend/api/rooms/{id}/   - Update room
        DELETE /backend/api/rooms/{id}/   - Delete room

    Features:
        - Uses RoomSerializer for list/create (basic room info)
        - Uses RoomDetailSerializer for retrieve (includes chat messages)
        - Filters rooms to only show user's rooms (student or counselor)
        - Prefetches chat_messages for optimized detail view
    """
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.

        - retrieve: RoomDetailSerializer (includes chat messages)
        - others: RoomSerializer (basic room info)
        """
        if self.action == 'retrieve':
            return RoomDetailSerializer
        return RoomSerializer

    def get_queryset(self):
        """
        Return rooms where user is either student or counselor.

        Optimizes queries with:
        - select_related: Fetch student and counselor in same query
        - prefetch_related: Fetch chat_messages efficiently
        """
        user = self.request.user
        return Room.objects.filter(
            models.Q(student=user) | models.Q(counselor=user)
        ).select_related('student', 'counselor').prefetch_related('chat_messages')

    def create(self, request, *args, **kwargs):
        """
        Create a new room between student and counselor.

        Request body:
            {
                "student": integer (user ID),
                "counselor": integer (user ID)
            }

        Returns:
            RoomSerializer with created room data
        """
        student_id = request.data.get('student')
        counselor_id = request.data.get('counselor')

        # Validate that both IDs are provided
        if not student_id or not counselor_id:
            return Response(
                {'error': 'Both student and counselor IDs are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create room
        room = Room.objects.create(
            student_id=student_id,
            counselor_id=counselor_id
        )

        serializer = RoomSerializer(room)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class FileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing file uploads.

    Endpoints:
        GET    /backend/api/files/        - List all files uploaded by user
        POST   /backend/api/files/        - Upload new file
        GET    /backend/api/files/{id}/   - Get file details
        DELETE /backend/api/files/{id}/   - Delete file

    Features:
        - Uses FileUploadSerializer for create (handles multipart/form-data)
        - Uses FileSerializer for retrieve/list (includes uploader info)
        - Filters files to only show user's uploaded files
        - Supports file upload via multipart/form-data
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.

        - create: FileUploadSerializer (for file uploads)
        - others: FileSerializer (includes uploader details)
        """
        if self.action == 'create':
            return FileUploadSerializer
        return FileSerializer

    def get_queryset(self):
        """
        Return files uploaded by the authenticated user.

        Optimizes queries with select_related to fetch uploader info.
        """
        return File.objects.filter(
            uploaded_by=self.request.user
        ).select_related('uploaded_by')

    def create(self, request, *args, **kwargs):
        """
        Handle file upload.

        Request body (multipart/form-data):
            {
                "name": "string",
                "file_path": "file"
            }

        Returns:
            FileUploadSerializer with uploaded file data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Return full file info using FileSerializer
        file_instance = serializer.instance
        return Response(
            FileSerializer(file_instance).data,
            status=status.HTTP_201_CREATED
        )


class MeetingScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing meeting schedules.

    Endpoints:
        GET    /backend/api/meeting-schedules/        - List all meetings for user
        POST   /backend/api/meeting-schedules/        - Create new meeting
        GET    /backend/api/meeting-schedules/{id}/   - Get meeting details
        PUT    /backend/api/meeting-schedules/{id}/   - Update meeting
        DELETE /backend/api/meeting-schedules/{id}/   - Delete meeting

    Features:
        - Filters meetings to only show user's meetings (student or counselor)
        - Auto-sets created_by from authenticated user
        - Optimized queries with select_related
    """
    serializer_class = MeetingScheduleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        """
        Return meetings where user is either student or counselor in the room.

        Optimizes queries with select_related to fetch room and creator info.
        """
        user = self.request.user
        return MeetingSchedule.objects.filter(
            models.Q(room__student=user) | models.Q(room__counselor=user)
        ).select_related('room', 'created_by')


class CounselorAssignedCollegeView(APIView):
    """
    View for retrieving counselor's assigned colleges.

    GET /backend/api/counselor-assigned-college/

    Returns active college assignments for the authenticated counselor.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        """
        Get counselor's assigned colleges.

        Returns:
            List of CounselorAssignedCollegeSerializer with nested school details
        """
        assignments = CounselorAssignedCollege.objects.filter(
            user=request.user,
            is_active=True
        ).select_related('school')

        return Response(
            CounselorAssignedCollegeSerializer(assignments, many=True).data
        )


class SchoolCounselorView(APIView):
    """
    Get all counselors for a specific school.

    GET /backend/api/school-counselor/{school_id}/

    Returns counselors assigned to the school with connection request status.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, school_id):
        """
        Get counselors for a school.

        Args:
            school_id: ID of the school

        Returns:
            List of counselors with nested school data and connection request status
        """
        # Get counselors assigned to this school
        assignments = CounselorAssignedCollege.objects.filter(
            school_id=school_id,
            is_active=True
        ).select_related('user', 'school')

        # Check for existing connection requests from current user
        user = request.user
        existing_requests = ConnectionRequest.objects.filter(
            requesting_user=user,
            school_id=school_id
        ).values('requested_user_id', 'status', 'id')

        request_map = {r['requested_user_id']: r for r in existing_requests}

        result = []
        for assignment in assignments:
            counselor_data = {
                'id': assignment.id,
                'user': assignment.user.id,
                'school': SchoolSerializer(assignment.school).data,
                'counselor': {
                    'id': assignment.user.id,
                    'username': assignment.user.username
                },
                'connection_request': request_map.get(assignment.user.id)
            }
            result.append(counselor_data)

        return Response(result)


class LoginWithOTPView(APIView):
    """
    Send OTP to user's email for passwordless authentication.

    POST /backend/api/login-with-otp/

    Generates a 6-digit OTP and stores it in cache for 10 minutes.
    """
    permission_classes = []  # Public endpoint

    def post(self, request):
        """
        Generate and send OTP to user's email.

        Request body:
            {
                "email": "user@example.com"
            }

        Returns:
            Success message with email confirmation
        """
        from django.contrib.auth import get_user_model
        from django.core.cache import cache
        import random
        import string

        User = get_user_model()

        email = request.data.get('email')

        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))

        # Store in cache with 10 minute expiry
        cache.set(f'otp_{email}', otp, 600)

        # TODO: Send OTP via email
        # from django.core.mail import send_mail
        # send_mail(
        #     'Your OTP Code',
        #     f'Your OTP code is: {otp}',
        #     'noreply@gluide.com',
        #     [email],
        #     fail_silently=False,
        # )

        return Response({
            'message': 'OTP sent to your email',
            'email': email
        })


class ValidateOTPView(APIView):
    """
    Validate OTP and return JWT authentication tokens.

    POST /backend/api/validate-otp/

    Verifies the OTP code and returns access/refresh tokens on success.
    """
    permission_classes = []  # Public endpoint

    def post(self, request):
        """
        Validate OTP and return authentication tokens.

        Request body:
            {
                "email": "user@example.com",
                "otp": "123456"
            }

        Returns:
            JWT access and refresh tokens with user info
        """
        from django.contrib.auth import get_user_model
        from django.core.cache import cache
        from rest_framework_simplejwt.tokens import RefreshToken

        User = get_user_model()

        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response(
                {'error': 'Email and OTP are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify OTP
        stored_otp = cache.get(f'otp_{email}')

        if not stored_otp or stored_otp != otp:
            return Response(
                {'error': 'Invalid or expired OTP'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Clear OTP from cache
        cache.delete(f'otp_{email}')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        })
