/**
 * Loading Skeleton Components
 * For better loading UX with skeleton screens
 */
import { cn } from '../config/utils'

interface SkeletonProps {
  className?: string
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn(
        'animate-pulse rounded-md bg-slate-700/50',
        className
      )}
      aria-live="polite"
      aria-busy="true"
    />
  )
}

export function StatCardSkeleton() {
  return (
    <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-6">
      <Skeleton className="h-4 w-20 mb-3" />
      <Skeleton className="h-8 w-16" />
    </div>
  )
}

export function DashboardSkeleton() {
  return (
    <div className="dashboard-root">
      <div className="topbar">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-10 w-24" />
      </div>

      <div className="stats-grid">
        <StatCardSkeleton />
        <StatCardSkeleton />
        <StatCardSkeleton />
        <StatCardSkeleton />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="col-span-2 chart-card">
          <Skeleton className="h-6 w-48 mb-4" />
          <Skeleton className="h-64 w-full" />
        </div>
        <div className="chart-card">
          <Skeleton className="h-6 w-32 mb-4" />
          <div className="space-y-3">
            <Skeleton className="h-12 w-full" />
            <Skeleton className="h-12 w-full" />
            <Skeleton className="h-12 w-full" />
          </div>
        </div>
      </div>
    </div>
  )
}
