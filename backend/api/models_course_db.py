"""
Course database models for the Gluide application.
These models use the 'course_db' database and have managed=False.
They represent EXISTING tables and migrations should NOT be run.
Reference: COMPREHENSIVE_DOCUMENTATION.md lines 1645-1884
"""

from django.db import models
from django.conf import settings


# Helper for geography fields - works in both test and database modes
def get_point_field(*args, **kwargs):
    """Returns PointField for PostGIS or CharField for test mode."""
    if getattr(settings, 'USE_TEST_MODE', False):
        # In test mode, store as text
        return models.CharField(max_length=100, *args, **kwargs)
    else:
        from django.contrib.gis.db import models as gis_models
        return gis_models.PointField(*args, **kwargs)


class School(models.Model):
    """School model - lines 1649-1658"""
    school_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    assist_university_id = models.BigIntegerField()
    is_community_college = models.BooleanField(default=False)
    alternate_names = models.JSONField(default=list)

    class Meta:
        managed = False
        db_table = 'school'

    def __str__(self):
        return self.name


class SchoolAddress(models.Model):
    """SchoolAddress model - lines 1660-1680"""
    address_id = models.BigAutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, db_column='school_id')
    address_type = models.CharField(max_length=50)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=5)
    zip = models.CharField(max_length=10)
    location = get_point_field(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField()
    last_updated_date = models.DateTimeField()
    created_by = models.CharField(max_length=50)
    last_updated_by = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'school_address'

    def __str__(self):
        return f"{self.school.name} - {self.city}"


class Major(models.Model):
    """Major model - lines 1682-1691"""
    id = models.BigAutoField(primary_key=True)
    major_name = models.CharField(max_length=255, unique=True)
    major_slug = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'majors'

    def __str__(self):
        return self.major_name


class Course(models.Model):
    """Course model - lines 1693-1703"""
    id = models.BigAutoField(primary_key=True)
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=255)
    credits = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'courses'

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class SchoolMajor(models.Model):
    """SchoolMajor model - lines 1705-1715"""
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, db_column='school_id')
    major = models.ForeignKey(Major, on_delete=models.DO_NOTHING, db_column='major_id')
    year = models.ForeignKey('AcademicYear', on_delete=models.DO_NOTHING, db_column='year_id')

    class Meta:
        managed = False
        db_table = 'school_majors'
        unique_together = ['school', 'major', 'year']

    def __str__(self):
        return f"{self.school.name} - {self.major.major_name}"


class SchoolCourse(models.Model):
    """SchoolCourse model - lines 1717-1728"""
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, db_column='school_id')
    major = models.ForeignKey(Major, on_delete=models.DO_NOTHING, db_column='major_id')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, db_column='course_id')
    year = models.ForeignKey('AcademicYear', on_delete=models.DO_NOTHING, db_column='year_id')

    class Meta:
        managed = False
        db_table = 'school_courses'
        unique_together = ['school', 'major', 'course', 'year']

    def __str__(self):
        return f"{self.school.name} - {self.course.course_code}"


class AcademicYear(models.Model):
    """AcademicYear model - lines 1730-1739"""
    id = models.BigAutoField(primary_key=True)
    year = models.CharField(max_length=50)
    assist_year_id = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'academic_years'

    def __str__(self):
        return self.year


