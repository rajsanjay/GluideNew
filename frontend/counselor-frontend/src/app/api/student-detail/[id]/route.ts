import { NextRequest, NextResponse } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { GLUIDEME_STUDENT_INFO_URL } from "@/constants/server/api";

export const dynamic = "force-dynamic";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const url = `${GLUIDEME_STUDENT_INFO_URL}${id}/`;

    const response = await fetchWithAuth(url, request);

    if (!response.ok) {
      return NextResponse.json(
        { error: "Student not found", success: false },
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
    console.error("Error fetching student:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}
