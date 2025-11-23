import { NextRequest, NextResponse } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { GLUIDEME_STUDENT_PATHWAYS_URL } from "@/constants/server/api";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate required fields
    const { courses, source_college_id, target_colleges, academic_year_id, operator } = body;

    if (!courses || !source_college_id || !target_colleges || !academic_year_id) {
      return NextResponse.json(
        { error: "Missing required fields", success: false },
        { status: 400 }
      );
    }

    const response = await fetchWithAuth(GLUIDEME_STUDENT_PATHWAYS_URL, request, {
      method: "POST",
      body: JSON.stringify({
        courses,
        source_college_id,
        target_colleges,
        academic_year_id,
        operator: operator || "OR",
      }),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to compute pathways", success: false },
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
    console.error("Error computing pathways:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}
