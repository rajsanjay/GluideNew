# Fetch Utilities

## fetchWithAuth (Server-side)

Use this function for server-side API routes that need to make authenticated requests to the Django backend.

### Example: API Route Handler

```typescript
import { NextRequest } from "next/server";
import { fetchWithAuth } from "@/utils/fetchWithAuth";
import { createSuccessResponse, createErrorResponse } from "@/types/api";
import { USER_PROFILE_URL } from "@/constants/server/api";

export async function GET(req: NextRequest) {
  try {
    const response = await fetchWithAuth(USER_PROFILE_URL, req);
    const data = await response.json();

    return Response.json(createSuccessResponse(data));
  } catch (error) {
    return Response.json(
      createErrorResponse(error instanceof Error ? error.message : "Unknown error", 500),
      { status: 500 }
    );
  }
}
```

## clientFetchWithAuth (Client-side)

Use this function for client-side components that need to make authenticated requests.

### Example: Client Component

```typescript
"use client";

import { useSession } from "next-auth/react";
import { clientFetchWithAuth } from "@/utils/fetchWithAuth";
import { USER_PROFILE_URL } from "@/constants/server/api";

export function ProfileComponent() {
  const { data: session } = useSession();

  async function fetchProfile() {
    if (!session?.user?.csrftoken || !session?.user?.sessionid) {
      return;
    }

    const response = await clientFetchWithAuth(
      USER_PROFILE_URL,
      session.user.csrftoken,
      session.user.sessionid
    );

    const data = await response.json();
    console.log(data);
  }

  return (
    <button onClick={fetchProfile}>Load Profile</button>
  );
}
```

## API Response Format

All API routes should return responses using the `ApiResponse` interface:

```typescript
interface ApiResponse<T = unknown> {
  data?: T;
  success: boolean;
  status: number;
  error?: string;
}
```

### Helper Functions

- `createSuccessResponse<T>(data: T, status?: number)` - Creates a success response
- `createErrorResponse(error: string, status?: number)` - Creates an error response
