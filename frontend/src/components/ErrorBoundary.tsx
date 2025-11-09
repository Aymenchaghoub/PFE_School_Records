/**
 * Error Boundary Component
 * Catches React errors and displays a fallback UI
 */
import { Component } from 'react'
import type { ReactNode, ErrorInfo } from 'react'
import toast from 'react-hot-toast'
import { AlertCircle, RefreshCw } from 'lucide-react'
import { Button } from './Button'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    }
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to console
    console.error('ErrorBoundary caught an error:', error, errorInfo)

    // Update state with error info
    this.setState({
      error,
      errorInfo,
    })

    // Show toast notification
    toast.error('Something went wrong. Please try refreshing the page.')

    // Send error to analytics (if enabled)
    if (import.meta.env.VITE_ENABLE_ERROR_REPORTING === 'true') {
      this.logErrorToService(error, errorInfo)
    }
  }

  logErrorToService = (error: Error, errorInfo: ErrorInfo) => {
    // You can integrate with error tracking services here
    // Example: Sentry, LogRocket, etc.
    const errorData = {
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href,
    }

    console.log('Error logged:', errorData)

    // Send to your error tracking service
    // Example: Sentry.captureException(error, { contexts: { react: errorInfo } })
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-b from-slate-900 to-slate-950">
          <div className="max-w-lg w-full bg-slate-800/60 backdrop-blur-sm border border-slate-700/50 rounded-xl p-8 text-center">
            <div className="flex justify-center mb-4">
              <div className="h-16 w-16 rounded-full bg-red-500/20 flex items-center justify-center">
                <AlertCircle className="h-8 w-8 text-red-400" />
              </div>
            </div>

            <h1 className="text-2xl font-bold text-slate-100 mb-2">
              Oops! Something went wrong
            </h1>

            <p className="text-slate-400 mb-6">
              We encountered an unexpected error. Don't worry, your data is safe.
            </p>

            {import.meta.env.MODE === 'development' && this.state.error && (
              <div className="mb-6 p-4 bg-slate-900/50 rounded-lg border border-slate-700">
                <p className="text-sm font-mono text-red-400 text-left mb-2">
                  {this.state.error.toString()}
                </p>
                {this.state.errorInfo && (
                  <details className="text-xs font-mono text-slate-500 text-left">
                    <summary className="cursor-pointer hover:text-slate-400">
                      View stack trace
                    </summary>
                    <pre className="mt-2 whitespace-pre-wrap overflow-auto max-h-40">
                      {this.state.errorInfo.componentStack}
                    </pre>
                  </details>
                )}
              </div>
            )}

            <div className="flex gap-3 justify-center">
              <Button
                onClick={this.handleReset}
                variant="secondary"
                size="md"
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Try Again
              </Button>

              <Button
                onClick={() => window.location.href = '/'}
                variant="primary"
                size="md"
              >
                Go Home
              </Button>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
