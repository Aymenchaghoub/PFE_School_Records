import { cn } from '../../config/utils'
import { type LucideIcon } from 'lucide-react'

interface StatCardProps {
  title: string
  value: string | number
  icon: LucideIcon
  trend?: {
    value: string
    isPositive: boolean
  }
  className?: string
}

export default function StatCard({ title, value, icon: Icon, trend, className }: StatCardProps) {
  return (
    <div
      className={cn(
        'group relative overflow-hidden rounded-2xl bg-white dark:bg-gray-900 p-6 shadow-lg border border-gray-100 dark:border-gray-800',
        'hover:shadow-violet hover:border-violet-500/50 transition-all duration-300',
        className
      )}
    >
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="relative flex items-center justify-between">
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white">{value}</p>
          
          {trend && (
            <div className={cn('flex items-center text-sm font-medium', trend.isPositive ? 'text-green-600' : 'text-red-600')}>
              <span>{trend.isPositive ? '↑' : '↓'}</span>
              <span className="ml-1">{trend.value}</span>
            </div>
          )}
        </div>
        
        <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-violet-100 dark:bg-violet-900/30 text-violet-600 dark:text-violet-400 group-hover:scale-110 transition-transform duration-300">
          <Icon className="h-7 w-7" />
        </div>
      </div>
    </div>
  )
}
