import { useState } from 'react'
import { Plus, Search, Filter } from 'lucide-react'
import DashboardLayout from '../layouts/DashboardLayout'
import GlassCard from '../components/ui/GlassCard'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'

const mockStudents = [
  { id: 1, name: 'Alice Johnson', email: 'alice@example.com', class: '10-A', grade: 'A', status: 'active' },
  { id: 2, name: 'Bob Smith', email: 'bob@example.com', class: '10-B', grade: 'B+', status: 'active' },
  { id: 3, name: 'Carol White', email: 'carol@example.com', class: '9-A', grade: 'A-', status: 'active' },
  { id: 4, name: 'David Brown', email: 'david@example.com', class: '11-C', grade: 'B', status: 'inactive' },
  { id: 5, name: 'Emma Davis', email: 'emma@example.com', class: '10-A', grade: 'A+', status: 'active' },
]

export default function StudentsPage() {
  const [searchTerm, setSearchTerm] = useState('')

  return (
    <DashboardLayout>
      {/* Page Header */}
      <div className="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Students</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Manage student profiles and information
          </p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Student
        </Button>
      </div>

      {/* Filters */}
      <GlassCard className="p-4 mb-6 bg-white dark:bg-gray-900">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search students..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full h-11 pl-11 pr-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-violet-500"
            />
          </div>
          <Button variant="outline">
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </Button>
        </div>
      </GlassCard>

      {/* Students Table */}
      <GlassCard className="p-6 bg-white dark:bg-gray-900">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Name
                </th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Email
                </th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Class
                </th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Grade
                </th>
                <th className="text-left py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Status
                </th>
                <th className="text-right py-4 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {mockStudents
                .filter((student) =>
                  student.name.toLowerCase().includes(searchTerm.toLowerCase())
                )
                .map((student) => (
                  <tr
                    key={student.id}
                    className="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                  >
                    <td className="py-4 px-4">
                      <div className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-violet-500 to-violet-700 flex items-center justify-center text-white font-semibold text-sm">
                          {student.name.charAt(0)}
                        </div>
                        <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {student.name}
                        </span>
                      </div>
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">
                      {student.email}
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-600 dark:text-gray-400">
                      {student.class}
                    </td>
                    <td className="py-4 px-4">
                      <Badge variant="info">{student.grade}</Badge>
                    </td>
                    <td className="py-4 px-4">
                      <Badge variant={student.status === 'active' ? 'success' : 'default'}>
                        {student.status}
                      </Badge>
                    </td>
                    <td className="py-4 px-4 text-right">
                      <button className="text-sm font-medium text-violet-600 hover:text-violet-700 dark:text-violet-400">
                        View
                      </button>
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
