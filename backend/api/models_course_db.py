"""
Course database models for the Gluide application.
These models use the 'course_db' database for course catalog information.
"""

from django.db import models


class Course(models.Model):
    """Course catalog model from course database."""
    _database = 'course_db'

    course_code = models.CharField(max_length=50, unique=True, primary_key=True)
    course_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=20)
    prerequisites = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'courses'
        managed = False  # Existing database, don't create/modify table
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class CourseOffering(models.Model):
    """Course offering/section model."""
    _database = 'course_db'

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='offerings')
    section = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    instructor = models.CharField(max_length=200)
    capacity = models.IntegerField()
    enrolled = models.IntegerField(default=0)
    schedule = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'course_offerings'
        managed = False  # Existing database, don't create/modify table
        unique_together = ['course', 'section', 'semester', 'year']
        ordering = ['year', 'semester', 'course']

    def __str__(self):
        return f"{self.course.course_code} {self.section} - {self.semester} {self.year}"
