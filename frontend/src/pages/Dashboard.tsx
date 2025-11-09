import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import '../index.css'

interface User {
  id: number
  name: string
  email: string
  role: string
}

interface DashboardStats {
  total_students: number
  total_teachers: number
  total_classes: number
  total_absences: number
}

interface GradeBucket {
  grade: string
  count: number
}

interface AbsenceItem {
  id: number
  student_name: string
  date: string
  reason?: string
}

// const COLORS = ['#6A1B9A', '#8E24AA', '#AB47BC', '#CE93D8', '#E1BEE7']

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<User | null>(null)
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [grades, setGrades] = useState<GradeBucket[]>([])
  const [absences, setAbsences] = useState<AbsenceItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const userJson = localStorage.getItem('user')
    if (!token || !userJson) {
      navigate('/login')
      return
    }

    try {
      setUser(JSON.parse(userJson))
    } catch (e) {
      localStorage.removeItem('user')
      navigate('/login')
      return
    }

    const base = import.meta.env.VITE_API_URL || ''
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const fetchStats = fetch(`${base}/api/statistics/dashboard`, { headers })
    const fetchGrades = fetch(`${base}/api/statistics/grades-distribution`, { headers })
    const fetchAbsences = fetch(`${base}/api/absences/`, { headers })

    setLoading(true)

    Promise.all([fetchStats, fetchGrades, fetchAbsences])
      .then(async ([r1, r2, r3]) => {
        if (!r1.ok) throw new Error(`Stats fetch failed: ${r1.status}`)
        if (!r2.ok) throw new Error(`Grades fetch failed: ${r2.status}`)
        if (!r3.ok) throw new Error(`Absences fetch failed: ${r3.status}`)

        const s = await r1.json()
        const g = await r2.json()
        const a = await r3.json()

        setStats(s)
        // Expecting grades array like [{grade: 'A', count: 12}, ...]
        setGrades(Array.isArray(g) ? g : [])
        // Expecting absences array
        setAbsences(Array.isArray(a) ? a : [])
      })
      .catch((err) => {
        console.error(err)
        setError(String(err?.message || err))
      })
      .finally(() => setLoading(false))
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  if (loading) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <div className="flex items-center justify-center">
            <svg className="animate-spin h-8 w-8 text-[var(--violet)]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
            </svg>
          </div>
          <p className="mt-4 text-center">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard-root">
      <div className="topbar">
        <div className="logo">School Dashboard</div>
        <div className="flex items-center gap-4">
          {user && (
            <div className="text-sm text-slate-300">
              {user.name} <span className="ml-2 text-slate-400">({user.role})</span>
            </div>
          )}
          <button onClick={handleLogout} className="px-3 py-2 rounded-md bg-slate-700 text-sm">Logout</button>
        </div>
      </div>

      {error && <div className="mb-4 text-red-300">{error}</div>}

      <div className="stats-grid">
        <div className="stat-card">
          <div className="text-sm text-slate-400">Students</div>
          <div className="text-2xl font-bold">{stats?.total_students ?? '—'}</div>
        </div>
        <div className="stat-card">
          <div className="text-sm text-slate-400">Teachers</div>
          <div className="text-2xl font-bold">{stats?.total_teachers ?? '—'}</div>
        </div>
        <div className="stat-card">
          <div className="text-sm text-slate-400">Classes</div>
          <div className="text-2xl font-bold">{stats?.total_classes ?? '—'}</div>
        </div>
        <div className="stat-card">
          <div className="text-sm text-slate-400">Absences</div>
          <div className="text-2xl font-bold">{stats?.total_absences ?? '—'}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="col-span-2 chart-card">
          <h3 className="text-lg font-semibold mb-2">Grades distribution</h3>
          {grades.length === 0 ? (
            <div className="text-slate-400">No grade data available</div>
          ) : (
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={grades} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <XAxis dataKey="grade" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip />
                <Bar dataKey="count" fill="#6A1B9A" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="chart-card">
          <h3 className="text-lg font-semibold mb-2">Latest absences</h3>
          {absences.length === 0 ? (
            <div className="text-slate-400">No recent absences</div>
          ) : (
            <div className="overflow-auto" style={{ maxHeight: 300 }}>
              <table className="table">
                <thead>
                  <tr>
                    <th className="py-2">Student</th>
                    <th className="py-2">Date</th>
                    <th className="py-2">Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {absences.slice(0, 8).map((a) => (
                    <tr key={a.id} className="border-t border-slate-700">
                      <td className="py-2">{a.student_name}</td>
                      <td className="py-2">{new Date(a.date).toLocaleDateString()}</td>
                      <td className="py-2">{a.reason ?? '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
