import { NextRequest, NextResponse } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { STUDENT_COURSES_URL } from "@/constants/server/api";

export const dynamic = "force-dynamic";

// Get saved schedules/courses
export async function GET(request: NextRequest) {
  try {
    const id = request.nextUrl.searchParams.get("id");
    const studentId = request.nextUrl.searchParams.get("student_id");

    let url = STUDENT_COURSES_URL;

    if (id) {
      url = `${STUDENT_COURSES_URL}${id}/`;
    } else if (studentId) {
      url = `${STUDENT_COURSES_URL}?student=${studentId}`;
    }

    const response = await fetchWithAuth(url, request);

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to fetch schedules", success: false },
        { status: response.status }
      );
    }

    const data = await response.json();

    return NextResponse.json({
      data,
      success: true,
      status: 200,
    });
  } catch (error) {
    console.error("Error fetching schedules:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}

// Save new schedule/course
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetchWithAuth(STUDENT_COURSES_URL, request, {
      method: "POST",
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to save schedule", success: false },
        { status: response.status }
      );
    }

    const data = await response.json();

    return NextResponse.json({
      data,
      success: true,
      status: 201,
    });
  } catch (error) {
    console.error("Error saving schedule:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}

// Update existing schedule/course
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const { id, ...scheduleData } = body;

    if (!id) {
      return NextResponse.json(
        { error: "Schedule ID is required", success: false },
        { status: 400 }
      );
    }

    const url = `${STUDENT_COURSES_URL}${id}/`;
    const response = await fetchWithAuth(url, request, {
      method: "PUT",
      body: JSON.stringify(scheduleData),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to update schedule", success: false },
        { status: response.status }
      );
    }

    const data = await response.json();

    return NextResponse.json({
      data,
      success: true,
      status: 200,
    });
  } catch (error) {
    console.error("Error updating schedule:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}

// Delete schedule/course
export async function DELETE(request: NextRequest) {
  try {
    const id = request.nextUrl.searchParams.get("id");

    if (!id) {
      return NextResponse.json(
        { error: "Schedule ID is required", success: false },
        { status: 400 }
      );
    }

    const url = `${STUDENT_COURSES_URL}${id}/`;
    const response = await fetchWithAuth(url, request, {
      method: "DELETE",
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to delete schedule", success: false },
        { status: response.status }
      );
    }

    return NextResponse.json({
      success: true,
      status: 204,
    });
  } catch (error) {
    console.error("Error deleting schedule:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}
