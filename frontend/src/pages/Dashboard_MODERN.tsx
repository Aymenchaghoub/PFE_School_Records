/**
 * Modernized Dashboard Page
 * Replace Dashboard.tsx with this file for the modern UI
 */
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { Users, GraduationCap, BookOpen, Calendar, LogOut, TrendingUp } from 'lucide-react'
import toast from 'react-hot-toast'
import { Button } from '../components/Button'
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card'
import { DashboardSkeleton } from '../components/LoadingSkeleton'

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
        setGrades(Array.isArray(g) ? g : [])
        setAbsences(Array.isArray(a) ? a : [])
      })
      .catch((err) => {
        console.error(err)
        const errorMsg = String(err?.message || err)
        setError(errorMsg)
        toast.error(`Failed to load dashboard: ${errorMsg}`)
      })
      .finally(() => setLoading(false))
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    toast.success('Logged out successfully')
    navigate('/login')
  }

  if (loading) {
    return <DashboardSkeleton />
  }

  const statCards = [
    {
      title: 'Students',
      value: stats?.total_students ?? 0,
      icon: Users,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10',
    },
    {
      title: 'Teachers',
      value: stats?.total_teachers ?? 0,
      icon: GraduationCap,
      color: 'text-green-400',
      bgColor: 'bg-green-500/10',
    },
    {
      title: 'Classes',
      value: stats?.total_classes ?? 0,
      icon: BookOpen,
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10',
    },
    {
      title: 'Absences',
      value: stats?.total_absences ?? 0,
      icon: Calendar,
      color: 'text-orange-400',
      bgColor: 'bg-orange-500/10',
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-950 text-slate-100 p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-violet to-purple-400 bg-clip-text text-transparent">
            School Dashboard
          </h1>
          {user && (
            <p className="text-slate-400 mt-1">
              Welcome back, <span className="text-slate-300 font-medium">{user.name}</span> 
              <span className="ml-2 text-xs px-2 py-1 rounded-full bg-violet/20 text-violet">
                {user.role}
              </span>
            </p>
          )}
        </div>

        <Button
          onClick={handleLogout}
          variant="secondary"
          size="md"
          className="sm:w-auto w-full"
        >
          <LogOut className="h-4 w-4 mr-2" />
          Logout
        </Button>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
          {error}
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {statCards.map((stat) => (
          <Card key={stat.title} hover className="group">
            <CardContent className="p-0">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-slate-400 mb-1">{stat.title}</p>
                  <p className="text-3xl font-bold group-hover:text-violet transition-colors">
                    {stat.value}
                  </p>
                </div>
                <div className={`${stat.bgColor} ${stat.color} p-3 rounded-lg`}>
                  <stat.icon className="h-6 w-6" />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Grades Distribution Chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-violet" />
                Grades Distribution
              </CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            {grades.length === 0 ? (
              <div className="h-64 flex items-center justify-center text-slate-400">
                <div className="text-center">
                  <BarChart className="h-16 w-16 mx-auto mb-4 opacity-20" />
                  <p>No grade data available</p>
                </div>
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={grades} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <XAxis dataKey="grade" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #475569',
                      borderRadius: '8px',
                    }}
                  />
                  <Bar dataKey="count" fill="#6A1B9A" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </CardContent>
        </Card>

        {/* Recent Absences Table */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-violet" />
              Latest Absences
            </CardTitle>
          </CardHeader>
          <CardContent>
            {absences.length === 0 ? (
              <div className="py-8 text-center text-slate-400">
                <Calendar className="h-12 w-12 mx-auto mb-3 opacity-20" />
                <p>No recent absences</p>
              </div>
            ) : (
              <div className="space-y-3 max-h-80 overflow-y-auto">
                {absences.slice(0, 8).map((absence) => (
                  <div
                    key={absence.id}
                    className="p-3 rounded-lg bg-slate-900/50 border border-slate-700/50 hover:border-slate-600 transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="font-medium text-slate-200">{absence.student_name}</p>
                        <p className="text-xs text-slate-400 mt-1">
                          {new Date(absence.date).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric',
                          })}
                        </p>
                      </div>
                    </div>
                    {absence.reason && (
                      <p className="text-sm text-slate-400 mt-2 line-clamp-2">{absence.reason}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard
