# Gluide - Academic Planning Platform

A consolidated Django + Next.js application combining AI-powered transcript parsing, course recommendations, and counselor guidance tools.

## Architecture

This is a **monorepo** containing:
- **Backend**: Django 5.1.1 + Django REST Framework 3.15.2 (Python 3.11+)
- **Frontend**: Next.js 15.4.5 + React 19.1.1 + TypeScript 5.8.3

## Features

### Core Features
- **AI Transcript Parsing**: Upload and parse academic transcripts using AI
- **Course Management**: Browse courses from existing course database
- **Student Profiles**: Manage student information and academic records
- **Saved Courses**: Save and track courses of interest

### Counselor Features (GluideMe)
- **Counselor Dashboard**: Manage assigned students
- **Guidance Sessions**: Schedule and track counseling sessions
- **Recommendations**: Provide course and program recommendations
- **Student Tracking**: Monitor student progress and academic plans

### AI Features (GluideAI)
- **Transcript Parser**: Extract course data from transcripts using OpenAI
- **Data Validation**: Validate and enhance parsed transcript data
- **Processing Logs**: Track AI processing attempts and results
- **Async Processing**: Background processing with Celery

## Two Operating Modes

### 1. TEST MODE (Synthetic Data)
- Uses SQLite databases
- No external service connections required
- Perfect for development and testing
- Uses fixture data from `backend/api/fixtures/` and `backend/gluideme/fixtures/`

### 2. DATABASE MODE (Production)
- Connects to **EXISTING** PostgreSQL databases
- Connects to **EXISTING** external services (Pinecone, Meilisearch, S3, Redis, OpenAI)
- DO NOT create new databases - configure existing ones

## Project Structure

```
gluide-me-app/
├── backend/                    # Django backend
│   ├── api/                    # Main API app
│   │   ├── fixtures/           # Test mode synthetic data
│   │   ├── models.py           # Primary database models
│   │   └── models_course_db.py # Course database models
│   ├── gluideme/               # Counselor features app
│   │   ├── fixtures/           # Test mode synthetic data
│   │   └── models.py           # Counselor models
│   ├── gluideai/               # AI transcript parser app
│   │   ├── llm/                # LLM integration
│   │   ├── prompts/templates/  # AI prompt templates
│   │   ├── middleware/         # Custom middleware
│   │   └── tasks.py            # Celery tasks
│   ├── config/                 # Django settings
│   │   ├── settings.py         # Base settings
│   │   ├── settings_test.py    # Test mode settings
│   │   └── settings_database.py # Database mode settings
│   ├── pyproject.toml          # Poetry dependencies
│   └── manage.py
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/                # Next.js App Router
│   │   ├── components/         # React components
│   │   ├── types/              # TypeScript types
│   │   ├── constants/          # API endpoints
│   │   └── lib/                # Utilities
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml          # Redis only (optional)
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ and pnpm
- Poetry for Python dependency management

### Backend Setup

#### Test Mode (Recommended for Development)

```bash
cd backend

# Install dependencies with Poetry
poetry install

# Activate virtual environment
poetry shell

# Copy test mode environment file
cp .env.test.example .env

# Run migrations for SQLite
python manage.py migrate --database=default
python manage.py migrate --database=course_db

# Create superuser
python manage.py createsuperuser

