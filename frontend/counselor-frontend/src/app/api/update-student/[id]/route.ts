import { NextRequest, NextResponse } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { GLUIDEME_STUDENT_INFO_URL } from "@/constants/server/api";

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const url = `${GLUIDEME_STUDENT_INFO_URL}${id}/`;

    const response = await fetchWithAuth(url, request, {
      method: "PUT",
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: errorData.detail || "Update failed", success: false },
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
    console.error("Error updating student:", error);
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
    const url = `${GLUIDEME_STUDENT_INFO_URL}${id}/`;

    const response = await fetchWithAuth(url, request, {
      method: "PATCH",
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        { error: errorData.detail || "Update failed", success: false },
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
    console.error("Error updating student:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}
