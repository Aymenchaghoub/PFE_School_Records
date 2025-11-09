import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import StudentsPage from './pages/StudentsPage'
import TeachersPage from './pages/TeachersPage'
import GradesPage from './pages/GradesPage'
import AbsencesPage from './pages/AbsencesPage'
import SettingsPage from './pages/SettingsPage'

function App() {
  return (
    <Router>
      <Toaster
        position="top-right"
        toastOptions={{
          className: 'dark:bg-gray-800 dark:text-white',
          duration: 3000,
          style: {
            background: '#1F2937',
            color: '#F9FAFB',
            borderRadius: '0.75rem',
          },
          success: {
            iconTheme: {
              primary: '#8E24AA',
              secondary: '#F9FAFB',
            },
          },
        }}
      />
      
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/students" element={<StudentsPage />} />
        <Route path="/teachers" element={<TeachersPage />} />
        <Route path="/grades" element={<GradesPage />} />
        <Route path="/absences" element={<AbsencesPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
