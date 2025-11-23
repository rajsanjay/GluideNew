/**
 * Course Scheduler Type Definitions
 * These types are used for the course scheduling and planning features.
 */

import { Course } from './college';
import { StudentCourse } from './student';

export interface ScheduledCourse {
  id: string;
  course: Course;
  semester: 'Fall' | 'Spring' | 'Summer' | 'Winter';
  year: number;
  status: 'planned' | 'enrolled' | 'completed' | 'dropped';
  credits: number;
  priority: number;
  prerequisites_met: boolean;
  notes: string;
}

export interface Semester {
  id: string;
  name: string;
  term: 'Fall' | 'Spring' | 'Summer' | 'Winter';
  year: number;
  start_date: string;
  end_date: string;
  courses: ScheduledCourse[];
  total_credits: number;
  is_active: boolean;
}

export interface AcademicPlan {
  plan_id: string;
  student_id: string;
  plan_name: string;
  start_semester: string;
  end_semester: string;
  semesters: Semester[];
  total_credits_required: number;
  credits_completed: number;
  credits_remaining: number;
  projected_graduation: string;
  status: 'draft' | 'active' | 'completed';
  last_updated: string;
}

export interface CourseRequisite {
  course_code: string;
  course_name: string;
  type: 'prerequisite' | 'corequisite' | 'recommended';
  is_met: boolean;
}

export interface CourseAvailability {
  course_code: string;
  fall: boolean;
  spring: boolean;
  summer: boolean;
  winter: boolean;
  typical_capacity: number;
  enrollment_restrictions: string[];
}

export interface ScheduleConflict {
  type: 'prerequisite' | 'time_conflict' | 'capacity' | 'restriction';
  severity: 'error' | 'warning' | 'info';
  message: string;
  courses_affected: string[];
  suggested_resolution: string;
}

export interface ScheduleValidation {
  is_valid: boolean;
  conflicts: ScheduleConflict[];
  warnings: string[];
  suggestions: string[];
}

// Additional types for course scheduler store
export interface PlacedCourse {
  id: string;
  course_code: string;
  course_name: string;
  credits: number;
  department?: string;
  prerequisites?: string[];
  position?: { x: number; y: number };
}

export interface Term {
  id: number;
  courses: PlacedCourse[];
  from: string;
  to: string;
}

export interface Connection {
  id: string;
  from: string;
  to: string;
  type: 'prerequisite' | 'corequisite' | 'recommended';
}

export interface SearchFilters {
  query: string;
  department: string;
  credits: number | null;
  level?: string;
  availability?: string;
}
