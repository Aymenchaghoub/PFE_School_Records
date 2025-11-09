/**
 * API Configuration
 * Centralized API URL management using environment variables
 */

// Get API URL from environment variables
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// API endpoints configuration
export const API_CONFIG = {
  baseURL: API_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
}

// API endpoint paths
export const API_ENDPOINTS = {
  // Authentication
  auth: {
    login: '/api/auth/login',
    register: '/api/auth/register',
    refresh: '/api/auth/refresh',
    logout: '/api/auth/logout',
  },
  // Users
  users: {
    list: '/api/users/',
    detail: (id: number) => `/api/users/${id}`,
    me: '/api/users/me',
  },
  // Classes
  classes: {
    list: '/api/classes/',
    detail: (id: number) => `/api/classes/${id}`,
  },
  // Subjects
  subjects: {
    list: '/api/subjects/',
    detail: (id: number) => `/api/subjects/${id}`,
  },
  // Grades
  grades: {
    list: '/api/grades/',
    detail: (id: number) => `/api/grades/${id}`,
    student: (studentId: number) => `/api/grades/student/${studentId}`,
  },
  // Absences
  absences: {
    list: '/api/absences/',
    detail: (id: number) => `/api/absences/${id}`,
    student: (studentId: number) => `/api/absences/student/${studentId}`,
  },
  // Events
  events: {
    list: '/api/events/',
    detail: (id: number) => `/api/events/${id}`,
  },
  // Statistics
  statistics: {
    dashboard: '/api/statistics/dashboard',
    gradesDistribution: '/api/statistics/grades-distribution',
  },
  // Reports
  reports: {
    studentReport: (studentId: number) => `/api/reports/student/${studentId}`,
    classReport: (classId: number) => `/api/reports/class/${classId}`,
  },
  // Health
  health: '/health',
}

// Helper function to build full URL
export const buildURL = (endpoint: string): string => {
  // If endpoint already starts with http, return as is
  if (endpoint.startsWith('http')) {
    return endpoint
  }
  // Otherwise prepend base URL
  return `${API_URL}${endpoint}`
}

// Helper function to get auth headers
export const getAuthHeaders = (): HeadersInit => {
  const token = localStorage.getItem('accessToken')
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

export default API_CONFIG
