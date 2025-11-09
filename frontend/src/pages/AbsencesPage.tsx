import { Plus } from 'lucide-react'
import DashboardLayout from '../layouts/DashboardLayout'
import GlassCard from '../components/ui/GlassCard'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'

const mockAbsences = [
  { id: 1, student: 'Alice Johnson', date: '2025-11-08', reason: 'Medical', status: 'Excused' },
  { id: 2, student: 'Bob Smith', date: '2025-11-07', reason: 'Personal', status: 'Unexcused' },
  { id: 3, student: 'Carol White', date: '2025-11-06', reason: 'Medical', status: 'Excused' },
  { id: 4, student: 'David Brown', date: '2025-11-05', reason: 'Unknown', status: 'Pending' },
]

export default function AbsencesPage() {
  return (
    <DashboardLayout>
      <div className="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Absences</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Track student attendance</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Record Absence
        </Button>
      </div>

      <GlassCard className="p-6 bg-white dark:bg-gray-900">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Student</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Date</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Reason</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Status</th>
                <th className="text-right py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Actions</th>
              </tr>
            </thead>
            <tbody>
              {mockAbsences.map((absence) => (
                <tr key={absence.id} className="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-gradient-to-br from-violet-500 to-violet-700 flex items-center justify-center text-white font-semibold text-sm">
                        {absence.student.charAt(0)}
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{absence.student}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">
                    {new Date(absence.date).toLocaleDateString()}
                  </td>
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">{absence.reason}</td>
                  <td className="py-4 px-4">
                    <Badge
                      variant={
                        absence.status === 'Excused' ? 'success' :
                        absence.status === 'Pending' ? 'warning' : 'error'
                      }
                    >
                      {absence.status}
                    </Badge>
                  </td>
                  <td className="py-4 px-4 text-right">
                    <button className="text-sm font-medium text-violet-600 hover:text-violet-700 dark:text-violet-400">Review</button>
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
