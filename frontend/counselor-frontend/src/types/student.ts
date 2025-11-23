/**
 * Student Type Definitions
 * These types MUST match the backend API responses exactly.
 * DO NOT MODIFY without updating the Django serializers.
 */

export interface StudentsList {
  id: string;
  full_name: string;
  first_name: string;
  last_name: string;
  student_id: string;
  email: string;
  phone: string;
  enrollment_status: string;
  program: string;
  major: string;
  gpa: string;
  academic_standing: string;
  stage: string;
  pathway: string;
  advisor: string;
  target_graduation: string;
  transfer_target: string;
  skills: string[];
  goals: string[];
  last_contact: string;
  next_followup: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface StudentsInfo {
  id: string;
  full_name: string;
  first_name: string;
  last_name: string;
  student_id: string;
  email: string;
  phone: string;
  enrollment_status: string;
  program: string;
  major: string;
  gpa: string;
  academic_standing: string;
  stage: string;
  pathway: string;
  advisor: string;
  target_graduation: string;
  transfer_target: string;
  skills: string[];
  goals: string[];
  last_contact: string;
  next_followup: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface StudentDemographicInfo {
  id: string;
  student: string;
  pers_info_age: number | null;
  pers_info_primary_language_spoken_at_home: string | null;
  pers_info_other_language_spoken_at_home: string | null;
  edu_back_first_in_family_to_attent_college: string | null;
  edu_back_parent_education: string | null;
  edu_back_have_attended_college_fefore: string | null;
  fin_info_eligible_for_pell_grant: string | null;
  fin_info_expected_primary_funding_source: string | null;
  fin_info_other_funding_source: string | null;
  life_employment_status: string | null;
  life_have_dependents: string | null;
  life_current_living_situation: string | null;
  geo_how_travel_distance_willing_for_classes: string | null;
  geo_primary_transport: string | null;
  sched_units_per_semester: string | null;
  sched_class_schedule_best_fits: string[];
  support_services_helpful: string[];
  back_ethnic_background: string | null;
  back_other_ethnic: string | null;
  back_veteran_status: string | null;
  back_disability_status: string | null;
  goals_primary_goal_to_attend_college: string | null;
  goals_other: string | null;
  goals_timeline_to_complete_goal: string | null;
  created_at: string;
}

export interface StudentGoalInfo {
  goal_id: string;
  student: string;
  goal_type: 'academic' | 'career' | 'transfer' | 'personal';
  goal_description: string;
  target_date: string | null;
  priority: 'high' | 'medium' | 'low';
  status: 'active' | 'completed' | 'deferred' | 'cancelled';
  progress_notes: string;
}

export interface StudentPathwayInfo {
  pathway_id: string;
  student: string;
  education_plan: string | null;
  pathway_type: 'associate_certificate' | 'transfer' | 'continuing_education';
  pathway_name: string;
  interest_level: 'high' | 'medium' | 'low';
  priority: number | null;
  target_institutions: string[];
  target_start_date: string | null;
  notes: string;
}

export interface StudentTargetInfo {
  id: string;
  student: string;
  college_name: string;
  program_name: string;
  priority: number | null;
  target_graduation: string | null;
  application_status: string;
  application_date: string | null;
  decision_date: string | null;
  minimum_gpa_required: string | null;
  current_gpa_gap: string | null;
  additional_requirements: string;
  notes: string;
  is_active: boolean;
  target_college: string | null;
  target_program: string | null;
}

export interface StudentCourse {
  id: string;
  course_code: string;
  course_name: string;
  institution: string;
  grade: string;
  status: string;
  semester: string | number | null;
  year: number;
  credits: string;
  verified_by_counselor: boolean;
  source: string;
  ai_extracted_transcript: TranscriptWebhookCourse | null;
}

export interface TranscriptWebhookCourse {
  id: string;
  college: string | null;
  major: string | null;
  semester: string | null;
  year: string | null;
  course_code: string;
  course_title: string;
  credit: string | null;
  grade: string | null;
  status: string;
  received_at: string;
}

export interface StudentTranscript {
  id: string;
  student: string;
  file_name: string;
  file_url: string;
  uploaded_at: string;
  status: 'unprocessed' | 'in_progress' | 'processed' | 'failed';
}

export interface CounselingSession {
  session_id: string;
  student: string;
  counselor: number | null;
  session_date: string;
  session_type: string;
  session_notes: string;
  follow_up_required: boolean;
  follow_up_date: string | null;
  created_at: string;
}

export interface EducationPlan {
  plan_id: string;
  student: string;
  plan_name: string;
  plan_type: 'degree' | 'transfer' | 'certificate';
  status: 'draft' | 'active' | 'completed' | 'archived';
  target_completion: string | null;
  advisor: number;
  is_approved: boolean;
  approval_date: string | null;
  total_credits: string | null;
  notes: string;
}
