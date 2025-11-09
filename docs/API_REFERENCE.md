# 📘 API Reference

Complete API documentation for the School Records Management System.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-app.onrender.com`

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## 🔐 Authentication Endpoints

### Register User
```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "SecurePassword123",
  "role": "STUDENT"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "role": "STUDENT",
  "created_at": "2025-11-09T12:00:00"
}
```

---

### Login
```http
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "STUDENT"
  }
}
```

---

### Refresh Token
```http
POST /api/auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:** `200 OK` (same as login)

---

### Logout
```http
POST /api/auth/logout
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

---

## 👤 User Endpoints

### List Users
```http
GET /api/users/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)
- `role` (optional): Filter by role (ADMIN, TEACHER, STUDENT, PARENT)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "STUDENT",
    "created_at": "2025-11-09T12:00:00"
  }
]
```

---

### Get User by ID
```http
GET /api/users/{id}
Authorization: Bearer <access_token>
```

**Response:** `200 OK` (single user object)

---

### Update User
```http
PUT /api/users/{id}
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response:** `200 OK` (updated user object)

---

### Delete User
```http
DELETE /api/users/{id}
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "message": "User deleted successfully"
}
```

---

## 📊 Grades Endpoints

### List Grades
```http
GET /api/grades/
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "student_id": 5,
    "subject_id": 2,
    "grade_value": 85.5,
    "grade_type": "exam",
    "date": "2025-11-09T10:00:00"
  }
]
```

---

### Create Grade
```http
POST /api/grades/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "student_id": 5,
  "subject_id": 2,
  "grade_value": 85.5,
  "grade_type": "exam"
}
```

**Response:** `201 Created` (grade object)

---

## 📅 Absence Endpoints

### List Absences
```http
GET /api/absences/
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "student_id": 5,
    "student_name": "John Doe",
    "date": "2025-11-09",
    "reason": "Medical appointment",
    "justified": true
  }
]
```

---

### Create Absence
```http
POST /api/absences/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "student_id": 5,
  "date": "2025-11-09",
  "reason": "Medical appointment",
  "justified": true
}
```

**Response:** `201 Created` (absence object)

---

## 📈 Statistics Endpoints

### Dashboard Statistics
```http
GET /api/statistics/dashboard
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "total_students": 150,
  "total_teachers": 25,
  "total_classes": 12,
  "total_absences": 45
}
```

---

### Grades Distribution
```http
GET /api/statistics/grades-distribution
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {"grade": "A", "count": 45},
  {"grade": "B", "count": 60},
  {"grade": "C", "count": 30},
  {"grade": "D", "count": 10},
  {"grade": "F", "count": 5}
]
```

---

## 🔍 Monitoring Endpoints

### Health Check
```http
GET /health
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

### System Metrics
```http
GET /metrics
```

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "application": {
    "uptime_seconds": 3600.45,
    "uptime_formatted": "1h 0m 0s",
    "total_requests": 1523,
    "error_rate": 0.33,
    "average_response_time_ms": 45.2
  },
  "database": {
    "status": "connected"
  },
  "system": {
    "cpu_percent": 15.3,
    "memory_percent": 42.1
  }
}
```

---

## 📄 Response Codes

| Code | Meaning |
|------|---------|
| **200** | OK - Request successful |
| **201** | Created - Resource created successfully |
| **400** | Bad Request - Invalid input |
| **401** | Unauthorized - Authentication required |
| **403** | Forbidden - Insufficient permissions |
| **404** | Not Found - Resource doesn't exist |
| **422** | Validation Error - Invalid data format |
| **429** | Too Many Requests - Rate limit exceeded |
| **500** | Server Error - Internal server error |

---

## 🔒 Roles & Permissions

| Role | Permissions |
|------|-------------|
| **ADMIN** | Full access to all endpoints |
| **TEACHER** | Manage grades, absences, view students |
| **STUDENT** | View own grades and absences |
| **PARENT** | View children's grades and absences |

---

## 📖 Interactive Documentation

Visit `/docs` for interactive Swagger UI documentation with live testing capabilities.

**URL**: `http://localhost:8000/docs`

---

**Last Updated**: November 2025  
**API Version**: 1.0.0
