# API Routes

This directory contains Next.js API routes that proxy authenticated requests to the Django backend.

## Authentication

All API routes use the `fetchWithAuth` utility which:
- Extracts session tokens from NextAuth JWT
- Includes CSRF token and sessionid in request headers
- Handles authentication errors (401, 502)

## Available Routes

### `/api/list-students`

Fetches paginated list of students from the Django backend.

**Method:** `GET`

**Query Parameters:**
- `page` (optional): Page number, defaults to 1
- `page_size` (optional): Number of items per page, defaults to 10

**Example Request:**
```
GET /api/list-students?page=1&page_size=20
```

**Response Format:**
```json
{
  "data": {
    "count": 100,
    "next": "?page=2",
    "previous": null,
    "results": [
      {
        "id": "uuid",
        "full_name": "John Doe",
        "student_id": "12345",
        "email": "john@example.com",
        "enrollment_status": "Active",
        ...
      }
    ]
  },
  "success": true,
  "status": 200
}
```

**Error Response:**
```json
{
  "error": "Failed to fetch students",
  "success": false
}
```

### `/api/student-detail/[id]`

Fetches detailed information for a specific student by ID.

**Method:** `GET`

**Path Parameters:**
- `id` (required): Student UUID

**Example Request:**
```
GET /api/student-detail/550e8400-e29b-41d4-a716-446655440000
```

**Response Format:**
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "John Doe",
    "first_name": "John",
    "last_name": "Doe",
    "student_id": "12345",
    "email": "john@example.com",
    "phone": "555-1234",
    "enrollment_status": "Active",
    "program": "Computer Science",
    "major": "CS",
    "gpa": "3.5",
    "academic_standing": "Good Standing",
    "stage": "Sophomore",
    "pathway": "Transfer",
    "advisor": "Dr. Smith",
    "target_graduation": "Spring 2025",
    "transfer_target": "UC Berkeley",
    "skills": ["Python", "Java"],
    "goals": ["Transfer to UC"],
    "last_contact": "2024-01-15",
    "next_followup": "2024-02-15",
    "notes": "Excellent student",
    "created_at": "2023-09-01T00:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "success": true,
  "status": 200
}
```

**Error Response:**
```json
{
  "error": "Student not found",
  "success": false
}
```

### `/api/update-student/[id]`

Updates student information. Supports both full updates (PUT) and partial updates (PATCH).

**Methods:** `PUT`, `PATCH`

**Path Parameters:**
- `id` (required): Student UUID

**Request Body (PUT - all fields required):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "555-1234",
  "student_id": "12345",
  "enrollment_status": "Active",
  "gpa": "3.5",
  "major": "Computer Science",
  "advisor": "Dr. Smith",
  "target_graduation": "Spring 2025",
  "skills": ["Python", "Java"],
  "goals": ["Transfer to UC"],
  "notes": "Excellent student",
  "last_contact": "2024-01-15",
  "next_followup": "2024-02-15",
  "stage": "Sophomore",
  "academic_standing": "Good Standing"
}
```

**Request Body (PATCH - only fields to update):**
```json
{
  "gpa": "3.7",
  "notes": "Updated notes",
  "next_followup": "2024-03-01"
}
```

**Example Request:**
```
PUT /api/update-student/550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  ...
}
```

