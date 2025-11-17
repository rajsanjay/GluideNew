"""
Pydantic models for transcript parser.
These models validate and structure data from LLM transcript parsing.
Reference: REWRITE_SPECIFICATION.md lines 272-363
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class Course(BaseModel):
    """
    Single course from transcript.
    CRITICAL: Field names must match EXACTLY as they appear in webhook payload.
    Reference: REWRITE_SPECIFICATION.md lines 241-262
    """
    college: str = Field(description="Name of the college/university")
    major: Optional[str] = Field(None, description="Student's major if mentioned")
    semester: str = Field(description="Semester (e.g., Fall, Spring, Summer)")
    year: str = Field(description="Year (e.g., 2023, 2024)")
    course_code: str = Field(description="Course code (e.g., CS 61A, MATH 54)")
    course_title: str = Field(description="Full course title")
    credit: str = Field(description="Credit units as string (e.g., '4.00', '3.00')")
    grade: str = Field(description="Letter grade (e.g., A, B+, C)")

    class Config:
        # Ensure exact field names in JSON output
        populate_by_name = True


class Transcript(BaseModel):
    """
    Complete transcript containing all courses.
    CRITICAL: This is the top-level structure returned by LLM.
    Reference: REWRITE_SPECIFICATION.md lines 264-270
    """
    courses: List[Course] = Field(
        description="List of all courses extracted from transcript"
    )

    @field_validator('courses')
    @classmethod
    def validate_courses(cls, v):
        if not v:
            raise ValueError("Transcript must contain at least one course")
        return v
