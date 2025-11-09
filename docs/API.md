# 📡 API Documentation

Complete API reference for the School Records Management System.

## Base URL

- **Local**: `http://localhost:8000`
- **Production**: `https://your-backend-url.onrender.com`

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "admin"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
  }
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

### Users

#### Get All Users
```http
GET /api/users
Authorization: Bearer <token>
```

**Query Parameters:**
- `role` (optional): Filter by role (admin, teacher, student, parent)

#### Get User by ID
```http
GET /api/users/{user_id}
Authorization: Bearer <token>
```

#### Create User (Admin only)
```http
POST /api/users
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "password": "password123",
  "role": "student"
}
```

#### Update User (Admin only)
```http
PUT /api/users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Smith",
  "email": "jane.smith@example.com"
}
```

#### Delete User (Admin only)
```http
DELETE /api/users/{user_id}
Authorization: Bearer <token>
```

### Classes

#### Get All Classes
```http
GET /api/classes
Authorization: Bearer <token>
```

#### Get Class by ID
```http
GET /api/classes/{class_id}
Authorization: Bearer <token>
```

#### Create Class (Admin only)
```http
POST /api/classes
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Class 10A",
  "teacher_id": 2
}
```

#### Update Class (Admin only)
```http
PUT /api/classes/{class_id}
Authorization: Bearer <token>
```

#### Delete Class (Admin only)
```http
DELETE /api/classes/{class_id}
Authorization: Bearer <token>
```

### Subjects

#### Get All Subjects
```http
GET /api/subjects
Authorization: Bearer <token>
```

**Query Parameters:**
- `class_id` (optional): Filter by class

#### Create Subject (Admin/Teacher)
```http
POST /api/subjects
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Mathematics",
  "class_id": 1
}
```

### Grades

#### Get All Grades
```http
GET /api/grades
Authorization: Bearer <token>
```

**Query Parameters:**
- `student_id` (optional): Filter by student
- `subject_id` (optional): Filter by subject

#### Create Grade (Admin/Teacher)
```http
POST /api/grades
Authorization: Bearer <token>
Content-Type: application/json

{
  "student_id": 3,
  "subject_id": 1,
  "grade": 15.5
}
```

**Validation:**
- Grade must be between 0 and 20

### Absences

#### Get All Absences
```http
GET /api/absences
Authorization: Bearer <token>
```

**Query Parameters:**
- `student_id` (optional): Filter by student

#### Create Absence (Admin/Teacher)
```http
POST /api/absences
Authorization: Bearer <token>
Content-Type: application/json

{
  "student_id": 3,
  "date": "2024-01-15",
  "reason": "Sick"
}
```

### Events

#### Get All Events
```http
GET /api/events
Authorization: Bearer <token>
```

**Query Parameters:**
- `start_date` (optional): Filter from date (YYYY-MM-DD)
- `end_date` (optional): Filter to date (YYYY-MM-DD)

#### Create Event (Admin/Teacher)
```http
POST /api/events
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Midterm Exam",
  "date": "2024-02-15",
  "description": "Mathematics midterm exam"
}
```

### Reports

#### Download Report Card
```http
GET /api/reports/report-card/{student_id}
Authorization: Bearer <token>
```

Returns PDF file.

### Statistics

#### Get Dashboard Statistics
```http
GET /api/statistics/dashboard
Authorization: Bearer <token>
```

Returns role-specific statistics.

#### Get Grades Distribution
```http
GET /api/statistics/grades-distribution
Authorization: Bearer <token>
```

**Query Parameters:**
- `student_id` (optional)
- `subject_id` (optional)

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

## Rate Limiting

Currently no rate limiting implemented. For production, consider adding rate limiting.

## Pagination

Currently not implemented. For large datasets, consider adding pagination.

## Testing

Use tools like:
- Postman
- Insomnia
- curl
- HTTPie

Example curl request:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@school.com","password":"admin123"}'
```

