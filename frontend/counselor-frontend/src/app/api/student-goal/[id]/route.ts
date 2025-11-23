import { NextRequest, NextResponse } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { GLUIDEME_STUDENT_GOAL_URL } from "@/constants/server/api";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const url = `${GLUIDEME_STUDENT_GOAL_URL}${id}/`;

    const response = await fetchWithAuth(url, request);

    if (!response.ok) {
      return NextResponse.json(
        { error: "Goal not found", success: false },
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
    console.error("Error fetching goal:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const url = `${GLUIDEME_STUDENT_GOAL_URL}${id}/`;

    const response = await fetchWithAuth(url, request, {
      method: "PUT",
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Update failed", success: false },
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
    console.error("Error updating goal:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const url = `${GLUIDEME_STUDENT_GOAL_URL}${id}/`;

    const response = await fetchWithAuth(url, request, {
      method: "PATCH",
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Update failed", success: false },
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
    console.error("Error updating goal:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const url = `${GLUIDEME_STUDENT_GOAL_URL}${id}/`;

    const response = await fetchWithAuth(url, request, {
      method: "DELETE",
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Delete failed", success: false },
        { status: response.status }
      );
    }

    return NextResponse.json({
      success: true,
      status: 204,
    });
  } catch (error) {
    console.error("Error deleting goal:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}
