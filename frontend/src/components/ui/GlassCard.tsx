import { type HTMLAttributes, forwardRef } from 'react'
import { cn } from '../../config/utils'
import { motion } from 'framer-motion'

export interface GlassCardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean
}

const GlassCard = forwardRef<HTMLDivElement, GlassCardProps>(
  ({ className, hover = true, children, ...props }, ref) => {
    const baseStyles = 'backdrop-blur-xl bg-white/10 dark:bg-black/10 border border-white/20 dark:border-white/10 rounded-2xl shadow-glass'
    const hoverStyles = hover ? 'hover:shadow-glass-lg hover:bg-white/15 dark:hover:bg-black/15 transition-all duration-300' : ''

    return (
      <motion.div
        ref={ref}
        className={cn(baseStyles, hoverStyles, className)}
        onClick={props.onClick}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        {children}
      </motion.div>
    )
  }
)

GlassCard.displayName = 'GlassCard'

export default GlassCard
