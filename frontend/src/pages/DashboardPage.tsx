import { Users, GraduationCap, BookOpen, TrendingUp } from 'lucide-react'
import DashboardLayout from '../layouts/DashboardLayout'
import StatCard from '../components/ui/StatCard'
import GlassCard from '../components/ui/GlassCard'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'

const statsData = [
  {
    title: 'Total Students',
    value: '1,234',
    icon: Users,
    trend: { value: '+12.5%', isPositive: true },
  },
  {
    title: 'Total Teachers',
    value: '87',
    icon: GraduationCap,
    trend: { value: '+3.2%', isPositive: true },
  },
  {
    title: 'Avg Grade',
    value: '85.4',
    icon: BookOpen,
    trend: { value: '-2.1%', isPositive: false },
  },
  {
    title: 'Attendance Rate',
    value: '94.2%',
    icon: TrendingUp,
    trend: { value: '+5.7%', isPositive: true },
  },
]

const gradesData = [
  { subject: 'Math', average: 85 },
  { subject: 'Science', average: 78 },
  { subject: 'English', average: 92 },
  { subject: 'History', average: 88 },
  { subject: 'Art', average: 95 },
]

const attendanceData = [
  { month: 'Jan', rate: 92 },
  { month: 'Feb', rate: 88 },
  { month: 'Mar', rate: 95 },
  { month: 'Apr', rate: 90 },
  { month: 'May', rate: 94 },
  { month: 'Jun', rate: 91 },
]

const recentGrades = [
  { student: 'Alice Johnson', subject: 'Mathematics', grade: 'A', date: '2025-11-08' },
  { student: 'Bob Smith', subject: 'Physics', grade: 'B+', date: '2025-11-08' },
  { student: 'Carol White', subject: 'English', grade: 'A-', date: '2025-11-07' },
  { student: 'David Brown', subject: 'Chemistry', grade: 'B', date: '2025-11-07' },
]

export default function DashboardPage() {
  return (
    <DashboardLayout>
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Welcome back! Here's what's happening today.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        {statsData.map((stat) => (
          <StatCard key={stat.title} {...stat} />
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Grades Chart */}
        <GlassCard className="p-6 bg-white dark:bg-gray-900">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Average Grades by Subject
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={gradesData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
              <XAxis dataKey="subject" stroke="#9CA3AF" fontSize={12} />
              <YAxis stroke="#9CA3AF" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1F2937',
                  border: 'none',
                  borderRadius: '0.75rem',
                  color: '#F3F4F6',
                }}
              />
              <Bar dataKey="average" fill="#8E24AA" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </GlassCard>

        {/* Attendance Trend */}
        <GlassCard className="p-6 bg-white dark:bg-gray-900">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Attendance Trend
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={attendanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.1} />
              <XAxis dataKey="month" stroke="#9CA3AF" fontSize={12} />
              <YAxis stroke="#9CA3AF" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1F2937',
                  border: 'none',
                  borderRadius: '0.75rem',
                  color: '#F3F4F6',
                }}
              />
              <Line
                type="monotone"
                dataKey="rate"
                stroke="#8E24AA"
                strokeWidth={3}
                dot={{ fill: '#8E24AA', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </GlassCard>
      </div>

      {/* Recent Activity */}
      <GlassCard className="p-6 bg-white dark:bg-gray-900">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Recent Grades
          </h3>
          <button className="text-sm font-medium text-violet-600 hover:text-violet-700 dark:text-violet-400">
            View All
          </button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Student
                </th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Subject
                </th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Grade
                </th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Date
                </th>
              </tr>
            </thead>
            <tbody>
              {recentGrades.map((grade, index) => (
                <tr
                  key={index}
                  className="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                >
                  <td className="py-4 px-4 text-sm text-gray-900 dark:text-gray-100">
                    {grade.student}
                  </td>
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">
                    {grade.subject}
                  </td>
                  <td className="py-4 px-4">
                    <span className="inline-flex items-center rounded-full bg-violet-100 dark:bg-violet-900/30 px-3 py-1 text-sm font-semibold text-violet-700 dark:text-violet-400">
                      {grade.grade}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">
                    {new Date(grade.date).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>
    </DashboardLayout>
  )
}
