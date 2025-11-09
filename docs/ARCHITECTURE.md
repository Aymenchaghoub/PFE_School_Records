# 🏗️ System Architecture

## Overview

School Records Management System is a full-stack web application built with modern technologies, featuring a React frontend, FastAPI backend, and MySQL database.

```
┌─────────────────────────────────────────────────────────┐
│                     ARCHITECTURE                        │
└─────────────────────────────────────────────────────────┘

┌──────────────────────┐      HTTP/REST      ┌──────────────────────┐
│                      │ ◄──────────────────► │                      │
│   React Frontend     │     JSON/JWT         │   FastAPI Backend    │
│   (Vite + Tailwind)  │                      │   (Python 3.13)      │
│                      │                      │                      │
└──────────────────────┘                      └──────────┬───────────┘
                                                         │
                                                         │ SQLAlchemy
                                                         │ ORM
                                                         │
                                              ┌──────────▼───────────┐
                                              │                      │
                                              │   MySQL Database     │
                                              │   (XAMPP / Cloud)    │
                                              │                      │
                                              └──────────────────────┘
```

---

## 🎨 Frontend Architecture

### Technology Stack
- **Framework**: React 19.1
- **Build Tool**: Vite 7.1
- **Language**: TypeScript 5.9
- **Styling**: Tailwind CSS 4.1
- **Routing**: React Router DOM 7.9
- **Charts**: Recharts 3.3
- **Icons**: Lucide React
- **Notifications**: React Hot Toast
- **State Management**: React useState/useEffect (Context API ready)

### Directory Structure
```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Button.tsx       # Modern button component
│   │   ├── Card.tsx         # Card container
│   │   ├── Input.tsx        # Form input
│   │   ├── Toaster.tsx      # Toast notifications
│   │   ├── ErrorBoundary.tsx # Error handling
│   │   └── LoadingSkeleton.tsx # Loading states
│   ├── pages/               # Page components
│   │   ├── Login.tsx        # Authentication page
│   │   └── Dashboard.tsx    # Main dashboard
│   ├── config/              # Configuration
│   │   ├── api.ts           # API endpoints
│   │   ├── analytics.ts     # Analytics integration
│   │   └── utils.ts         # Utility functions
│   ├── index.css            # Global styles
│   └── main.tsx             # Entry point
├── public/                  # Static assets
├── index.html               # HTML template
├── tailwind.config.js       # Tailwind configuration
├── vite.config.ts           # Vite configuration
└── package.json             # Dependencies
```

### Key Features
- **Component-Based**: Modular, reusable components
- **Type-Safe**: Full TypeScript coverage
- **Responsive**: Mobile-first design (360px - 1440px+)
- **Accessible**: WCAG AA compliant
- **Modern UI**: 2025 design standards
- **Error Handling**: React Error Boundary
- **Analytics**: Optional Plausible/GA4 integration

---

## ⚙️ Backend Architecture

### Technology Stack
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.13
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic 1.17
- **Database**: MySQL 8.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib + bcrypt
- **Server**: Uvicorn / Gunicorn

### Directory Structure
```
backend/
├── app/
│   ├── core/                    # Core functionality
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database setup
│   │   ├── security.py          # Auth & JWT
│   │   └── monitoring.py        # Metrics & logging
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py              # User model
│   │   ├── grade.py             # Grade model
│   │   ├── absence.py           # Absence model
│   │   ├── class_model.py       # Class model
│   │   ├── subject.py           # Subject model
│   │   ├── event.py             # Event model
│   │   └── refresh_token.py     # Token model
│   ├── routers/                 # API endpoints
│   │   ├── auth.py              # Authentication
│   │   ├── users.py             # User management
│   │   ├── grades.py            # Grade management
│   │   ├── absences.py          # Absence tracking
│   │   ├── classes.py           # Class management
│   │   ├── subjects.py          # Subject management
│   │   ├── events.py            # Event calendar
│   │   ├── reports.py           # PDF reports
│   │   ├── statistics.py        # Dashboard stats
│   │   └── metrics.py           # Monitoring
│   ├── schemas/                 # Pydantic schemas
│   │   └── ...                  # Request/Response models
│   └── main.py                  # Application entry
├── alembic/                     # Database migrations
│   ├── versions/                # Migration scripts
│   └── env.py                   # Alembic config
├── tests/                       # Unit & integration tests
│   ├── conftest.py              # Test fixtures
│   ├── test_auth.py             # Auth tests
│   ├── test_models.py           # Model tests
│   └── test_health.py           # Health tests
├── .env                         # Environment variables
├── alembic.ini                  # Alembic configuration
├── requirements.txt             # Python dependencies
└── Dockerfile                   # Docker configuration
```

### Key Features
- **RESTful API**: Clean, intuitive endpoints
- **Authentication**: JWT with refresh token rotation
- **Authorization**: Role-based access control (RBAC)
- **Validation**: Pydantic schemas
- **Monitoring**: Metrics endpoint + Sentry integration
- **Rate Limiting**: SlowAPI protection
- **CORS**: Configurable origins
- **Testing**: Pytest with 51%+ coverage

---

## 🗄️ Database Architecture

### Entity Relationship Diagram

```
┌─────────────┐
│    User     │
├─────────────┤
│ id          │◄──────────────┐
│ email       │               │
│ name        │               │
│ password    │               │
│ role        │               │ Foreign Keys
│ created_at  │               │
└──────┬──────┘               │
       │                      │
       │ 1:N                  │
       │                      │
┌──────▼──────┐     ┌─────────┴────────┐
│   Grade     │     │     Absence      │
├─────────────┤     ├──────────────────┤
│ id          │     │ id               │
│ student_id  │     │ student_id       │
│ subject_id  │     │ date             │
│ grade_value │     │ reason           │
│ date        │     │ justified        │
└─────────────┘     └──────────────────┘

┌─────────────┐     ┌──────────────┐
│   Class     │     │   Subject    │
├─────────────┤     ├──────────────┤
│ id          │     │ id           │
│ name        │     │ name         │
│ teacher_id  │     │ description  │
└─────────────┘     │ teacher_id   │
                    └──────────────┘

┌──────────────────┐
│   RefreshToken   │
├──────────────────┤
│ id               │
│ user_id          │
│ token_hash       │
│ expires_at       │
│ revoked          │
└──────────────────┘
```

### Tables

| Table | Description | Key Relationships |
|-------|-------------|-------------------|
| **users** | User accounts (admin, teacher, student, parent) | → grades, absences, classes, subjects |
| **grades** | Student grades | user_id → users, subject_id → subjects |
| **absences** | Attendance tracking | student_id → users |
| **classes** | Class definitions | teacher_id → users |
| **subjects** | Subject courses | teacher_id → users |
| **events** | School events | (standalone) |
| **refresh_tokens** | JWT refresh tokens | user_id → users |

### Indexes
- `users.email` (unique)
- `grades.student_id`, `grades.subject_id`
- `absences.student_id`
- `refresh_tokens.token_hash` (unique)
- `refresh_tokens.user_id, revoked` (composite)

---

## 🔐 Security Architecture

### Authentication Flow

```
1. User Login
   ├─► POST /api/auth/login
   │   └─► {email, password}
   │
2. Verify Credentials
   ├─► Check user exists
   ├─► Verify password hash
   └─► Generate tokens
       ├─► Access Token (JWT, 60min)
       └─► Refresh Token (7 days, stored hashed)
   
3. Access Protected Resource
   ├─► Authorization: Bearer {access_token}
   │   └─► Verify JWT signature
   │       └─► Extract user_id
   │
4. Token Refresh
   ├─► POST /api/auth/refresh
   │   └─► {refresh_token}
   ├─► Verify token exists & not revoked
   ├─► Generate new tokens
   └─► Revoke old refresh token
   
5. Logout
   └─► POST /api/auth/logout
       └─► Revoke all user's refresh tokens
```

### Security Features
- **Password Hashing**: bcrypt (cost factor: 12)
- **JWT Tokens**: HS256 algorithm
- **Refresh Token Rotation**: New token on each refresh
- **Token Revocation**: Stored in database
- **CORS Protection**: Whitelist origins
- **Rate Limiting**: 100 requests/minute
- **SQL Injection**: SQLAlchemy ORM protection
- **XSS Protection**: Content Security Policy headers

---

## 🚀 Deployment Architecture

### Development Environment
```
┌─────────────────────┐
│   Developer Machine │
├─────────────────────┤
│ Windows 11          │
│ Python 3.13         │
│ Node.js 20          │
│ MySQL (XAMPP)       │
└─────────────────────┘
```

### Production Environment (Cloud)
```
┌──────────────────────────────────────────────┐
│             Production Stack                  │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────────┐    ┌─────────────────┐ │
│  │  Netlify CDN   │    │  Render.com     │ │
│  │  (Frontend)    │◄───┤  (Backend)      │ │
│  │  React Build   │    │  Gunicorn       │ │
│  │  Static Files  │    │  + Uvicorn      │ │
│  └────────────────┘    └─────────┬───────┘ │
│                                  │          │
│                                  │          │
│                        ┌─────────▼───────┐ │
│                        │  MySQL Cloud    │ │
│                        │  (PlanetScale/  │ │
│                        │   Render DB)    │ │
│                        └─────────────────┘ │
│                                              │
└──────────────────────────────────────────────┘
```

### Docker Environment
```
docker-compose.yml
├─► frontend (nginx:alpine)
│   └─► Port 80 → React build
├─► backend (python:3.13-slim)
│   └─► Port 8000 → FastAPI
└─► db (mysql:8.0)
    └─► Port 3306 → MySQL
```

---

## 📊 Monitoring & Observability

### Metrics Endpoint: `/metrics`

Returns comprehensive system metrics:

