/**
 * API endpoint constants and configuration.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Main API endpoints
  students: `${API_BASE_URL}/api/students/`,
  transcripts: `${API_BASE_URL}/api/transcripts/`,
  savedCourses: `${API_BASE_URL}/api/saved-courses/`,
  courses: `${API_BASE_URL}/api/courses/`,
  courseOfferings: `${API_BASE_URL}/api/course-offerings/`,

  // GluideMe (Counselor) endpoints
  counselors: `${API_BASE_URL}/api/gluideme/counselors/`,
  assignments: `${API_BASE_URL}/api/gluideme/assignments/`,
  sessions: `${API_BASE_URL}/api/gluideme/sessions/`,
  recommendations: `${API_BASE_URL}/api/gluideme/recommendations/`,

  // GluideAI (AI Processing) endpoints
  parsedTranscripts: `${API_BASE_URL}/api/gluideai/parsed-transcripts/`,
  parsedCourses: `${API_BASE_URL}/api/gluideai/parsed-courses/`,
  processingLogs: `${API_BASE_URL}/api/gluideai/processing-logs/`,
  triggerProcessing: `${API_BASE_URL}/api/gluideai/processing-logs/trigger_processing/`,
} as const;

export const API_CONFIG = {
  baseUrl: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
} as const;

export const USE_TEST_MODE = process.env.NEXT_PUBLIC_USE_TEST_MODE === 'true';
