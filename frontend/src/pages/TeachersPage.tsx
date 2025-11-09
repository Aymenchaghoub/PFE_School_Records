import { Plus, Search } from 'lucide-react'
import DashboardLayout from '../layouts/DashboardLayout'
import GlassCard from '../components/ui/GlassCard'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'

const mockTeachers = [
  { id: 1, name: 'Dr. John Smith', email: 'john@school.com', subject: 'Mathematics', students: 45, status: 'active' },
  { id: 2, name: 'Ms. Sarah Johnson', email: 'sarah@school.com', subject: 'English', students: 38, status: 'active' },
  { id: 3, name: 'Prof. Michael Brown', email: 'michael@school.com', subject: 'Physics', students: 32, status: 'active' },
  { id: 4, name: 'Dr. Emily Davis', email: 'emily@school.com', subject: 'Chemistry', students: 29, status: 'inactive' },
]

export default function TeachersPage() {
  return (
    <DashboardLayout>
      <div className="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Teachers</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">Manage teaching staff</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Teacher
        </Button>
      </div>

      <GlassCard className="p-4 mb-6 bg-white dark:bg-gray-900">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search teachers..."
            className="w-full h-11 pl-11 pr-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
          />
        </div>
      </GlassCard>

      <GlassCard className="p-6 bg-white dark:bg-gray-900">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Name</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Email</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Subject</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Students</th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Status</th>
                <th className="text-right py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Actions</th>
              </tr>
            </thead>
            <tbody>
              {mockTeachers.map((teacher) => (
                <tr key={teacher.id} className="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-gradient-to-br from-violet-500 to-violet-700 flex items-center justify-center text-white font-semibold text-sm">
                        {teacher.name.split(' ')[0].charAt(0)}{teacher.name.split(' ')[1]?.charAt(0)}
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100">{teacher.name}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">{teacher.email}</td>
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">{teacher.subject}</td>
                  <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">{teacher.students}</td>
                  <td className="py-4 px-4">
                    <Badge variant={teacher.status === 'active' ? 'success' : 'default'}>{teacher.status}</Badge>
                  </td>
                  <td className="py-4 px-4 text-right">
                    <button className="text-sm font-medium text-violet-600 hover:text-violet-700 dark:text-violet-400">View</button>
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
