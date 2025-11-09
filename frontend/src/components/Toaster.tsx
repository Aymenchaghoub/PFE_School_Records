/**
 * Toast Notifications Provider
 * Uses react-hot-toast for modern toast notifications
 */
import { Toaster as HotToaster } from 'react-hot-toast'

export function Toaster() {
  return (
    <HotToaster
      position="top-right"
      toastOptions={{
        duration: 4000,
        style: {
          background: '#1e293b', // slate-800
          color: '#f1f5f9', // slate-100
          border: '1px solid #475569', // slate-600
          padding: '16px',
          borderRadius: '12px',
          fontSize: '14px',
        },
        success: {
          iconTheme: {
            primary: '#6A1B9A',
            secondary: '#fff',
          },
        },
        error: {
          iconTheme: {
            primary: '#ef4444',
            secondary: '#fff',
          },
        },
      }}
    />
  )
}
