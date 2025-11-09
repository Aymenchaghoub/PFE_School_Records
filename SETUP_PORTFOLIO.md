# 🎨 Portfolio Setup Guide (Next.js)

## Quick Setup Script

If you want to create the Portfolio_Aymen project, run these commands:

```bash
# Create Portfolio directory
mkdir Portfolio_Aymen
cd Portfolio_Aymen

# Initialize Next.js project
npx create-next-app@latest . --typescript --tailwind --app --src-dir --import-alias "@/*"

# Install additional dependencies
npm install lucide-react framer-motion @vercel/analytics

# Create GitHub Actions workflow for auto-sync
mkdir -p .github/workflows
```

## GitHub Actions Auto-Sync Configuration

Create `.github/workflows/sync.yml`:

```yaml
name: Sync Portfolio Data

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          
      - name: Fetch GitHub Stats
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Fetch repository data
          curl -H "Authorization: token $GITHUB_TOKEN" \
            https://api.github.com/users/Aymenchaghoub/repos \
            > public/repos.json
            
      - name: Build and Export
        run: |
          npm ci
          npm run build
          
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./
```

## Vercel Deployment

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```

3. **Get deployment credentials**:
   ```bash
   vercel link
   # This will create .vercel/project.json with IDs
   ```

4. **Add secrets to GitHub**:
   - Go to repository settings → Secrets
   - Add: `VERCEL_TOKEN`, `ORG_ID`, `PROJECT_ID`

## Portfolio Structure

```
Portfolio_Aymen/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── projects/
│   │   ├── about/
│   │   └── contact/
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── ProjectCard.tsx
│   │   └── SkillBadge.tsx
│   └── lib/
│       ├── github.ts
│       └── analytics.ts
├── public/
├── .github/workflows/
├── package.json
└── next.config.js
```

## Sample Homepage Component

```typescript
// src/app/page.tsx
export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-950">
      <div className="container mx-auto px-4 py-16">
        <h1 className="text-5xl font-bold text-white mb-4">
          Aymen Chaghoub
        </h1>
        <p className="text-xl text-gray-300 mb-8">
          L3 Informatique | Université de Lille
        </p>
        
        <section className="grid md:grid-cols-2 gap-8 mt-12">
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-2xl font-semibold text-white mb-4">
              School Records System
            </h2>
            <p className="text-gray-400">
              Full-stack application with FastAPI, React, and MySQL
            </p>
            <a href="https://github.com/Aymenchaghoub/PFE_School_Records" 
               className="text-blue-400 hover:text-blue-300 mt-4 inline-block">
              View on GitHub →
            </a>
          </div>
        </section>
      </div>
    </main>
  )
}
```

## Environment Variables

Create `.env.local`:
```env
NEXT_PUBLIC_GITHUB_USERNAME=Aymenchaghoub
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
```

## Deploy Command

```bash
# Build and deploy to Vercel
npm run build && vercel --prod
```

---

**Note**: This is optional. Your School Records System is already deployed and working!
