import { Plus, Download } from 'lucide-react'
import DashboardLayout from '../layouts/DashboardLayout'
import GlassCard from '../components/ui/GlassCard'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'

const mockGrades = [
  { id: 1, student: 'Alice Johnson', subject: 'Mathematics', grade: 'A', score: 95, date: '2025-11-08' },
  { id: 2, student: 'Bob Smith', subject: 'Physics', grade: 'B+', score: 87, date: '2025-11-08' },
  { id: 3, student: 'Carol White', subject: 'English', grade: 'A-', score: 91, date: '2025-11-07' },
  { id: 4, student: 'David Brown', subject: 'Chemistry', grade: 'B', score: 83, date: '2025-11-07' },
  { id: 5, student: 'Emma Davis', subject: 'Mathematics', grade: 'A+', score: 98, date: '2025-11-06' },
]

const getGradeVariant = (grade: string) => {
  if (grade.startsWith('A')) return 'success'
  if (grade.startsWith('B')) return 'info'
  if (grade.startsWith('C')) return 'warning'
  return 'error'
}

export default function GradesPage() {
  return (
    <DashboardLayout>
      <div className="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Grades</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Track and manage student grades</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Add Grade
          </Button>
        </div>
      </div>

      <GlassCard className="p-6 bg-white dark:bg-gray-900">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Student</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Subject</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Score</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Grade</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Date</th>
                <th className="text-right py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Actions</th>
              </tr>
            </thead>
            <tbody>
              {mockGrades.map((grade) => (
                <tr key={grade.id} className="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                  <td className="py-4 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">{grade.student}</td>
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">{grade.subject}</td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-24 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-violet-500 to-violet-700 rounded-full"
                          style={{ width: `${grade.score}%` }}
                        />
                      </div>
                      <span className="text-sm text-gray-600 dark:text-gray-400">{grade.score}%</span>
                    </div>
                  </td>
                  <td className="py-4 px-4">
                    <Badge variant={getGradeVariant(grade.grade)}>{grade.grade}</Badge>
                  </td>
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">
                    {new Date(grade.date).toLocaleDateString()}
                  </td>
                  <td className="py-4 px-4 text-right">
                    <button className="text-sm font-medium text-violet-600 hover:text-violet-700 dark:text-violet-400">Edit</button>
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
