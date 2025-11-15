"""
Django management command to generate synthetic test fixtures for TEST mode.
Uses Faker and Factory Boy to create realistic test data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
import factory
from factory.django import DjangoModelFactory
import random
from decimal import Decimal
from datetime import timedelta

# Import models
from api.models import Student, Transcript, SavedCourse
from api.models_course_db import Course, CourseOffering
from gluideme.models import Counselor, CounselorStudentAssignment, GuidanceSession, Recommendation
from gluideai.models import ParsedTranscriptData, ParsedCourse, AIProcessingLog

fake = Faker()


# =============================================================================
# FACTORY CLASSES
# =============================================================================

class UserFactory(DjangoModelFactory):
    """Factory for creating User instances."""
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f"user{n:04d}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
    is_superuser = False


class StudentFactory(DjangoModelFactory):
    """Factory for creating Student instances."""
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    student_id = factory.Sequence(lambda n: f"STU{n:06d}")
    grade_level = factory.LazyFunction(lambda: random.randint(9, 12))
    school = factory.Iterator([
        'Lincoln High School',
        'Washington High School',
        'Jefferson High School',
        'Roosevelt High School',
        'Kennedy High School'
    ])


class TranscriptFactory(DjangoModelFactory):
    """Factory for creating Transcript instances."""
    class Meta:
        model = Transcript

    student = factory.SubFactory(StudentFactory)
    file_name = factory.LazyAttribute(lambda obj: f"{obj.student.student_id}_transcript.pdf")
    file_url = factory.LazyAttribute(lambda obj: f"https://storage.example.com/transcripts/{obj.file_name}")
    processing_status = factory.Iterator(['pending', 'processing', 'completed', 'failed'])
    parsed_data = factory.LazyFunction(lambda: {
        'courses': [],
        'gpa': str(round(random.uniform(2.0, 4.0), 2)),
        'total_credits': random.randint(20, 50)
    })


class SavedCourseFactory(DjangoModelFactory):
    """Factory for creating SavedCourse instances."""
    class Meta:
        model = SavedCourse

    student = factory.SubFactory(StudentFactory)
    course_code = factory.Sequence(lambda n: f"MATH{100 + n}")
    course_name = factory.LazyAttribute(lambda obj: f"{obj.course_code} - {fake.catch_phrase()}")


class CourseFactory(DjangoModelFactory):
    """Factory for creating Course instances (course_db)."""
    class Meta:
        model = Course
        django_get_or_create = ('course_code',)

    course_code = factory.Sequence(lambda n: f"CS{100 + n}")
    course_name = factory.Faker('catch_phrase')
    description = factory.Faker('paragraph')
    credits = factory.LazyFunction(lambda: Decimal(str(random.choice([1.0, 3.0, 4.0, 5.0]))))
    department = factory.Iterator(['Computer Science', 'Mathematics', 'English', 'History', 'Biology'])
    level = factory.Iterator(['Introductory', 'Intermediate', 'Advanced', 'Graduate'])
    prerequisites = factory.LazyFunction(lambda: [])


class CourseOfferingFactory(DjangoModelFactory):
    """Factory for creating CourseOffering instances (course_db)."""
    class Meta:
        model = CourseOffering

    course = factory.SubFactory(CourseFactory)
    section = factory.Sequence(lambda n: f"00{n % 10 + 1}")
    semester = factory.Iterator(['Fall', 'Spring', 'Summer'])
    year = factory.LazyFunction(lambda: timezone.now().year)
    instructor = factory.Faker('name')
    capacity = factory.LazyFunction(lambda: random.randint(20, 50))
    enrolled = factory.LazyAttribute(lambda obj: random.randint(0, obj.capacity))
    schedule = factory.LazyFunction(lambda: {
        'days': random.choice(['MWF', 'TTh', 'MW', 'TThF']),
        'time': random.choice(['09:00-10:00', '10:00-11:00', '13:00-14:00', '14:00-15:00']),
        'room': f"Building {random.choice(['A', 'B', 'C'])}-{random.randint(100, 400)}"
    })


class CounselorFactory(DjangoModelFactory):
    """Factory for creating Counselor instances."""
    class Meta:
        model = Counselor

    user = factory.SubFactory(UserFactory)
    counselor_id = factory.Sequence(lambda n: f"COUN{n:04d}")
    school = factory.Iterator([
        'Lincoln High School',
        'Washington High School',
        'Jefferson High School',
        'Roosevelt High School',
        'Kennedy High School'
    ])
    specialization = factory.Iterator([
        'Academic Planning',
        'Career Counseling',
        'College Admissions',
        'Special Education',
        'Mental Health'
    ])


class CounselorStudentAssignmentFactory(DjangoModelFactory):
    """Factory for creating CounselorStudentAssignment instances."""
    class Meta:
        model = CounselorStudentAssignment

    counselor = factory.SubFactory(CounselorFactory)
    student = factory.SubFactory(StudentFactory)
    is_active = True


class GuidanceSessionFactory(DjangoModelFactory):
    """Factory for creating GuidanceSession instances."""
    class Meta:
        model = GuidanceSession

    counselor = factory.SubFactory(CounselorFactory)
    student = factory.SubFactory(StudentFactory)
    session_date = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=random.randint(-30, 30))
    )
    duration_minutes = factory.Iterator([30, 45, 60])
    session_type = factory.Iterator(['academic', 'career', 'college', 'personal'])
    notes = factory.Faker('paragraph')
    follow_up_required = factory.LazyFunction(lambda: random.choice([True, False]))


class RecommendationFactory(DjangoModelFactory):
    """Factory for creating Recommendation instances."""
    class Meta:
        model = Recommendation

    counselor = factory.SubFactory(CounselorFactory)
    student = factory.SubFactory(StudentFactory)
    recommendation_type = factory.Iterator(['course', 'program', 'activity'])
    title = factory.Faker('catch_phrase')
    description = factory.Faker('paragraph')
    priority = factory.Iterator(['high', 'medium', 'low'])
    status = factory.Iterator(['pending', 'accepted', 'declined', 'completed'])


class ParsedTranscriptDataFactory(DjangoModelFactory):
    """Factory for creating ParsedTranscriptData instances."""
    class Meta:
        model = ParsedTranscriptData

    transcript = factory.SubFactory(TranscriptFactory)
    student_name = factory.LazyAttribute(lambda obj: f"{obj.transcript.student.user.first_name} {obj.transcript.student.user.last_name}")
    student_id = factory.LazyAttribute(lambda obj: obj.transcript.student.student_id)
    school_name = factory.LazyAttribute(lambda obj: obj.transcript.student.school)
    graduation_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=random.randint(0, 365)))
    gpa = factory.LazyFunction(lambda: Decimal(str(round(random.uniform(2.0, 4.0), 2))))
    total_credits = factory.LazyFunction(lambda: Decimal(str(random.randint(20, 50))))
    courses_data = factory.LazyFunction(lambda: [])


class ParsedCourseFactory(DjangoModelFactory):
    """Factory for creating ParsedCourse instances."""
    class Meta:
        model = ParsedCourse

    parsed_transcript = factory.SubFactory(ParsedTranscriptDataFactory)
    course_code = factory.Sequence(lambda n: f"COURSE{n:03d}")
    course_name = factory.Faker('catch_phrase')
    semester = factory.Iterator(['Fall', 'Spring'])
    year = factory.LazyFunction(lambda: random.randint(2020, 2024))
    grade = factory.Iterator(['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'])
    credits = factory.LazyFunction(lambda: Decimal(str(random.choice([3.0, 4.0, 5.0]))))


class AIProcessingLogFactory(DjangoModelFactory):
    """Factory for creating AIProcessingLog instances."""
    class Meta:
        model = AIProcessingLog

    transcript = factory.SubFactory(TranscriptFactory)
    processing_type = factory.Iterator(['extraction', 'validation', 'enhancement'])
    status = factory.Iterator(['started', 'completed', 'failed'])
    model_used = factory.Iterator(['gpt-4', 'gpt-3.5-turbo', 'claude-3'])
    tokens_used = factory.LazyFunction(lambda: random.randint(100, 5000))
    processing_time_seconds = factory.LazyFunction(lambda: Decimal(str(round(random.uniform(0.5, 10.0), 2))))
    error_message = factory.LazyAttribute(lambda obj: '' if obj.status == 'completed' else 'Processing error occurred')
    result_data = factory.LazyFunction(lambda: {'success': True, 'fields_extracted': random.randint(5, 15)})


# =============================================================================
# MANAGEMENT COMMAND
# =============================================================================

class Command(BaseCommand):
    help = 'Generate synthetic test fixtures for TEST mode'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=20,
            help='Number of users to create (default: 20)'
        )
        parser.add_argument(
            '--students',
            type=int,
            default=15,
            help='Number of students to create (default: 15)'
        )
        parser.add_argument(
            '--counselors',
            type=int,
            default=3,
            help='Number of counselors to create (default: 3)'
        )
        parser.add_argument(
            '--courses',
            type=int,
            default=50,
            help='Number of courses to create (default: 50)'
        )

    def handle(self, *args, **options):
        from django.conf import settings

        # Check if running in TEST mode
        if not getattr(settings, 'USE_TEST_MODE', False):
            self.stdout.write(self.style.ERROR(
                '❌ This command should ONLY be run in TEST mode!\n'
                'Set DJANGO_SETTINGS_MODULE=config.settings_test'
            ))
            return

        self.stdout.write(self.style.SUCCESS('🧪 Running in TEST MODE'))
        self.stdout.write('Generating synthetic test fixtures...\n')

        # Get counts from options
        num_users = options['users']
        num_students = options['students']
        num_counselors = options['counselors']
        num_courses = options['courses']

        # Create superuser
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(f'  ✓ Created superuser: admin (password: admin123)')

        # Create counselors
        counselors = []
        for i in range(num_counselors):
            counselor = CounselorFactory()
            counselors.append(counselor)
        self.stdout.write(f'  ✓ Created {len(counselors)} counselors')

        # Create students
        students = []
        for i in range(num_students):
            student = StudentFactory()
            students.append(student)
        self.stdout.write(f'  ✓ Created {len(students)} students')

        # Assign students to counselors
        assignments = []
        for student in students:
            counselor = random.choice(counselors)
            assignment = CounselorStudentAssignmentFactory(
                counselor=counselor,
                student=student
            )
            assignments.append(assignment)
        self.stdout.write(f'  ✓ Created {len(assignments)} counselor-student assignments')

        # Create transcripts for each student
        transcripts = []
        for student in students:
            transcript = TranscriptFactory(student=student)
            transcripts.append(transcript)
        self.stdout.write(f'  ✓ Created {len(transcripts)} transcripts')

        # Create parsed transcript data for completed transcripts
        parsed_count = 0
        for transcript in transcripts:
            if transcript.processing_status == 'completed':
                parsed = ParsedTranscriptDataFactory(transcript=transcript)
                # Create some parsed courses
                for _ in range(random.randint(3, 8)):
                    ParsedCourseFactory(parsed_transcript=parsed)
                parsed_count += 1
        self.stdout.write(f'  ✓ Created {parsed_count} parsed transcript records')

        # Create AI processing logs
        log_count = 0
        for transcript in transcripts:
            for _ in range(random.randint(1, 3)):
                AIProcessingLogFactory(transcript=transcript)
                log_count += 1
        self.stdout.write(f'  ✓ Created {log_count} AI processing logs')

        # Create courses (in course_db)
        courses = []
        for i in range(num_courses):
            course = CourseFactory()
            courses.append(course)
        self.stdout.write(f'  ✓ Created {len(courses)} courses')

        # Create course offerings
        offering_count = 0
        for course in courses:
            for _ in range(random.randint(1, 3)):
                CourseOfferingFactory(course=course)
                offering_count += 1
        self.stdout.write(f'  ✓ Created {offering_count} course offerings')

        # Create saved courses
        saved_count = 0
        for student in students:
            for _ in range(random.randint(2, 6)):
                course = random.choice(courses)
                SavedCourseFactory(
                    student=student,
                    course_code=course.course_code,
                    course_name=course.course_name
                )
                saved_count += 1
        self.stdout.write(f'  ✓ Created {saved_count} saved courses')

        # Create guidance sessions
        session_count = 0
        for assignment in assignments:
            for _ in range(random.randint(1, 5)):
                GuidanceSessionFactory(
                    counselor=assignment.counselor,
                    student=assignment.student
                )
                session_count += 1
        self.stdout.write(f'  ✓ Created {session_count} guidance sessions')

        # Create recommendations
        rec_count = 0
        for assignment in assignments:
            for _ in range(random.randint(2, 5)):
                RecommendationFactory(
                    counselor=assignment.counselor,
                    student=assignment.student
                )
                rec_count += 1
        self.stdout.write(f'  ✓ Created {rec_count} recommendations')

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('✅ Test fixtures generated successfully!\n'))
        self.stdout.write('Summary:')
        self.stdout.write(f'  • {num_counselors} counselors')
        self.stdout.write(f'  • {num_students} students')
        self.stdout.write(f'  • {len(assignments)} assignments')
        self.stdout.write(f'  • {len(transcripts)} transcripts')
        self.stdout.write(f'  • {parsed_count} parsed transcripts')
        self.stdout.write(f'  • {log_count} AI processing logs')
        self.stdout.write(f'  • {len(courses)} courses')
        self.stdout.write(f'  • {offering_count} course offerings')
        self.stdout.write(f'  • {saved_count} saved courses')
        self.stdout.write(f'  • {session_count} guidance sessions')
        self.stdout.write(f'  • {rec_count} recommendations')
        self.stdout.write('='*60)
        self.stdout.write('\nLogin credentials:')
        self.stdout.write(f'  Username: admin')
        self.stdout.write(f'  Password: admin123')
