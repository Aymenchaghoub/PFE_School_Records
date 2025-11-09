import DashboardLayout from '../layouts/DashboardLayout'
import GlassCard from '../components/ui/GlassCard'
import Button from '../components/ui/Button'
import DarkModeToggle from '../components/ui/DarkModeToggle'

export default function SettingsPage() {
  return (
    <DashboardLayout>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">Manage your account and preferences</p>
      </div>

      <div className="space-y-6">
        {/* Profile Settings */}
        <GlassCard className="p-6 bg-white dark:bg-gray-900">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Profile Settings</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Full Name
              </label>
              <input
                type="text"
                defaultValue="Aymen Chaghoub"
                className="w-full h-11 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email
              </label>
              <input
                type="email"
                defaultValue="aymen@school.com"
                className="w-full h-11 px-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </div>
            <div>
              <Button>Save Changes</Button>
            </div>
          </div>
        </GlassCard>

        {/* Appearance */}
        <GlassCard className="p-6 bg-white dark:bg-gray-900">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Appearance</h3>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-gray-900 dark:text-white">Dark Mode</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">Toggle dark mode on/off</p>
            </div>
            <DarkModeToggle />
          </div>
        </GlassCard>

        {/* Notifications */}
        <GlassCard className="p-6 bg-white dark:bg-gray-900">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Notifications</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900 dark:text-white">Email Notifications</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Receive email updates</p>
              </div>
              <input type="checkbox" defaultChecked className="h-5 w-5 rounded border-gray-300 text-violet-600 focus:ring-violet-500" />
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-gray-900 dark:text-white">Push Notifications</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Receive push notifications</p>
              </div>
              <input type="checkbox" defaultChecked className="h-5 w-5 rounded border-gray-300 text-violet-600 focus:ring-violet-500" />
            </div>
          </div>
        </GlassCard>

        {/* Security */}
        <GlassCard className="p-6 bg-white dark:bg-gray-900">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Security</h3>
          <div className="space-y-4">
            <Button variant="outline">Change Password</Button>
            <Button variant="outline">Two-Factor Authentication</Button>
          </div>
        </GlassCard>
      </div>
    </DashboardLayout>
  )
}
