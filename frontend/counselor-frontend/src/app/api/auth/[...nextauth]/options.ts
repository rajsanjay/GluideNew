import type { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { AUTH_LOGIN_URL } from "@/constants/server/api";

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        try {
          // Get CSRF token first
          const csrfResponse = await fetch(AUTH_LOGIN_URL, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
          });

          const csrfCookies = csrfResponse.headers.get("set-cookie");
          const csrfToken = csrfCookies?.match(/csrftoken=([^;]+)/)?.[1];

          // Login with credentials
          const response = await fetch(AUTH_LOGIN_URL, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken || "",
              Cookie: `csrftoken=${csrfToken}`,
            },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          });

          if (!response.ok) {
            return null;
          }

          const cookies = response.headers.get("set-cookie");
          const sessionid = cookies?.match(/sessionid=([^;]+)/)?.[1];
          const newCsrfToken = cookies?.match(/csrftoken=([^;]+)/)?.[1] || csrfToken;

          // Get user role
          const roleResponse = await fetch(
            `${process.env.BACKEND_BASE_URL}/backend/api/user/`,
            {
              headers: {
                Cookie: `csrftoken=${newCsrfToken}; sessionid=${sessionid}`,
                "X-CSRFToken": newCsrfToken || "",
              },
            }
          );

          const userData = await roleResponse.json();
          const role = userData.designation?.name || "STUDENT";

          // Only allow COUNSELOR role
          if (role !== "COUNSELOR") {
            return null;
          }

          return {
            id: userData.id.toString(),
            email: credentials.email,
            username: userData.username,
            csrftoken: newCsrfToken,
            sessionid: sessionid,
            role: role,
            isVerified: userData.user_attribute?.is_verified || false,
          };
        } catch (error) {
          console.error("Auth error:", error);
          return null;
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.csrftoken = user.csrftoken;
        token.sessionid = user.sessionid;
        token.role = user.role;
        token.isVerified = user.isVerified;
      }
      return token;
    },
    async session({ session, token }) {
      session.user.csrftoken = token.csrftoken as string;
      session.user.sessionid = token.sessionid as string;
      session.user.role = token.role as string;
      session.user.isVerified = token.isVerified as boolean;
      return session;
    },
  },
  pages: {
    signIn: "/login",
    error: "/login",
  },
  session: {
    strategy: "jwt",
  },
};