**Response Format:**
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "full_name": "John Doe",
    "first_name": "John",
    "last_name": "Doe",
    "student_id": "12345",
    ...
  },
  "success": true,
  "status": 200
}
```

**Error Response:**
```json
{
  "error": "Update failed",
  "success": false
}
```

### `/api/student-demographics`

Fetches or creates student demographic information.

**Methods:** `GET`, `POST`

**GET Query Parameters:**
- `student_id` (required): Student UUID

**GET Example Request:**
```
GET /api/student-demographics?student_id=550e8400-e29b-41d4-a716-446655440000
```

**GET Response Format:**
```json
{
  "data": {
    "results": [
      {
        "id": "demo-uuid",
        "student": "550e8400-e29b-41d4-a716-446655440000",
        "pers_info_age": 20,
        "pers_info_primary_language_spoken_at_home": "English",
        "edu_back_first_in_family_to_attent_college": "Yes",
        "fin_info_eligible_for_pell_grant": "Yes",
        "life_employment_status": "Part-time",
        "goals_primary_goal_to_attend_college": "Transfer to 4-year",
        ...
      }
    ]
  },
  "success": true,
  "status": 200
}
```

**POST Request Body:**
```json
{
  "student": "550e8400-e29b-41d4-a716-446655440000",
  "pers_info_age": 20,
  "pers_info_primary_language_spoken_at_home": "English",
  "edu_back_first_in_family_to_attent_college": "Yes",
  "fin_info_eligible_for_pell_grant": "Yes",
  ...
}
```

**POST Response:**
```json
{
  "data": {
    "id": "demo-uuid",
    "student": "550e8400-e29b-41d4-a716-446655440000",
    ...
  },
  "success": true,
  "status": 201
}
```

### `/api/student-demographics/[id]`

Updates student demographic information.

**Methods:** `PUT`, `PATCH`

**Path Parameters:**
- `id` (required): Demographics record UUID

**PUT Request Body (all fields):**
```json
{
  "student": "550e8400-e29b-41d4-a716-446655440000",
  "pers_info_age": 21,
  "pers_info_primary_language_spoken_at_home": "Spanish",
  "edu_back_first_in_family_to_attent_college": "Yes",
  ...
}
```

**PATCH Request Body (partial fields):**
```json
{
  "pers_info_age": 21,
  "life_employment_status": "Full-time"
}
```

**Response Format:**
```json
{
  "data": {
    "id": "demo-uuid",
    "student": "550e8400-e29b-41d4-a716-446655440000",
    "pers_info_age": 21,
    ...
  },
  "success": true,
  "status": 200
}
```

### `/api/student-goal`

Fetches or creates student goals (academic, career, transfer, personal).

**Methods:** `GET`, `POST`

**GET Query Parameters:**
- `student_id` (required): Student UUID

**GET Example Request:**
```
GET /api/student-goal?student_id=550e8400-e29b-41d4-a716-446655440000
```

**GET Response Format:**
```json
{
  "data": {
    "results": [
      {
        "goal_id": "goal-uuid",
        "student": "550e8400-e29b-41d4-a716-446655440000",
        "goal_type": "transfer",
        "goal_description": "Transfer to UC Berkeley",
        "target_date": "2025-09-01",
        "priority": "high",
        "status": "active",
        "progress_notes": "Meeting GPA requirements"
      }
    ]
  },
  "success": true,
  "status": 200
}
```

**POST Request Body:**
```json
{
  "student": "550e8400-e29b-41d4-a716-446655440000",
  "goal_type": "transfer",
  "goal_description": "Transfer to UC Berkeley",
  "target_date": "2025-09-01",
  "priority": "high",
  "status": "active",
  "progress_notes": "Meeting GPA requirements"
}
```

**Goal Types:**
- `academic` - Academic achievement goals
- `career` - Career preparation goals
- `transfer` - Transfer to 4-year institution
- `personal` - Personal development goals

**Priority Levels:** `high`, `medium`, `low`

**Status Options:** `active`, `completed`, `deferred`, `cancelled`

**POST Response:**
```json
{
  "data": {
    "goal_id": "goal-uuid",
    "student": "550e8400-e29b-41d4-a716-446655440000",
    ...
  },
  "success": true,
  "status": 201
}
```

### `/api/student-goal/[id]`

Fetch, update, or delete a specific student goal.

**Methods:** `GET`, `PUT`, `PATCH`, `DELETE`

**Path Parameters:**
- `id` (required): Goal UUID

**GET Example:**
```
GET /api/student-goal/goal-uuid
```

**PUT Request Body (all fields):**
```json
{
  "student": "550e8400-e29b-41d4-a716-446655440000",
  "goal_type": "transfer",
  "goal_description": "Transfer to UCLA",
  "target_date": "2025-09-01",
  "priority": "high",
  "status": "active",
  "progress_notes": "Updated progress"
}
```

**PATCH Request Body (partial):**
```json
{
  "status": "completed",
  "progress_notes": "Successfully transferred"
}
```

**DELETE Example:**
```
DELETE /api/student-goal/goal-uuid
```

**DELETE Response:**
```json
{
  "success": true,
  "status": 204
}
```

### `/api/course-scheduler`

Manages student course schedules and saved courses.

**Methods:** `GET`, `POST`, `PUT`, `DELETE`

**GET Query Parameters:**
- `id` (optional): Specific schedule/course ID
- `student_id` (optional): Filter by student UUID

**GET Examples:**
```
# Get all schedules
GET /api/course-scheduler

# Get specific schedule
GET /api/course-scheduler?id=123

