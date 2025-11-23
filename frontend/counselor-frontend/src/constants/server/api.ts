/**
 * API Constants for Gluide Backend
 * DO NOT CHANGE - These endpoints match the backend implementation
 */

export const BACKEND_BASE_URL = process.env.BACKEND_BASE_URL || "https://dev-api.gluide.me";
export const WEBSOCKET_URL = process.env.NEXT_PUBLIC_WEBSOCKET_URL || "wss://dev-api.gluide.me";

// ============================================================================
// Authentication Endpoints - Django Allauth (DO NOT CHANGE)
// ============================================================================
export const AUTH_LOGIN_URL = `${BACKEND_BASE_URL}/_allauth/browser/v1/auth/login`;
export const AUTH_REGISTER_URL = `${BACKEND_BASE_URL}/_allauth/browser/v1/auth/signup`;
export const AUTH_SESSION_URL = `${BACKEND_BASE_URL}/_allauth/browser/v1/auth/session`;
export const AUTH_PASSWORD_REQUEST_URL = `${BACKEND_BASE_URL}/_allauth/app/v1/auth/password/request`;
export const AUTH_PASSWORD_RESET_URL = `${BACKEND_BASE_URL}/_allauth/app/v1/auth/password/reset`;
export const AUTH_PASSWORD_CHANGE_URL = `${BACKEND_BASE_URL}/_allauth/browser/v1/account/password/change`;
export const AUTH_EMAIL_VERIFY_URL = `${BACKEND_BASE_URL}/_allauth/app/v1/auth/email/verify`;
export const AUTH_PROVIDER_TOKEN_URL = `${BACKEND_BASE_URL}/_allauth/browser/v1/auth/provider/token`;

// JWT Token Endpoints
export const JWT_TOKEN_OBTAIN_URL = `${BACKEND_BASE_URL}/backend/api/token/`;
export const JWT_TOKEN_REFRESH_URL = `${BACKEND_BASE_URL}/backend/api/token/refresh/`;

// OTP Login Endpoints
export const OTP_LOGIN_URL = `${BACKEND_BASE_URL}/backend/api/login-with-otp/`;
export const OTP_VALIDATE_URL = `${BACKEND_BASE_URL}/backend/api/validate-otp/`;

// ============================================================================
// Session & Message Endpoints
// ============================================================================
export const SESSION_URL = `${BACKEND_BASE_URL}/backend/api/session/`;
export const MESSAGE_URL = `${BACKEND_BASE_URL}/backend/api/message/`;

// ============================================================================
// Student Course Management
// ============================================================================
export const STUDENT_COURSES_URL = `${BACKEND_BASE_URL}/backend/api/student-courses/`;
export const STUDENT_TARGET_COLLEGE_URL = `${BACKEND_BASE_URL}/backend/api/student-target-collage/`;
export const STUDENT_COMMUNITY_COLLEGE_URL = `${BACKEND_BASE_URL}/backend/api/student-community-collage/`;

// ============================================================================
// User Management
// ============================================================================
export const USER_PROFILE_URL = `${BACKEND_BASE_URL}/backend/api/user/`;
export const USER_ATTRIBUTES_URL = `${BACKEND_BASE_URL}/backend/api/user-info/`;

// ============================================================================
// Academic Data Search
// ============================================================================
export const COLLEGE_SEARCH_URL = `${BACKEND_BASE_URL}/backend/api/collage/`;
export const COURSE_SEARCH_URL = `${BACKEND_BASE_URL}/backend/api/course/`;
export const MAJOR_SEARCH_URL = `${BACKEND_BASE_URL}/backend/api/major/`;
export const ACADEMIC_YEARS_URL = `${BACKEND_BASE_URL}/backend/api/academic-years/`;
export const ACADEMIC_SEMESTERS_URL = `${BACKEND_BASE_URL}/backend/api/academic-semesters/`;
export const SCHOOLS_LIST_URL = `${BACKEND_BASE_URL}/backend/api/schools/`;

// ============================================================================
// Connection Requests & Rooms
// ============================================================================
export const CONNECTION_REQUESTS_URL = `${BACKEND_BASE_URL}/backend/api/connection-requests/`;
export const ROOMS_URL = `${BACKEND_BASE_URL}/backend/api/rooms/`;

// ============================================================================
// File Upload
// ============================================================================
export const FILES_URL = `${BACKEND_BASE_URL}/backend/api/files/`;

// ============================================================================
// Meeting Schedules
// ============================================================================
export const MEETING_SCHEDULES_URL = `${BACKEND_BASE_URL}/backend/api/meeting-schedules/`;

// ============================================================================
// Counselor Management
// ============================================================================
export const COUNSELOR_ASSIGNED_COLLEGES_URL = `${BACKEND_BASE_URL}/backend/api/counselor-assigned-college/`;
export const SCHOOL_COUNSELORS_URL = (schoolId: number) =>
  `${BACKEND_BASE_URL}/backend/api/school-counselor/${schoolId}/`;

// ============================================================================
// WebSocket Endpoints
// ============================================================================
export const WS_CHAT_URL = (roomName: string, sessionId: string) =>
  `${WEBSOCKET_URL}/ws/chat/${roomName}/?session_id=${sessionId}`;
export const WS_ASK_GLUIDE_URL = (sessionId: string) =>
  `${WEBSOCKET_URL}/ws/ask-gluide/${sessionId}/?session_id=${sessionId}`;

// ============================================================================
// Gluideme Endpoints
// ============================================================================
export const GLUIDEME_STUDENT_INFO_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/student_info/`;
export const GLUIDEME_STUDENT_DEMOGRAPHICS_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/student-demographics/`;
export const GLUIDEME_STUDENT_GOAL_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/student-goal/`;
export const GLUIDEME_STUDENT_PATHWAYS_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/student-pathways/`;
export const GLUIDEME_COLLEGES_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/colleges/`;
export const GLUIDEME_COURSES_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/courses/`;
export const GLUIDEME_PROGRAMS_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/programs/`;
export const GLUIDEME_EDUCATION_PLAN_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/education-plan/`;
export const GLUIDEME_COUNSELOR_PROFILE_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/counselor-profile/`;
export const GLUIDEME_AI_RECOMMENDATIONS_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/ai-recommendations/`;
export const GLUIDEME_DOCUMENTS_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/documents/`;

// Transcript Endpoints
export const GLUIDEME_TRANSCRIPT_LIST_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/transcripts/list/`;
export const GLUIDEME_TRANSCRIPT_UPLOAD_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/transcripts/upload/`;
export const GLUIDEME_TRANSCRIPT_WEBHOOK_URL = `${BACKEND_BASE_URL}/backend/api/gluideme/transcript-webhooks/`;
