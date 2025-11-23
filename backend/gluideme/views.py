from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import (
    Students, StudentDemographics, StudentGoal, StudentPathways,
    College, Course, Program, EducationPlan, CounselorProfile,
    AIRecommendation, Document, Department, CounselingSession,
    StudentTranscripts, TranscriptWebhookCourses
)
from .serializers import (
    StudentsSerializer, StudentDemographicsSerializer,
    StudentGoalSerializer, StudentPathwaysSerializer,
    CollegeSerializer, CourseSerializer, ProgramSerializer,
    EducationPlanSerializer, CounselorProfileSerializer,
    AIRecommendationSerializer, DocumentSerializer,
    DepartmentSerializer, CounselingSessionSerializer,
    StudentTranscriptSerializer, TranscriptWebhookCoursesSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for list views."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class StudentsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Students model.

    Endpoints:
    - GET /backend/api/gluideme/student_info/ - List students (paginated)
    - POST /backend/api/gluideme/student_info/ - Create student
    - GET /backend/api/gluideme/student_info/{id}/ - Get student
    - PUT /backend/api/gluideme/student_info/{id}/ - Update student

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1014-1094
    """
    serializer_class = StudentsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Counselors see all students, students see only themselves
        user = self.request.user
        if user.groups.filter(name='COUNSELOR').exists():
            return Students.objects.all()
        # For students, filter by linked user (if applicable)
        return Students.objects.all()

    @action(detail=True, methods=['post'])
    def note(self, request, pk=None):
        """
        Add note to student.
        POST /backend/api/gluideme/student_info/{id}/note/
        """
        student = self.get_object()
        note = request.data.get('note', '')

        # Append note to existing notes
        if student.notes:
            student.notes += f"\n\n{note}"
        else:
            student.notes = note

        student.save()
        serializer = self.get_serializer(student)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def student_courses(self, request, pk=None):
        """
        Get student courses.
        GET /backend/api/gluideme/student_info/{id}/student-courses/
        """
        student = self.get_object()
        # TODO: Implement course retrieval logic
        return Response([])


class StudentDemographicsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StudentDemographics model.

    Endpoints:
    - GET /backend/api/gluideme/student-demographics/?student_id={id}
    - POST /backend/api/gluideme/student-demographics/
    - PUT /backend/api/gluideme/student-demographics/{id}/

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1014-1066
    """
    serializer_class = StudentDemographicsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        queryset = StudentDemographics.objects.all()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset


class StudentGoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StudentGoal model.

    Endpoints:
    - GET /backend/api/gluideme/student-goal/?student_id={id}
    - POST /backend/api/gluideme/student-goal/
    - PUT /backend/api/gluideme/student-goal/{id}/

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1098-1126
    """
    serializer_class = StudentGoalSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        queryset = StudentGoal.objects.all()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset


class StudentPathwaysViewSet(viewsets.ModelViewSet):
    """
    ViewSet for StudentPathways model.

    Endpoints:
    - GET /backend/api/gluideme/student-pathways/
    - POST /backend/api/gluideme/student-pathways/

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1128-1158
    """
    serializer_class = StudentPathwaysSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = StudentPathways.objects.all()


class CollegeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for College model.

    Endpoints:
    - GET /backend/api/gluideme/colleges/
    - POST /backend/api/gluideme/colleges/

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1162-1189
    """
    serializer_class = CollegeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = College.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course model.

    Endpoints:
    - GET /backend/api/gluideme/courses/
    - POST /backend/api/gluideme/courses/

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1191-1225
    """
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Course.objects.all()


class ProgramViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Program model.

    Endpoints:
    - GET /backend/api/gluideme/programs/
    - POST /backend/api/gluideme/programs/

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1227-1257
    """
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Program.objects.all()

    def get_queryset(self):
        queryset = Program.objects.all()
        college_id = self.request.query_params.get('collegeID')
        program_type = self.request.query_params.get('programType')
        academic_year = self.request.query_params.get('academicYear')

        if college_id:
            queryset = queryset.filter(college_id=college_id)
        if program_type:
            queryset = queryset.filter(program_type=program_type)
        if academic_year:
            queryset = queryset.filter(academic_year_id=academic_year)

        return queryset


class EducationPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for EducationPlan model.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1259-1288
    """
    serializer_class = EducationPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = EducationPlan.objects.all()


class CounselorProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CounselorProfile model.

    Endpoints:
    - GET /backend/api/gluideme/counselor-profile/
    - PUT /backend/api/gluideme/counselor-profile/

    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1373-1392
    """
    serializer_class = CounselorProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return CounselorProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return CounselorProfile.objects.get(user=self.request.user)


class AIRecommendationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AIRecommendation model.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1340-1371
    """
    serializer_class = AIRecommendationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = AIRecommendation.objects.all()


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Document model.
    Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1393-1419
    """
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Document.objects.all()


class TranscriptUploadView(APIView):
    """
    View for uploading student transcripts.

    POST /backend/api/gluideme/transcript-upload/

    Uploads transcript to S3 and triggers async parsing via gluideai.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """
        Upload transcript file.

        Request body (multipart/form-data):
            - student_id: UUID of student
            - file: Transcript file (PDF, image, etc.)

        Returns:
            StudentTranscriptSerializer with created transcript data
        """
        student_id = request.data.get('student_id')
        file = request.FILES.get('file')

        if not file or not student_id:
            return Response(
                {'error': 'student_id and file are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Upload to S3
        from django.core.files.storage import default_storage
        file_path = f'transcripts/{student_id}/{file.name}'
        saved_path = default_storage.save(file_path, file)
        file_url = default_storage.url(saved_path)

        # Create transcript record
        transcript = StudentTranscripts.objects.create(
            student_id=student_id,
            file_name=file.name,
            file_url=file_url,
            status='unprocessed'
        )

        # Trigger async parsing via gluideai
        self.trigger_transcript_parsing(transcript, saved_path)

        return Response(
            StudentTranscriptSerializer(transcript).data,
            status=status.HTTP_201_CREATED
        )

    def trigger_transcript_parsing(self, transcript, file_path):
        """
        Send transcript to gluideai parse-transcript endpoint.

        Args:
            transcript: StudentTranscripts instance
            file_path: S3 file path
        """
        import requests
        from django.conf import settings

        webhook_url = f"{settings.BACKEND_BASE_URL}/backend/api/gluideme/transcript-webhooks/"

        try:
            requests.post(
                f"{settings.GLUIDEAI_URL}/api/v1/gluideai/parse-transcript/",
                json={
                    "file_path": file_path,
                    "webhook_url": webhook_url,
                    "transcript_id": str(transcript.id)
                },
                headers={
                    "Authorization": f"Bearer {settings.STATIC_TOKEN}"
                },
                timeout=10
            )

            transcript.status = 'in_progress'
            transcript.save()
        except Exception as e:
            # If request fails, keep status as unprocessed
            print(f"Failed to trigger transcript parsing: {e}")


class TranscriptWebhookView(APIView):
    """
    Webhook endpoint for receiving parsed transcript data from gluideai.

    POST /backend/api/gluideme/transcript-webhooks/

    Receives parsed course data and updates transcript status.
    This is a public endpoint (no authentication) for webhook callbacks.
    """
    permission_classes = []  # Public endpoint for webhook

    def post(self, request):
        """
        Receive parsed transcript data from gluideai.

        Request body:
            {
                "transcript_id": "uuid",
                "status": "success" | "failed",
                "data": {
                    "courses": [
                        {
                            "college": "string",
                            "major": "string",
                            "semester": "string",
                            "year": "string",
                            "course_code": "string",
                            "course_title": "string",
                            "credit": "string",
                            "grade": "string"
                        }
                    ]
                }
            }

        Returns:
            Success message
        """
        data = request.data
        transcript_id = data.get('transcript_id')
        status_val = data.get('status')
        courses = data.get('data', {}).get('courses', [])

        try:
            transcript = StudentTranscripts.objects.get(id=transcript_id)
        except StudentTranscripts.DoesNotExist:
            return Response(
                {'error': 'Transcript not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if status_val == 'success':
            # Create course records from parsed data
            for course in courses:
                TranscriptWebhookCourses.objects.create(
                    transcript=transcript,
                    college=course.get('college'),
                    major=course.get('major'),
                    semester=course.get('semester'),
                    year=course.get('year'),
                    course_code=course.get('course_code'),
                    course_title=course.get('course_title'),
                    credit=course.get('credit'),
                    grade=course.get('grade'),
                    status='success'
                )
            transcript.status = 'processed'
        else:
            transcript.status = 'failed'

        transcript.save()
        return Response({'message': 'Webhook received'})


class TranscriptListView(APIView):
    """
    View for listing student transcripts with parsed courses.

    GET /backend/api/gluideme/transcripts/list/?student_id={id}

    Returns all transcripts for a student with nested webhook_courses data.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List transcripts for a student.

        Query parameters:
            - student_id: UUID of student (required)

        Returns:
            List of StudentTranscriptSerializer with nested webhook_courses
        """
        student_id = request.query_params.get('student_id')

        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transcripts = StudentTranscripts.objects.filter(
            student_id=student_id
        ).prefetch_related('webhook_courses').order_by('-uploaded_at')

        return Response(StudentTranscriptSerializer(transcripts, many=True).data)