# Load test fixtures (if available)
python manage.py loaddata api/fixtures/*.json
python manage.py loaddata gluideme/fixtures/*.json

# Run development server
python manage.py runserver
```

#### Database Mode (Production)

```bash
cd backend

# Install dependencies
poetry install
poetry shell

# Copy database mode environment file
cp .env.database.example .env

# IMPORTANT: Edit .env and configure your EXISTING databases
# - POSTGRES_HOST, POSTGRES_PASSWORD (primary database)
# - DB_HOST, DB_PASSWORD (course database)
# - REDIS_HOST, AWS credentials, API keys, etc.

# Run migrations (only for primary database, course_db is managed=False)
python manage.py migrate --database=default

# Run server
python manage.py runserver
```

### Frontend Setup

#### Test Mode

```bash
cd frontend

# Install dependencies with pnpm
pnpm install

# Copy test mode environment file
cp .env.test.example .env.local

# Run development server
pnpm dev
```

#### Database Mode

```bash
cd frontend
pnpm install

# Copy database mode environment file
cp .env.database.example .env.local

# Edit .env.local if needed
pnpm dev
```

### Optional: Redis with Docker

If you don't have an existing Redis instance:

```bash
# Start Redis
docker-compose up -d redis

# Stop Redis
docker-compose down
```

## Development Workflow

### Running Both Services

```bash
# Terminal 1 - Backend
cd backend
poetry shell
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
pnpm dev
```

### Running Celery (for AI processing)

```bash
# Terminal 3 - Celery Worker
cd backend
poetry shell
celery -A config worker -l info

# Terminal 4 - Celery Beat (optional, for scheduled tasks)
celery -A config beat -l info
```

## API Endpoints

### Main API (`/api/`)
- `GET /api/students/` - List students
- `GET /api/transcripts/` - List transcripts
- `POST /api/transcripts/{id}/process/` - Process transcript with AI
- `GET /api/courses/` - List courses (from course_db)
- `GET /api/saved-courses/` - Student saved courses

### GluideMe - Counselor (`/api/gluideme/`)
- `GET /api/gluideme/counselors/` - List counselors
- `GET /api/gluideme/assignments/` - Counselor-student assignments
- `GET /api/gluideme/sessions/` - Guidance sessions
- `GET /api/gluideme/recommendations/` - Recommendations

### GluideAI - AI Processing (`/api/gluideai/`)
- `GET /api/gluideai/parsed-transcripts/` - Parsed transcript data
- `GET /api/gluideai/processing-logs/` - AI processing logs
- `POST /api/gluideai/processing-logs/trigger_processing/` - Trigger AI processing

## Technology Stack

### Backend
- **Django** 5.1.1
- **Django REST Framework** 3.15.2
- **PostgreSQL** (existing databases)
- **Celery** + Redis (async tasks)
- **OpenAI** (transcript parsing)
- **Pinecone** (vector search)
- **Meilisearch** (search)
- **AWS S3** (file storage)

### Frontend
- **Next.js** 15.4.5 (App Router)
- **React** 19.1.1
- **TypeScript** 5.8.3
- **pnpm** (package manager)

## Database Configuration

### Two Databases

1. **Primary Database** (`default`): Student data, transcripts, counselor data
   - Test Mode: SQLite (`test_db.sqlite3`)
   - Database Mode: PostgreSQL (existing `gluide_me`)

2. **Course Database** (`course_db`): Course catalog (read-only)
   - Test Mode: SQLite (`test_course_db.sqlite3`)
   - Database Mode: PostgreSQL (existing `course_db`)

### Database Routers
- `TestDatabaseRouter`: Routes models in test mode
- `ProductionDatabaseRouter`: Routes models to appropriate databases in production

## External Services

All external services are **EXISTING** - do not create new ones:
- **PostgreSQL**: Two existing databases (primary + course)
- **Redis**: Existing Redis instance
- **AWS S3**: Existing S3 bucket
- **Pinecone**: Existing vector database
- **Meilisearch**: Existing search service
- **OpenAI**: Existing API account

Configure these in `backend/.env.database`.

## Testing

```bash
# Backend tests
cd backend
poetry shell
pytest

# Frontend tests (if configured)
cd frontend
pnpm test
```

## Production Deployment

1. Set `DEBUG=False` in backend/.env
2. Configure production database credentials
3. Set up proper CORS origins
4. Configure static file serving
5. Use production-grade WSGI server (Gunicorn)
6. Set up Celery workers with supervisor/systemd
7. Configure SSL/HTTPS

## Environment Variables

See example files:
- `backend/.env.test.example` - Test mode configuration
- `backend/.env.database.example` - Database mode configuration
- `frontend/.env.test.example` - Frontend test mode
- `frontend/.env.database.example` - Frontend database mode

## Contributing

This is a consolidated application combining four repositories:
- Student portal
- Counselor dashboard (GluideMe)
- AI transcript parser (GluideAI)
- Course catalog integration

## License

Proprietary - All rights reserved

## Support

For issues or questions, please contact the development team.
