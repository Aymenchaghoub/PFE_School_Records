import { type ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { Github } from 'lucide-react'
import Button from '../components/ui/Button'

interface LandingLayoutProps {
  children: ReactNode
}

export default function LandingLayout({ children }: LandingLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-violet-50 dark:from-gray-950 dark:via-gray-900 dark:to-violet-950">
      {/* Header */}
      <header className="fixed top-0 w-full z-50 border-b border-gray-200/50 dark:border-gray-800/50 backdrop-blur-xl bg-white/70 dark:bg-gray-900/70">
        <nav className="container mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-violet-600 to-violet-800 flex items-center justify-center">
              <span className="text-white font-bold text-sm">SR</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-violet-600 to-violet-800 bg-clip-text text-transparent">
              School Records
            </span>
          </Link>

          <div className="flex items-center gap-4">
            <Link to="/login">
              <Button variant="outline" size="sm">Sign In</Button>
            </Link>
            <Link to="/login">
              <Button size="sm">Get Started</Button>
            </Link>
          </div>
        </nav>
      </header>

      {/* Main content */}
      <main className="pt-16">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-800 bg-white/50 dark:bg-gray-900/50 backdrop-blur-xl">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center gap-2 mb-4">
                <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-violet-600 to-violet-800 flex items-center justify-center">
                  <span className="text-white font-bold text-sm">SR</span>
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-violet-600 to-violet-800 bg-clip-text text-transparent">
                  School Records
                </span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 max-w-sm">
                Empowering education with smart digital tools. Modern school management made simple.
              </p>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Product</h3>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><Link to="#features" className="hover:text-violet-600">Features</Link></li>
                <li><Link to="#pricing" className="hover:text-violet-600">Pricing</Link></li>
                <li><Link to="#docs" className="hover:text-violet-600">Documentation</Link></li>
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Company</h3>
              <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <li><Link to="#about" className="hover:text-violet-600">About</Link></li>
                <li>
                  <a
                    href="https://github.com/Aymenchaghoub/PFE_School_Records"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 hover:text-violet-600"
                  >
                    <Github className="h-4 w-4" />
                    GitHub
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-800 text-center text-sm text-gray-600 dark:text-gray-400">
            <p>© 2025 School Records Management System. Built by Aymen Chaghoub.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
