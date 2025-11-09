# 🎨 Portfolio Website Setup Guide - Phase 9

Complete guide for creating Aymen Chaghoub's Portfolio Website with Next.js 15

---

## 📋 Quick Start

### 1. Create Next.js Project

```powershell
# Navigate to Desktop
cd C:\Users\Aymen\Desktop

# Create Next.js 15 App Router project
npx create-next-app@latest Portfolio_Aymen --typescript --tailwind --eslint --app

# Prompts (select these options):
# ✓ Would you like to use TypeScript? Yes
# ✓ Would you like to use ESLint? Yes
# ✓ Would you like to use Tailwind CSS? Yes
# ✓ Would you like to use `src/` directory? No
# ✓ Would you like to use App Router? Yes
# ✓ Would you like to customize the default import alias? No

# Navigate to project
cd Portfolio_Aymen
```

---

## 📦 Install Dependencies

```powershell
# Install required packages
npm install framer-motion lucide-react react-hot-toast emailjs-com clsx tailwind-merge

# Install development dependencies
npm install -D @types/node
```

**Dependencies Installed:**
- `framer-motion` - Animations
- `lucide-react` - Icons (200+ beautiful icons)
- `react-hot-toast` - Toast notifications
- `emailjs-com` - Email service for contact form
- `clsx` - Conditional classNames
- `tailwind-merge` - Merge Tailwind classes

---

## 🏗️ Project Structure

Create this folder structure:

```
Portfolio_Aymen/
├── app/
│   ├── layout.tsx
│   ├── page.tsx              # Home page
│   ├── about/
│   │   └── page.tsx
│   ├── projects/
│   │   └── page.tsx
│   ├── contact/
│   │   └── page.tsx
│   └── globals.css
├── components/
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   ├── Hero.tsx
│   ├── ProjectCard.tsx
│   ├── TechStack.tsx
│   ├── ContactForm.tsx
│   └── ui/
│       ├── Button.tsx
│       └── Card.tsx
├── data/
│   └── projects.json
├── public/
│   └── images/
│       └── screenshots/
├── scripts/
│   └── sync_portfolio.py
├── .github/
│   └── workflows/
│       └── sync.yml
├── lib/
│   └── utils.ts
├── .env.example
├── .env.local
├── vercel.json
├── tailwind.config.ts
└── package.json
```

---

## 🎨 Configuration Files

### 1. Tailwind Configuration

Update `tailwind.config.ts`:

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        violet: {
          DEFAULT: "#6A1B9A",
          50: "#F3E5F5",
          100: "#E1BEE7",
          200: "#CE93D8",
          300: "#BA68C8",
          400: "#AB47BC",
          500: "#9C27B0",
          600: "#8E24AA",
          700: "#7B1FA2",
          800: "#6A1B9A",
          900: "#4A148C",
        },
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-in",
        "slide-up": "slideUp 0.5s ease-out",
        "slide-down": "slideDown 0.5s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        slideDown: {
          "0%": { transform: "translateY(-20px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
```

### 2. Environment Variables

Create `.env.example`:

```env
# EmailJS Configuration (for contact form)
NEXT_PUBLIC_EMAILJS_SERVICE_ID=your_service_id
NEXT_PUBLIC_EMAILJS_TEMPLATE_ID=your_template_id
NEXT_PUBLIC_EMAILJS_PUBLIC_KEY=your_public_key

# GitHub API (optional for private repos)
GITHUB_TOKEN=your_github_token

# Analytics (optional)
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=aymen-chaghoub.vercel.app
```

Create `.env.local` (copy from .env.example and fill in real values)

### 3. Vercel Configuration

Create `vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["cdg1"],
  "github": {
    "enabled": true,
    "autoAlias": true
  }
}
```

---

## 📄 Core Components

### 1. Utility Function

Create `lib/utils.ts`:

```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}
```

### 2. Navbar Component

Create `components/Navbar.tsx`:

```typescript
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

