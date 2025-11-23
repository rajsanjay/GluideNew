import "next-auth";
import "next-auth/jwt";

declare module "next-auth" {
  interface User {
    csrftoken?: string;
    sessionid?: string;
    role?: string;
    isVerified?: boolean;
  }
  interface Session {
    user: User & {
      csrftoken?: string;
      sessionid?: string;
      role?: string;
      isVerified?: boolean;
    };
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    csrftoken?: string;
    sessionid?: string;
    role?: string;
    isVerified?: boolean;
  }
}
