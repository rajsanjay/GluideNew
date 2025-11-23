# Gluide Counselor Frontend

Next.js 15 application for the Gluide Counselor Portal.

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:

```bash
npm install
```

2. Copy environment variables:

```bash
cp .env.example .env.local
```

3. Update `.env.local` with your configuration

### Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Build

```bash
npm run build
npm run start
```

## Project Structure

```
src/
├── app/
│   ├── (app)/                    # Protected routes
│   │   ├── dashboard/
│   │   ├── students/
│   │   ├── course-scheduler/
│   │   └── settings/
│   ├── (auth)/                   # Auth routes
│   │   ├── login/
│   │   ├── register/
│   │   └── forgot-password/
│   └── api/
│       └── auth/[...nextauth]/
├── components/
│   ├── ui/                       # Shadcn components
│   └── features/                 # Feature components
├── constants/
│   └── server/
│       └── api.ts               # API endpoints
├── types/
│   ├── student.ts
│   ├── college.ts
│   └── course-scheduler.ts
├── utils/
│   └── fetchWithAuth.ts
└── stores/                       # Zustand stores
```

## Tech Stack

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand (to be added)
- **UI Components:** Shadcn UI (to be added)
- **Authentication:** NextAuth.js (to be added)

## Environment Variables

See `.env.example` for required environment variables.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs)
- [Learn Next.js](https://nextjs.org/learn)
