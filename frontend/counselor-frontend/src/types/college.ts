/**
 * College, Course, Program, and Department Type Definitions
 * These types MUST match the backend API responses exactly.
 * DO NOT MODIFY without updating the Django serializers.
 */

export interface College {
  id: string;
  name: string;
  short_name: string;
  type: 'UC' | 'CSU' | 'Private' | 'Community';
  location: string;
  website: string;
  parent_college: string | null;
  course_db_school_id: number | null;
}

export interface Course {
  id: string;
  course_code: string;
  course_name: string;
  level: 'Junior' | 'Graduate';
  units: string;
  prerequisites: string[];
  is_transferrable: boolean;
  transfer_universities: string[];
  department: string;
  college: string;
}

export interface Department {
  department_id: string;
  department_name: string;
  college: string;
}

export interface Program {
  program_id: string;
  program_code: string;
  program_name: string;
  program_type: 'certificate' | 'associate' | 'bachelor' | 'master' | 'transfer' | 'major' | 'other';
  program_description: string;
  degree_url: string;
  college: string;
  department: string | null;
  total_credits_required: string | null;
  duration_years: string | null;
  year: string;
  is_active: boolean;
  course_db_program_id: number | null;
  academic_year_id: number | null;
}

export interface CounselorProfile {
  profile_id: string;
  user: number;
  full_name: string;
  email: string;
  employee_id: string;
  site_name: string;
  site_name_detail: string | null;
  phone: string;
  department: string;
  specialization: string;
  bio: string;
  is_active: boolean;
}

export interface AIRecommendation {
  recommendation_id: string;
  student: string;
  recommendation_type: 'course' | 'program' | 'pathway' | 'resource';
  recommendation_data: Record<string, any>;
  reason: string;
  confidence_score: string;
  is_accepted: boolean;
  is_dismissed: boolean;
  created_by_counselor: number | null;
  created_at: string;
}

export interface Document {
  document_id: string;
  student: string;
  document_type: string;
  document_name: string;
  file_url: string;
  uploaded_by: number | null;
  uploaded_at: string;
  notes: string;
}
