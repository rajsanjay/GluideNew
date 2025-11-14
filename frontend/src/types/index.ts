/**
 * TypeScript type definitions for the Gluide application.
 */

// Student types
export interface Student {
  id: number;
  username: string;
  email: string;
  student_id: string;
  grade_level: number;
  school: string;
  created_at: string;
  updated_at: string;
}

// Transcript types
export interface Transcript {
  id: number;
  student: number;
  student_name: string;
  file_name: string;
  file_url: string;
  upload_date: string;
  processing_status: 'pending' | 'processing' | 'completed' | 'failed';
  parsed_data: any;
  created_at: string;
  updated_at: string;
}

// Course types
export interface Course {
  course_code: string;
  course_name: string;
  description: string;
  credits: number;
  department: string;
  level: string;
  prerequisites: string[];
}

export interface CourseOffering {
  id: number;
  course: string;
  course_info: Course;
  section: string;
  semester: string;
  year: number;
  instructor: string;
  capacity: number;
  enrolled: number;
  schedule: any;
}

// Counselor types
export interface Counselor {
  id: number;
  username: string;
  email: string;
  counselor_id: string;
  school: string;
  specialization: string;
  created_at: string;
  updated_at: string;
}

export interface GuidanceSession {
  id: number;
  counselor: number;
  counselor_name: string;
  student: number;
  student_name: string;
  session_date: string;
  duration_minutes: number;
  session_type: 'academic' | 'career' | 'college' | 'personal';
  notes: string;
  follow_up_required: boolean;
  created_at: string;
  updated_at: string;
}

export interface Recommendation {
  id: number;
  counselor: number;
  counselor_name: string;
  student: number;
  student_name: string;
  recommendation_type: 'course' | 'program' | 'activity';
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  status: 'pending' | 'accepted' | 'declined' | 'completed';
  created_at: string;
  updated_at: string;
}

// AI Processing types
export interface ParsedTranscriptData {
  id: number;
  transcript: number;
  transcript_file_name: string;
  student_name: string;
  student_id: string;
  school_name: string;
  graduation_date: string | null;
  gpa: number | null;
  total_credits: number | null;
  courses_data: any[];
  courses: ParsedCourse[];
  created_at: string;
  updated_at: string;
}

export interface ParsedCourse {
  id: number;
  course_code: string;
  course_name: string;
  semester: string;
  year: number | null;
  grade: string;
  credits: number | null;
  created_at: string;
}

// API Response types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  detail?: string;
  [key: string]: any;
}