# Get schedules for student
GET /api/course-scheduler?student_id=550e8400-e29b-41d4-a716-446655440000
```

**GET Response Format:**
```json
{
  "data": {
    "results": [
      {
        "id": "course-id",
        "course_code": "CS101",
        "course_name": "Introduction to Computer Science",
        "institution": "Community College",
        "grade": "A",
        "status": "completed",
        "semester": "Fall",
        "year": 2024,
        "credits": "3.0",
        "verified_by_counselor": true,
        "source": "manual"
      }
    ]
  },
  "success": true,
  "status": 200
}
```

**POST Request Body:**
```json
{
  "course_code": "CS101",
  "course_name": "Introduction to Computer Science",
  "institution": "Community College",
  "grade": "A",
  "status": "enrolled",
  "semester": "Spring",
  "year": 2025,
  "credits": "3.0",
  "verified_by_counselor": false,
  "source": "manual"
}
```

**POST Response:**
```json
{
  "data": {
    "id": "course-id",
    "course_code": "CS101",
    ...
  },
  "success": true,
  "status": 201
}
```

**PUT Request Body:**
```json
{
  "id": "course-id",
  "course_code": "CS101",
  "course_name": "Introduction to Computer Science",
  "grade": "A+",
  "status": "completed",
  ...
}
```

**DELETE Example:**
```
DELETE /api/course-scheduler?id=course-id
```

**DELETE Response:**
```json
{
  "success": true,
  "status": 204
}
```

### `/api/get-pathways`

Computes transfer pathways from community colleges to target universities based on completed courses.

**Method:** `POST`

**Request Body:**
```json
{
  "courses": [101, 102, 103],
  "source_college_id": 5,
  "target_colleges": [10, 15, 20],
  "academic_year_id": 2024,
  "operator": "OR"
}
```

**Request Fields:**
- `courses` (required): Array of course IDs completed at source college
- `source_college_id` (required): Community college ID (integer)
- `target_colleges` (required): Array of target university IDs
- `academic_year_id` (required): Academic year ID for articulation agreements
- `operator` (optional): Logic operator for course matching
  - `"OR"` (default) - Pathways matching any courses
  - `"AND"` - Pathways requiring all courses

**Example Request:**
```
POST /api/get-pathways
Content-Type: application/json

{
  "courses": [101, 102, 103],
  "source_college_id": 5,
  "target_colleges": [10, 15],
  "academic_year_id": 2024,
  "operator": "OR"
}
```

**Response Format:**
```json
{
  "data": {
    "pathways": [
      {
        "target_college": {
          "id": 10,
          "name": "UC Berkeley",
          "type": "UC"
        },
        "programs": [
          {
            "program_id": "prog-uuid",
            "program_name": "Computer Science",
            "program_type": "bachelor",
            "matched_courses": [101, 102],
            "required_courses": [101, 102, 103, 104],
            "completion_percentage": 50,
            "articulation_notes": "IGETC certified"
          }
        ]
      }
    ]
  },
  "success": true,
  "status": 200
}
```

**Use Case:**
This endpoint helps counselors identify transfer pathways by:
1. Analyzing student's completed courses at community college
2. Finding articulation agreements with target universities
3. Computing completion percentage for each pathway
4. Recommending programs based on course alignment

### `/api/auth/[...nextauth]`

NextAuth.js authentication endpoints (login, session, etc.)

See NextAuth documentation for details.

## Creating New API Routes

1. Create a new directory under `/api` with the route name
2. Create a `route.ts` file with GET/POST handlers
3. Use `fetchWithAuth` for authenticated requests
4. Return responses using the `ApiResponse` format

**Example (Simple Route):**
```typescript
import { NextRequest, NextResponse } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { BACKEND_ENDPOINT } from "@/constants/server/api";

export const dynamic = "force-dynamic";

export async function GET(request: NextRequest) {
  try {
    const response = await fetchWithAuth(BACKEND_ENDPOINT, request);
    const data = await response.json();

    return NextResponse.json({
      data,
      success: true,
      status: 200,
    });
  } catch (error) {
    return NextResponse.json(
      { error: error.message, success: false },
      { status: 500 }
    );
  }
}
```

**Example (Dynamic Route with Parameters):**
```typescript
import { NextRequest, NextResponse } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { BACKEND_ENDPOINT } from "@/constants/server/api";

export const dynamic = "force-dynamic";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    // IMPORTANT: In Next.js 15, params must be awaited
    const { id } = await params;
    const url = `${BACKEND_ENDPOINT}${id}/`;

    const response = await fetchWithAuth(url, request);
    const data = await response.json();

    return NextResponse.json({
      data,
      success: true,
      status: 200,
    });
  } catch (error) {
    return NextResponse.json(
      { error: error.message, success: false },
      { status: 500 }
    );
  }
}
```

## Dynamic Routes

Mark routes as dynamic to prevent caching:

```typescript
export const dynamic = "force-dynamic";
export const revalidate = 0;
```

This ensures fresh data on every request.