const navItems = [
  { name: "Home", path: "/" },
  { name: "Projects", path: "/projects" },
  { name: "About", path: "/about" },
  { name: "Contact", path: "/contact" },
];

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  return (
    <nav className="fixed top-0 w-full z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="text-xl font-bold text-violet">
            Aymen Chaghoub
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={cn(
                  "px-3 py-2 text-sm font-medium transition-colors",
                  pathname === item.path
                    ? "text-violet"
                    : "text-slate-300 hover:text-white"
                )}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 text-slate-300 hover:text-white"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-2">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                onClick={() => setIsOpen(false)}
                className={cn(
                  "block px-3 py-2 text-sm font-medium transition-colors",
                  pathname === item.path
                    ? "text-violet"
                    : "text-slate-300 hover:text-white"
                )}
              >
                {item.name}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}
```

### 3. Footer Component

Create `components/Footer.tsx`:

```typescript
import { Github, Linkedin, Mail, Twitter } from "lucide-react";
import Link from "next/link";

const socialLinks = [
  {
    name: "GitHub",
    href: "https://github.com/AymenChaghoub",
    icon: Github,
  },
  {
    name: "LinkedIn",
    href: "https://linkedin.com/in/aymen-chaghoub",
    icon: Linkedin,
  },
  {
    name: "Email",
    href: "mailto:aymen.chaghoub@example.com",
    icon: Mail,
  },
];

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-slate-950 border-t border-slate-800 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="text-lg font-bold text-violet mb-4">
              Aymen Chaghoub
            </h3>
            <p className="text-slate-400 text-sm">
              Full-Stack Developer passionate about building intelligent and
              scalable applications.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">
              Quick Links
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/projects"
                  className="text-slate-400 hover:text-violet text-sm transition-colors"
                >
                  Projects
                </Link>
              </li>
              <li>
                <Link
                  href="/about"
                  className="text-slate-400 hover:text-violet text-sm transition-colors"
                >
                  About
                </Link>
              </li>
              <li>
                <Link
                  href="/contact"
                  className="text-slate-400 hover:text-violet text-sm transition-colors"
                >
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Social Links */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Connect</h3>
            <div className="flex space-x-4">
              {socialLinks.map((link) => (
                <a
                  key={link.name}
                  href={link.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2 bg-slate-800 rounded-lg hover:bg-violet transition-colors"
                  aria-label={link.name}
                >
                  <link.icon className="h-5 w-5 text-slate-300" />
                </a>
              ))}
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-8 border-t border-slate-800 text-center">
          <p className="text-slate-400 text-sm">
            © {currentYear} Aymen Chaghoub. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
```

---

## 📄 Page Components

### Hero Component

Create `components/Hero.tsx`:

```typescript
"use client";

import { motion } from "framer-motion";
import { Github, Linkedin, Mail, ArrowDown } from "lucide-react";
import Link from "next/link";

export function Hero() {
  return (
    <section className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            Aymen Chaghoub
          </h1>
          <p className="text-2xl md:text-3xl text-violet font-semibold mb-4">
            Full-Stack Developer
          </p>
          <p className="text-lg md:text-xl text-slate-400 mb-8">
            Building intelligent & scalable applications
          </p>

          <div className="flex justify-center space-x-4 mb-12">
            <Link
              href="/projects"
              className="px-6 py-3 bg-violet text-white rounded-lg hover:bg-violet-700 transition-colors"
            >
              View Projects
            </Link>
            <Link
              href="/contact"
              className="px-6 py-3 bg-slate-800 text-white rounded-lg hover:bg-slate-700 transition-colors"
            >
              Get in Touch
            </Link>
          </div>

          <div className="flex justify-center space-x-6">
            {[
              {
                icon: Github,
                href: "https://github.com/AymenChaghoub",
                label: "GitHub",
              },
              {
                icon: Linkedin,
                href: "https://linkedin.com/in/aymen-chaghoub",
                label: "LinkedIn",
              },
              {
                icon: Mail,
                href: "mailto:aymen.chaghoub@example.com",
                label: "Email",
              },
            ].map((social) => (
              <a
                key={social.label}
                href={social.href}
                target="_blank"
                rel="noopener noreferrer"
                className="p-3 bg-slate-800 rounded-lg hover:bg-violet transition-colors"
                aria-label={social.label}
              >
                <social.icon className="h-6 w-6 text-slate-300" />
              </a>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.5 }}
          className="absolute bottom-10 left-1/2 transform -translate-x-1/2"
        >
          <ArrowDown className="h-8 w-8 text-slate-400 animate-bounce" />
        </motion.div>
      </div>
    </section>
  );
}
```

### Home Page

Update `app/page.tsx`:

```typescript
import { Hero } from "@/components/Hero";
import { ProjectCard } from "@/components/ProjectCard";
import { TechStack } from "@/components/TechStack";
import projects from "@/data/projects.json";

export default function Home() {
  const featuredProjects = projects.slice(0, 3);

  return (
    <main className="min-h-screen">
      <Hero />

      {/* Featured Projects */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-12 text-center">
            Featured Projects
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredProjects.map((project, index) => (
              <ProjectCard key={index} project={project} index={index} />
            ))}
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <TechStack />
    </main>
  );
}
```

---

## 📊 Data Structure

Create `data/projects.json`:

```json
[
  {
    "name": "School Records Management System",
    "description": "A production-ready full-stack web application for managing student academic records with role-based access control, JWT authentication, and comprehensive monitoring.",
    "stack": ["FastAPI", "React", "MySQL", "Docker", "TypeScript", "Tailwind CSS"],
    "image": "/images/screenshots/school-records.png",
    "demo": "https://pfc.netlify.app",
    "github": "https://github.com/AymenChaghoub/PFE_School_Records",
    "docs": "/docs/School_Records_Management_Documentation.pdf",
    "featured": true,
    "category": "Full-Stack",
    "year": 2025,
    "highlights": [
      "JWT Authentication with Refresh Token Rotation",
      "Role-Based Access Control (RBAC)",
      "51%+ Test Coverage with pytest",
      "Docker & Docker Compose Support",
      "Monitoring & Analytics Integration",
      "Comprehensive Documentation (5,500+ lines)"
    ]
  },
  {
    "name": "Bike-Sharing System",
    "description": "A Java-based bike-sharing management system demonstrating design patterns including Singleton, Factory, Observer, and Strategy patterns with Maven build system.",
    "stack": ["Java", "Maven", "Design Patterns", "JUnit"],
    "image": "/images/screenshots/bike-sharing.png",
    "github": "https://github.com/AymenChaghoub/Bike_Sharing_System",
    "featured": true,
    "category": "Backend",
    "year": 2024,
    "highlights": [
      "Implemented 4+ Design Patterns",
      "Maven Build System",
      "Unit Testing with JUnit",
      "Clean Architecture"
    ]
  },
  {
    "name": "Data Science Portfolio",
    "description": "Collection of data science projects including machine learning models, data analysis, and visualizations using Python, Pandas, and scikit-learn.",
    "stack": ["Python", "Pandas", "scikit-learn", "Matplotlib", "Jupyter"],
    "image": "/images/screenshots/data-science.png",
    "github": "https://github.com/AymenChaghoub/Data_Science_Portfolio",
    "featured": true,
    "category": "Data Science",
    "year": 2024,
    "highlights": [
      "Machine Learning Models",
      "Data Analysis & Visualization",
      "Jupyter Notebooks",
      "Statistical Analysis"
    ]
  }
]
```

---

## 🚀 Running the Portfolio

```powershell
# Development
npm run dev

# Production Build
npm run build

# Start Production Server
npm start

# Lint
npm run lint
```

**Access**: http://localhost:3000

---

## 📝 Next Steps

1. **Complete all component files** (see full guide)
2. **Add project screenshots** to `/public/images/screenshots/`
3. **Configure EmailJS** for contact form
4. **Set up Phase 9.5** (Auto-sync script)
5. **Deploy to Vercel**

---

**Last Updated**: November 2025  
**Status**: 📋 Setup Guide Complete
