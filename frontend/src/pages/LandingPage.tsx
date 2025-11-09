import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowRight, Users, BookOpen, BarChart3, Shield, Zap, Clock } from 'lucide-react'
import LandingLayout from '../layouts/LandingLayout'
import Button from '../components/ui/Button'
import GlassCard from '../components/ui/GlassCard'

export default function LandingPage() {
  const features = [
    {
      icon: Users,
      title: 'Student Management',
      description: 'Comprehensive student profiles with grades, attendance, and performance tracking.',
    },
    {
      icon: BookOpen,
      title: 'Grade Tracking',
      description: 'Real-time grade management with detailed analytics and reporting capabilities.',
    },
    {
      icon: BarChart3,
      title: 'Smart Analytics',
      description: 'Visual insights and data-driven decisions with advanced analytics dashboards.',
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Enterprise-grade security with role-based access control and data encryption.',
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Built with modern tech stack for blazing-fast performance and responsiveness.',
    },
    {
      icon: Clock,
      title: 'Real-time Updates',
      description: 'Instant notifications and live updates for attendance, grades, and events.',
    },
  ]

  return (
    <LandingLayout>
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 sm:py-32">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-4xl text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
                <span className="block text-gray-900 dark:text-white">Empowering Education</span>
                <span className="block mt-2 bg-gradient-to-r from-violet-600 to-pink-600 bg-clip-text text-transparent">
                  with Smart Digital Tools
                </span>
              </h1>
              
              <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
                Transform your school management with our modern, intuitive platform. Track grades, attendance, and performance all in one place.
              </p>

              <div className="mt-10 flex items-center justify-center gap-4">
                <Link to="/login">
                  <Button size="lg" className="group">
                    Get Started
                    <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                  </Button>
                </Link>
                <Link to="/login">
                  <Button variant="outline" size="lg">
                    View Demo
                  </Button>
                </Link>
              </div>
            </motion.div>

            {/* Floating dashboard preview */}
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="mt-16 relative"
            >
              <div className="relative mx-auto max-w-5xl">
                <div className="absolute inset-0 bg-gradient-to-r from-violet-600/20 to-pink-600/20 blur-3xl" />
                <img
                  src="/dashboard-preview.png"
                  alt="Dashboard Preview"
                  className="relative rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-800"
                  onError={(e) => {
                    // Fallback to gradient placeholder if image doesn't exist
                    e.currentTarget.style.display = 'none'
                    e.currentTarget.parentElement!.innerHTML += '<div class="relative rounded-2xl h-96 bg-gradient-to-br from-violet-100 to-pink-100 dark:from-violet-900/20 dark:to-pink-900/20 flex items-center justify-center"><p class="text-gray-500 dark:text-gray-400">Dashboard Preview</p></div>'
                  }}
                />
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 bg-white/50 dark:bg-gray-900/50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Everything you need to manage your school
            </h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              Powerful features designed for modern education management
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <GlassCard className="p-6 h-full">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-violet-100 dark:bg-violet-900/30 text-violet-600 dark:text-violet-400 mb-4">
                      <Icon className="h-6 w-6" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      {feature.description}
                    </p>
                  </GlassCard>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-violet-600 to-violet-800 px-6 py-16 shadow-2xl sm:px-12 sm:py-20">
            <div className="relative mx-auto max-w-2xl text-center">
              <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                Ready to transform your school management?
              </h2>
              <p className="mt-6 text-lg leading-8 text-violet-100">
                Join thousands of schools already using our platform to streamline their operations.
              </p>
              <div className="mt-10 flex items-center justify-center gap-4">
                <Link to="/login">
                  <Button
                    size="lg"
                    variant="secondary"
                    className="bg-white text-violet-700 hover:bg-gray-50"
                  >
                    Start Free Trial
                  </Button>
                </Link>
                <Link to="/login">
                  <Button
                    size="lg"
                    variant="outline"
                    className="border-white text-white hover:bg-white/10"
                  >
                    Contact Sales
                  </Button>
                </Link>
              </div>
            </div>

            {/* Decorative elements */}
            <div className="absolute top-0 left-0 -translate-x-1/2 -translate-y-1/2 h-64 w-64 rounded-full bg-white/10 blur-3xl" />
            <div className="absolute bottom-0 right-0 translate-x-1/2 translate-y-1/2 h-64 w-64 rounded-full bg-white/10 blur-3xl" />
          </div>
        </div>
      </section>
    </LandingLayout>
  )
}
