import { NextRequest, NextResponse } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { GLUIDEME_STUDENT_GOAL_URL } from "@/constants/server/api";

export const dynamic = "force-dynamic";

export async function GET(request: NextRequest) {
  try {
    const studentId = request.nextUrl.searchParams.get("student_id");

    if (!studentId) {
      return NextResponse.json(
        { error: "student_id is required", success: false },
        { status: 400 }
      );
    }

    const url = `${GLUIDEME_STUDENT_GOAL_URL}?student=${studentId}`;
    const response = await fetchWithAuth(url, request);

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to fetch goals", success: false },
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
    console.error("Error fetching goals:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetchWithAuth(GLUIDEME_STUDENT_GOAL_URL, request, {
      method: "POST",
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to create goal", success: false },
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
    console.error("Error creating goal:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}
