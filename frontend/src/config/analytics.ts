/**
 * Analytics Integration
 * Supports Plausible and Google Analytics (GA4)
 */

// interface AnalyticsEvent {
//   name: string
//   properties?: Record<string, string | number | boolean>
// }

class Analytics {
  private enabled: boolean
  private provider: 'plausible' | 'google-analytics' | null
  private analyticsId: string | null

  constructor() {
    this.enabled = import.meta.env.VITE_ENABLE_ANALYTICS === 'true'
    this.provider = import.meta.env.VITE_ANALYTICS_PROVIDER || null
    this.analyticsId = import.meta.env.VITE_ANALYTICS_ID || null

    if (this.enabled && this.analyticsId) {
      this.initialize()
    }
  }

  private initialize() {
    if (!this.provider || !this.analyticsId) {
      console.warn('Analytics enabled but provider or ID not configured')
      return
    }

    switch (this.provider) {
      case 'plausible':
        this.initializePlausible()
        break
      case 'google-analytics':
        this.initializeGoogleAnalytics()
        break
      default:
        console.warn(`Unknown analytics provider: ${this.provider}`)
    }
  }

  private initializePlausible() {
    // Create and append Plausible script
    const script = document.createElement('script')
    script.defer = true
    script.dataset.domain = window.location.hostname
    script.src = 'https://plausible.io/js/script.js'
    
    document.head.appendChild(script)
    
    console.log('✅ Plausible analytics initialized')
  }

  private initializeGoogleAnalytics() {
    if (!this.analyticsId) return

    // Load Google Analytics gtag.js
    const script1 = document.createElement('script')
    script1.async = true
    script1.src = `https://www.googletagmanager.com/gtag/js?id=${this.analyticsId}`
    document.head.appendChild(script1)

    // Initialize gtag
    const script2 = document.createElement('script')
    script2.innerHTML = `
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '${this.analyticsId}', {
        page_path: window.location.pathname,
      });
    `
    document.head.appendChild(script2)

    console.log('✅ Google Analytics initialized')
  }

  /**
   * Track a page view
   */
  pageView(path?: string) {
    if (!this.enabled) return

    const url = path || window.location.pathname

    if (this.provider === 'plausible') {
      // Plausible automatically tracks page views
      // Manual tracking: window.plausible('pageview', { props: { path: url } })
    } else if (this.provider === 'google-analytics' && window.gtag) {
      window.gtag('config', this.analyticsId!, {
        page_path: url,
      })
    }
  }

  /**
   * Track a custom event
   */
  event(name: string, properties?: Record<string, string | number | boolean>) {
    if (!this.enabled) return

    if (this.provider === 'plausible' && window.plausible) {
      window.plausible(name, { props: properties })
    } else if (this.provider === 'google-analytics' && window.gtag) {
      window.gtag('event', name, properties)
    }

    console.log('📊 Analytics event:', name, properties)
  }

  /**
   * Track an error
   */
  error(error: Error, context?: Record<string, unknown>) {
    if (!this.enabled) return

    this.event('error', {
      error_message: error.message,
      error_stack: error.stack?.substring(0, 150) || '',
      ...context,
    })
  }
}

// Augment window object for TypeScript
declare global {
  interface Window {
    plausible?: (event: string, options?: { props?: Record<string, unknown> }) => void
    gtag?: (...args: unknown[]) => void
    dataLayer?: unknown[]
  }
}

// Export singleton instance
export const analytics = new Analytics()

// Export helper functions
export const trackPageView = (path?: string) => analytics.pageView(path)
export const trackEvent = (name: string, properties?: Record<string, string | number | boolean>) => 
  analytics.event(name, properties)
export const trackError = (error: Error, context?: Record<string, unknown>) => 
  analytics.error(error, context)
