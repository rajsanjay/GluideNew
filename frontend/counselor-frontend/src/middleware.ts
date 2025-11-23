import { withAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

export default withAuth(
  function middleware(req) {
    const token = req.nextauth.token;
    const path = req.nextUrl.pathname;

    // Protected routes that require COUNSELOR role
    const protectedPaths = [
      "/dashboard",
      "/students",
      "/course-scheduler",
      "/settings",
      "/chat",
    ];

    const isProtectedPath = protectedPaths.some((p) => path.startsWith(p));

    if (isProtectedPath) {
      // Check if user is authenticated
      if (!token) {
        return NextResponse.redirect(new URL("/login", req.url));
      }

      // Check if user has COUNSELOR role
      if (token.role !== "COUNSELOR") {
        return NextResponse.redirect(new URL("/unauthorized", req.url));
      }
    }

    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: ({ token, req }) => {
        const path = req.nextUrl.pathname;

        // Public paths
        const publicPaths = [
          "/login",
          "/register",
          "/forgot-password",
          "/reset-password",
          "/verify-email",
        ];

        if (publicPaths.some((p) => path.startsWith(p))) {
          return true;
        }

        return !!token;
      },
    },
  }
);

export const config = {
  matcher: [
    "/((?!api|_next/static|_next/image|favicon.ico|public).*)",
  ],
};