class AcademicSemester(models.Model):
    """AcademicSemester model - lines 1741-1748"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'academic_semesters'

    def __str__(self):
        return self.name


class CourseSchedule(models.Model):
    """CourseSchedule model - lines 1750-1779"""
    collegename = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    courseid = models.CharField(max_length=100)
    classname = models.CharField(max_length=255)
    classid = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    mode = models.CharField(max_length=20)
    section = models.CharField(max_length=100)
    instructor = models.CharField(max_length=255)
    prereq = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    details = models.TextField(null=True, blank=True)
    days = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    units = models.CharField(max_length=100)
    term = models.CharField(max_length=100)
    coursetype = models.CharField(max_length=20)
    external_normalized_course_id = models.CharField(max_length=100, null=True, blank=True)
    academic_semester_id = models.IntegerField()
    academic_year_id = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, db_column='school_id')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, db_column='course_id')

    class Meta:
        managed = False
        db_table = 'course_schedule'

    def __str__(self):
        return f"{self.classname} - {self.term}"


class Program(models.Model):
    """Program model - lines 1781-1793"""
    program_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    target_school = models.ForeignKey(School, on_delete=models.DO_NOTHING, related_name='target_programs', db_column='target_school_id')
    source_school = models.ForeignKey(School, on_delete=models.DO_NOTHING, related_name='source_programs', db_column='source_school_id')
    major = models.ForeignKey(Major, on_delete=models.DO_NOTHING, db_column='major_id')
    title_slug = models.CharField(max_length=255)
    year = models.ForeignKey(AcademicYear, on_delete=models.DO_NOTHING, db_column='year_id')

    class Meta:
        managed = False
        db_table = 'program'

    def __str__(self):
        return self.title


class ProgramDetail(models.Model):
    """ProgramDetail model - lines 1795-1806"""
    DETAIL_TYPE_CHOICES = [
        ('GeneralTitle', 'General Title'),
        ('GeneralText', 'General Text'),
    ]
    AREA_CHOICES = [
        ('General', 'General'),
    ]

    program_detail_id = models.BigAutoField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING, db_column='program_id')
    detail_type = models.CharField(max_length=50, choices=DETAIL_TYPE_CHOICES)
    position = models.CharField(max_length=3)
    area = models.CharField(max_length=50, choices=AREA_CHOICES)
    detail_data = models.TextField()

    class Meta:
        managed = False
        db_table = 'program_detail'

    def __str__(self):
        return f"{self.program.title} - {self.detail_type}"


class Requirement(models.Model):
    """Requirement model - lines 1808-1822"""
    requirement_id = models.BigAutoField(primary_key=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING, db_column='program_id')
    requirement_title = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    position = models.CharField(max_length=3)
    section_conjunction = models.TextField()
    attributes = models.JSONField()
    instruction = models.JSONField()
    advisements = models.JSONField()

    class Meta:
        managed = False
        db_table = 'requirement'

    def __str__(self):
        return self.requirement_title


class RequirementSection(models.Model):
    """RequirementSection model - lines 1824-1849"""
    section_id = models.BigAutoField(primary_key=True)
    requirement = models.ForeignKey(Requirement, on_delete=models.DO_NOTHING, db_column='requirement_id')
    section_name = models.CharField(max_length=255)
    section_header = models.JSONField(null=True, blank=True)
    section_advisements = models.JSONField(null=True, blank=True)
    section_attributes = models.JSONField(null=True, blank=True)
    section_parsed_advisements = models.TextField()

    class Meta:
        managed = False
        db_table = 'requirement_section'

    def __str__(self):
        return self.section_name


class RequirementCourse(models.Model):
    """RequirementCourse model - lines 1851-1866"""
    course_id = models.BigAutoField(primary_key=True)
    section = models.ForeignKey(RequirementSection, on_delete=models.DO_NOTHING, db_column='section_id')
    course_code = models.CharField(max_length=50)
    course_name = models.CharField(max_length=255)
    credits = models.CharField(max_length=50)
    special_comments = models.JSONField(default=list)
    general_comment = models.JSONField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'requirement_course'

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Equivalency(models.Model):
    """Equivalency model - lines 1868-1878"""
    equivalence_id = models.BigAutoField(primary_key=True)
    from_course = models.ForeignKey(RequirementCourse, on_delete=models.DO_NOTHING, related_name='equivalencies_from', db_column='from_course_id')
    to_course = models.ForeignKey(RequirementCourse, on_delete=models.DO_NOTHING, related_name='equivalencies_to', db_column='to_course_id')

    class Meta:
        managed = False
        db_table = 'equivalency'

    def __str__(self):
        return f"{self.from_course.course_code} -> {self.to_course.course_code}"


class AdmissionRates(models.Model):
    """AdmissionRates model - lines 1880-1884"""
    school = models.ForeignKey(School, on_delete=models.DO_NOTHING, db_column='school_id')
    year = models.ForeignKey(AcademicYear, on_delete=models.DO_NOTHING, db_column='year_id')
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'admission_rates'

    def __str__(self):
        return f"{self.school.name} - {self.year.year}: {self.rate}%"