```json
{
  "status": "healthy",
  "application": {
    "uptime_seconds": 3600.45,
    "uptime_formatted": "1h 0m 0s",
    "total_requests": 1523,
    "total_errors": 5,
    "error_rate": 0.33,
    "average_response_time_ms": 45.2,
    "requests_per_minute": 25.4,
    "endpoint_counts": {
      "/api/grades/": 450,
      "/api/users/": 320,
      "/api/absences/": 210
    }
  },
  "database": {
    "status": "connected"
  },
  "system": {
    "cpu_percent": 15.3,
    "memory_percent": 42.1,
    "disk_percent": 35.8
  }
}
```

### Monitoring Features
- Request/response logging
- Performance metrics
- Error tracking
- Database health checks
- System resource monitoring
- Optional Sentry integration

---

## 🔄 Data Flow

### User Login Flow
```
Frontend                     Backend                    Database
   │                            │                          │
   ├─► POST /api/auth/login ───►│                          │
   │   {email, password}        │                          │
   │                            ├─► Query user ───────────►│
   │                            │◄─ User data ─────────────┤
   │                            │                          │
   │                            ├─► Verify password        │
   │                            ├─► Generate JWT           │
   │                            ├─► Create refresh token ──►│
   │                            │◄─ Confirm ───────────────┤
   │◄─ {access_token, user} ───┤                          │
   │                            │                          │
   ├─► Store in localStorage   │                          │
   └─► Navigate to dashboard   │                          │
```

### Dashboard Data Fetch
```
Frontend                     Backend                    Database
   │                            │                          │
   ├─► GET /api/statistics/ ───►│                          │
   │   Authorization: Bearer    │                          │
   │                            ├─► Verify JWT             │
   │                            ├─► Extract user_id        │
   │                            ├─► Query stats ──────────►│
   │                            │◄─ Aggregated data ───────┤
   │◄─ {stats, grades, ...} ───┤                          │
   │                            │                          │
   └─► Render dashboard        │                          │
```

---

## 🧩 API Design

### RESTful Principles
- **Resource-based URLs**: `/api/users/{id}`
- **HTTP Methods**: GET, POST, PUT, PATCH, DELETE
- **Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Server Error)
- **JSON Format**: All requests/responses
- **Pagination**: Query parameters `?skip=0&limit=10`
- **Filtering**: Query parameters `?role=STUDENT`

### Example Endpoints
```
Authentication:
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh
POST   /api/auth/logout

Users:
GET    /api/users/              # List all users
GET    /api/users/{id}          # Get user by ID
POST   /api/users/              # Create user
PUT    /api/users/{id}          # Update user
DELETE /api/users/{id}          # Delete user

Grades:
GET    /api/grades/             # List grades
POST   /api/grades/             # Create grade
GET    /api/grades/{id}         # Get grade
PUT    /api/grades/{id}         # Update grade
DELETE /api/grades/{id}         # Delete grade

Statistics:
GET    /api/statistics/dashboard
GET    /api/statistics/grades-distribution

Monitoring:
GET    /health                  # Health check
GET    /metrics                 # System metrics
```

---

## 🔧 Configuration Management

### Environment Variables

**Backend** (.env):
```bash
# Database
DATABASE_URL=mysql+pymysql://user:pass@host/db

# Security
SECRET_KEY=<32+ character secret>
JWT_EXPIRE_MINUTES=60
JWT_REFRESH_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:5173"]

# Monitoring
ENABLE_SENTRY=false
SENTRY_DSN=
```

**Frontend** (.env):
```bash
# API
VITE_API_URL=http://localhost:8000

# Analytics
VITE_ENABLE_ANALYTICS=false
VITE_ANALYTICS_ID=
VITE_ANALYTICS_PROVIDER=plausible
```

---

## 📈 Performance Characteristics

### Backend
- **Response Time**: ~45ms average
- **Throughput**: 1,000+ req/min (single worker)
- **Database Queries**: Optimized with indexes
- **Memory Usage**: ~200MB (idle), ~500MB (active)

### Frontend
- **Initial Load**: <1.5s (FCP)
- **Time to Interactive**: <3s
- **Bundle Size**: ~200KB gzipped
- **Lighthouse Score**: 90+ (all metrics)

---

## 🛡️ Error Handling

### Backend
- Try-catch blocks around database operations
- Custom exception handlers for FastAPI
- Structured error responses (JSON)
- Logging to files and Sentry (optional)

### Frontend
- React Error Boundary for component errors
- Toast notifications for user feedback
- Graceful degradation for failed API calls
- Loading states to prevent confusion

---

## 🔮 Future Enhancements

1. **WebSocket Support**: Real-time notifications
2. **Redis Caching**: Improve API response times
3. **GraphQL API**: Alternative to REST
4. **Mobile App**: React Native version
5. **Advanced Analytics**: Custom dashboards
6. **Multi-tenancy**: Support multiple schools
7. **SSO Integration**: OAuth2 providers
8. **Audit Logging**: Track all data changes

---

**Last Updated**: November 2025  
**Version**: 1.0.0  
**Python**: 3.13  
**React**: 19.1
