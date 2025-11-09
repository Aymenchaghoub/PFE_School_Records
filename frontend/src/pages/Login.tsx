import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { LogIn, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'
import { Button } from '../components/Button'
import { Input } from '../components/Input'
import { Card, CardHeader, CardTitle, CardContent } from '../components/Card'

interface User {
  id: number
  name: string
  email: string
  role: string
}

interface AuthResponse {
  access_token: string
  refresh_token?: string
  token_type: string
  user: User
}

const Login: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      if (!res.ok) {
        const text = await res.text()
        const errorMsg = `Login failed: ${text}`
        setError(errorMsg)
        toast.error(errorMsg)
        setLoading(false)
        return
      }

      const data: AuthResponse = await res.json()

      // Save tokens and user
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))

      // Show success message
      toast.success(`Welcome back, ${data.user.name}!`)

      // Navigate to dashboard
      setTimeout(() => navigate('/dashboard'), 500)
    } catch (err: any) {
      const errorMsg = err?.message || 'Network error. Please try again.'
      setError(errorMsg)
      toast.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <div className="flex items-center justify-center mb-2">
            <div className="h-12 w-12 rounded-full bg-violet/20 flex items-center justify-center">
              <LogIn className="h-6 w-6 text-violet" />
            </div>
          </div>
          <CardTitle className="text-center text-2xl">Welcome Back</CardTitle>
          <p className="text-center text-sm text-slate-400 mt-1">
            Sign in to your School Management account
          </p>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              type="email"
              label="Email Address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@school.com"
              required
              autoComplete="email"
            />

            <Input
              type="password"
              label="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              autoComplete="current-password"
            />

            {error && (
              <div className="flex items-start gap-2 p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                <AlertCircle className="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-400">{error}</p>
              </div>
            )}

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full"
              isLoading={loading}
              disabled={loading}
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>

            <div className="text-center text-sm text-slate-400 pt-2">
              <p>Demo credentials:</p>
              <p className="mt-1 font-mono text-xs">
                <span className="text-violet">admin@school.com</span> / <span className="text-violet">admin123</span>
              </p>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default Login
