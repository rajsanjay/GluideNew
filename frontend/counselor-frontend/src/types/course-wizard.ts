/**
 * Course Wizard Type Definitions
 * These types are used for the guided course selection wizard.
 */

import { Course, Program } from './college';

export interface WizardStep {
  step: number;
  title: string;
  description: string;
  is_complete: boolean;
  is_current: boolean;
  data: Record<string, any>;
}

export interface CourseSelectionCriteria {
  student_id: string;
  program_id?: string;
  semester_preference: ('Fall' | 'Spring' | 'Summer' | 'Winter')[];
  credits_per_semester: number;
  schedule_preference: 'morning' | 'afternoon' | 'evening' | 'online' | 'hybrid' | 'flexible';
  completed_courses: string[];
  required_courses: string[];
  elective_areas: string[];
  transfer_goal?: string;
  graduation_target?: string;
  work_schedule_constraints?: string;
  travel_constraints?: string;
}

export interface CourseRecommendation {
  course: Course;
  relevance_score: number;
  reason: string;
  semester_suggestion: string;
  prerequisites_status: {
    all_met: boolean;
    missing: string[];
  };
  fits_criteria: boolean;
  alternative_courses: string[];
}

export interface PathwayRecommendation {
  program: Program;
  match_score: number;
  match_reasons: string[];
  required_courses: Course[];
  estimated_completion: string;
  transfer_opportunities: string[];
  career_outcomes: string[];
}

export interface WizardSession {
  session_id: string;
  student_id: string;
  current_step: number;
  steps: WizardStep[];
  criteria: CourseSelectionCriteria;
  recommendations: CourseRecommendation[];
  pathway_recommendations: PathwayRecommendation[];
  selected_courses: string[];
  created_at: string;
  updated_at: string;
  status: 'in_progress' | 'completed' | 'abandoned';
}

export interface WizardProgress {
  total_steps: number;
  completed_steps: number;
  current_step: number;
  completion_percentage: number;
  estimated_time_remaining: string;
}
