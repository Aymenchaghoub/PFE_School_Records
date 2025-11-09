/**
 * Modern Card Component
 * Reusable card container with consistent styling
 */
import type { HTMLAttributes, ReactNode } from 'react'
import { cn } from '../config/utils'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
  hover?: boolean
}

export function Card({ children, hover = false, className, ...props }: CardProps) {
  return (
    <div
      className={cn(
        'bg-slate-800/60 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6 shadow-lg',
        hover && 'transition-all hover:shadow-xl hover:border-slate-600 hover:-translate-y-0.5',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

interface CardHeaderProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
}

export function CardHeader({ children, className, ...props }: CardHeaderProps) {
  return (
    <div className={cn('mb-4', className)} {...props}>
      {children}
    </div>
  )
}

interface CardTitleProps extends HTMLAttributes<HTMLHeadingElement> {
  children: ReactNode
}

export function CardTitle({ children, className, ...props }: CardTitleProps) {
  return (
    <h3 className={cn('text-lg font-semibold text-slate-100', className)} {...props}>
      {children}
    </h3>
  )
}

interface CardContentProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
}

export function CardContent({ children, className, ...props }: CardContentProps) {
  return (
    <div className={cn('text-slate-300', className)} {...props}>
      {children}
    </div>
  )
}
