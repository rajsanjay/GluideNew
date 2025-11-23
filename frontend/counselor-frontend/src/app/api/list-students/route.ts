import { NextRequest, NextResponse } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { GLUIDEME_STUDENT_INFO_URL } from "@/constants/server/api";

export const dynamic = "force-dynamic";
export const revalidate = 0;

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const page = searchParams.get("page") || "1";
    const pageSize = searchParams.get("page_size") || "10";

    const url = `${GLUIDEME_STUDENT_INFO_URL}?page=${page}&page_size=${pageSize}`;

    const response = await fetchWithAuth(url, request);

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to fetch students", success: false },
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
    console.error("Error fetching students:", error);
    return NextResponse.json(
      { error: "Internal server error", success: false },
      { status: 500 }
    );
  }
}
