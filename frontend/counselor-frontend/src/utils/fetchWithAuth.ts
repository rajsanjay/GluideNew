import { getToken } from "next-auth/jwt";
import { NextRequest } from "next/server";

interface FetchOptions extends RequestInit {
  headers?: Record<string, string>;
}

export async function fetchWithAuth(
  url: string,
  req: NextRequest,
  options: FetchOptions = {}
): Promise<Response> {
  const token = await getToken({ req });

  if (!token?.csrftoken || !token?.sessionid) {
    throw new Error("Not authenticated");
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    "X-CSRFToken": token.csrftoken,
    Cookie: `csrftoken=${token.csrftoken}; sessionid=${token.sessionid}`,
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // Handle auth errors
  if (response.status === 401) {
    throw new Error("Unauthorized");
  }

  if (response.status === 502) {
    throw new Error("Backend unavailable");
  }

  return response;
}

// Helper for client-side fetching (from session)
export async function clientFetchWithAuth(
  url: string,
  csrftoken: string,
  sessionid: string,
  options: FetchOptions = {}
): Promise<Response> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    "X-CSRFToken": csrftoken,
    Cookie: `csrftoken=${csrftoken}; sessionid=${sessionid}`,
    ...options.headers,
  };

  return fetch(url, {
    ...options,
    headers,
  });
}
