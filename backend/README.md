# OT Assessment Tracker - Django Backend

Hospital-grade, HIPAA-compliant Django backend for occupational therapy patient assessments.

## Features

- ✅ Multi-tenancy (Schema-per-Tenant with PostgreSQL)
- ✅ HIPAA-compliant security (encryption, audit logging, session management)
- ✅ Django REST Framework API
- ✅ JWT Authentication
- ✅ Field-level encryption for PHI
- ✅ Comprehensive audit logging
- ✅ Role-based access control (RBAC)

## Tech Stack

- Django 5.0+
- Django REST Framework
- PostgreSQL 15+ (with django-tenants)
- pytest for testing
- JWT for authentication

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings (database credentials, etc.)
```

### 3. Setup Database

```bash
# Install PostgreSQL 15+ if not installed

# Create database and user
psql -U postgres
CREATE DATABASE ot_assessment_db;
CREATE USER ot_user WITH PASSWORD 'ot_password';
GRANT ALL PRIVILEGES ON DATABASE ot_assessment_db TO ot_user;
\q
```

### 4. Run Migrations

```bash
# Run migrations for public schema
python manage.py migrate_schemas --shared

# Run migrations for tenant schemas
python manage.py migrate_schemas
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit http://localhost:8000/admin

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_models_organization.py

# Run specific test
pytest tests/test_models_organization.py::test_organization_creation
```

## Project Structure

```
backend/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings (HIPAA-compliant)
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI config
├── organizations/          # Multi-tenancy app
│   └── models.py          # Organization/Domain models
├── users/                  # Therapist/staff app
│   └── models.py          # User model (custom)
├── patients/               # Patient records app
│   └── models.py          # Patient model (PHI)
├── assessments/            # Assessment app
│   ├── models.py          # Assessment models
│   └── serializers.py     # DRF serializers
├── tests/                  # Test suite
├── manage.py               # Django management script
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Python dependencies
```

## Development Workflow

We're building **incrementally** - one model at a time with full test coverage:

1. Design model schema
2. Write Django model
3. Create migrations
4. Write unit tests
5. Run tests & verify
6. Commit to git
7. Move to next model

## API Endpoints (Coming Soon)

```
# Authentication
POST   /api/auth/login/
POST   /api/auth/logout/
POST   /api/auth/refresh/

# Patients
GET    /api/patients/
POST   /api/patients/
GET    /api/patients/{id}/
PUT    /api/patients/{id}/
DELETE /api/patients/{id}/

# Assessments
GET    /api/assessments/
POST   /api/assessments/
GET    /api/assessments/{id}/
PUT    /api/assessments/{id}/
```

## HIPAA Compliance

This application implements:

- **Encryption at Rest**: PostgreSQL TDE + field-level encryption
- **Encryption in Transit**: TLS 1.3+ (HTTPS)
- **Audit Logging**: Every PHI access is logged
- **Access Control**: Role-based permissions (OT, OTA, Admin, Viewer)
- **Session Management**: 15-minute inactivity timeout
- **Password Policy**: 12+ characters, 90-day expiry
- **Data Retention**: 7-year minimum

## Contributing

This is a professional healthcare application. Please follow these guidelines:

- Write tests for all new features
- Follow PEP 8 style guide
- Use meaningful commit messages
- Never commit sensitive data (.env files)
- Document all API endpoints

## License

MIT License - See LICENSE file

## Contact

For questions or issues, please open a GitHub issue.
