# 🔄 Auto-Sync Portfolio Script - Phase 9.5

Automated GitHub repository synchronization for portfolio website

---

## 📋 Overview

The auto-sync script automatically fetches your latest GitHub repositories and updates your portfolio website's project list.

**Features**:
- Fetches top 5 repositories from GitHub
- Sorts by recent push date
- Extracts name, description, language, topics, stars
- Updates `projects.json` automatically
- Runs weekly via GitHub Actions
- Manual run support

---

## 📄 Sync Script

Create `Portfolio_Aymen/scripts/sync_portfolio.py`:

```python
#!/usr/bin/env python3
"""
Portfolio Auto-Sync Script
Fetches latest GitHub repositories and updates projects.json
"""

import json
import os
import requests
from datetime import datetime
from pathlib import Path

# Configuration
GITHUB_USERNAME = "AymenChaghoub"
GITHUB_API_URL = "https://api.github.com"
OUTPUT_FILE = "../data/projects.json"
MAX_REPOS = 5

# Optional: GitHub token for higher rate limits (60 → 5000 requests/hour)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")


def fetch_github_repos():
    """Fetch repositories from GitHub API"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    url = f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}/repos"
    params = {
        "sort": "pushed",
        "direction": "desc",
        "per_page": MAX_REPOS,
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching repos: {e}")
        return []


def map_language_to_stack(language, topics):
    """Map primary language and topics to tech stack"""
    stack = []
    
    # Add primary language
    if language:
        stack.append(language)
    
    # Map topics to common tech names
    tech_map = {
        "react": "React",
        "nextjs": "Next.js",
        "typescript": "TypeScript",
        "javascript": "JavaScript",
        "python": "Python",
        "fastapi": "FastAPI",
        "django": "Django",
        "flask": "Flask",
        "nodejs": "Node.js",
        "express": "Express",
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "mongodb": "MongoDB",
        "redis": "Redis",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "aws": "AWS",
        "gcp": "Google Cloud",
        "azure": "Azure",
        "tailwindcss": "Tailwind CSS",
        "sass": "SASS",
        "vue": "Vue.js",
        "angular": "Angular",
        "graphql": "GraphQL",
        "rest-api": "REST API",
        "machine-learning": "Machine Learning",
        "data-science": "Data Science",
        "jupyter": "Jupyter",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "scikit-learn": "scikit-learn",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
    }
    
    for topic in topics:
        topic_lower = topic.lower()
        if topic_lower in tech_map and tech_map[topic_lower] not in stack:
            stack.append(tech_map[topic_lower])
    
    return stack[:6]  # Limit to 6 technologies


def categorize_project(language, topics, description):
    """Determine project category based on content"""
    description_lower = description.lower() if description else ""
    topics_str = " ".join(topics).lower()
    
    # Full-Stack indicators
    if any(
        term in topics_str or term in description_lower
        for term in ["full-stack", "fullstack", "backend", "frontend"]
    ):
        return "Full-Stack"
    
    # Data Science indicators
    if any(
        term in topics_str or term in description_lower
        for term in [
            "data-science",
            "machine-learning",
            "ml",
            "ai",
            "jupyter",
            "pandas",
            "analysis",
        ]
    ):
        return "Data Science"
    
    # Mobile indicators
    if any(
        term in topics_str or term in description_lower
        for term in ["mobile", "android", "ios", "react-native", "flutter"]
    ):
        return "Mobile"
    
    # Backend-only
    if language in ["Python", "Java", "Go", "Rust", "PHP"] and "frontend" not in topics_str:
        return "Backend"
    
    # Frontend-only
    if language in ["JavaScript", "TypeScript", "HTML", "CSS"]:
        return "Frontend"
    
    return "Other"


def transform_repo_to_project(repo):
    """Transform GitHub repo data to portfolio project format"""
    stack = map_language_to_stack(repo.get("language"), repo.get("topics", []))
    category = categorize_project(
        repo.get("language"), repo.get("topics", []), repo.get("description")
    )
    
    return {
        "name": repo["name"].replace("-", " ").replace("_", " ").title(),
        "description": repo.get("description") or "No description provided.",
        "stack": stack,
        "image": f"/images/screenshots/{repo['name'].lower()}.png",
        "github": repo["html_url"],
        "demo": repo.get("homepage") or None,
        "featured": repo.get("stargazers_count", 0) > 0,
        "category": category,
        "year": datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ").year,
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "lastUpdated": repo.get("pushed_at"),
        "highlights": [],
    }


def load_existing_projects():
    """Load existing projects.json to preserve manual data"""
    script_dir = Path(__file__).parent
    projects_file = script_dir / OUTPUT_FILE
    
    if projects_file.exists():
        try:
            with open(projects_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Existing projects.json is invalid, starting fresh")
            return []
    return []


def merge_projects(existing_projects, new_projects):
    """Merge existing manually-added projects with auto-fetched ones"""
    # Create a map of existing projects by GitHub URL or name
    existing_map = {}
    for project in existing_projects:
        key = project.get("github") or project.get("name")
        if key:
            existing_map[key] = project
    
    # Update or add new projects
    merged = []
    for new_project in new_projects:
        key = new_project.get("github") or new_project.get("name")
        
        if key in existing_map:
            # Preserve manual data (highlights, custom description, etc.)
            existing = existing_map[key]
            merged_project = {
                **new_project,
                "highlights": existing.get("highlights", []),
                "docs": existing.get("docs"),
            }
            # Keep custom description if it's more detailed
            if len(existing.get("description", "")) > len(new_project["description"]):
                merged_project["description"] = existing["description"]
            merged.append(merged_project)
            del existing_map[key]
        else:
            merged.append(new_project)
    
    # Add remaining existing projects (not on GitHub)
    for remaining_project in existing_map.values():
        merged.append(remaining_project)
    
    return merged


def save_projects(projects):
    """Save projects to JSON file"""
    script_dir = Path(__file__).parent
    projects_file = script_dir / OUTPUT_FILE
    
    # Ensure data directory exists
    projects_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Sort by featured status and stars
    projects.sort(
        key=lambda x: (x.get("featured", False), x.get("stars", 0)), reverse=True
    )
    
    with open(projects_file, "w", encoding="utf-8") as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(projects)} projects to {projects_file}")


def main():
    print("🔄 Syncing portfolio with GitHub...")
    print(f"   Username: {GITHUB_USERNAME}")
    print(f"   Fetching top {MAX_REPOS} repositories...")
    
    # Fetch repos from GitHub
    repos = fetch_github_repos()
    
    if not repos:
        print("⚠️  No repositories fetched. Exiting.")
        return
    
    print(f"✅ Fetched {len(repos)} repositories")
    
    # Transform to project format
    new_projects = [transform_repo_to_project(repo) for repo in repos]
    
    # Load existing projects
    existing_projects = load_existing_projects()
    print(f"📂 Loaded {len(existing_projects)} existing projects")
    
    # Merge
    merged_projects = merge_projects(existing_projects, new_projects)
    
    # Save
    save_projects(merged_projects)
    
    print(f"\n📊 Summary:")
    print(f"   Total Projects: {len(merged_projects)}")
    print(f"   Featured: {sum(1 for p in merged_projects if p.get('featured'))}")
    print(f"   Categories: {set(p['category'] for p in merged_projects)}")
    print("\n✅ Sync complete!")


if __name__ == "__main__":
    main()
```

---

## 🤖 GitHub Actions Workflow

Create `.github/workflows/sync.yml`:

```yaml
name: Auto Sync Portfolio Projects

on:
  # Run every Monday at 9 AM UTC
  schedule:
    - cron: "0 9 * * 1"
  
  # Allow manual trigger
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install Dependencies
        run: pip install requests
      
      - name: Run Sync Script
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/sync_portfolio.py
        working-directory: ./
      
      - name: Check for Changes
        id: verify_diff
        run: |
          git diff --quiet data/projects.json || echo "changed=true" >> $GITHUB_OUTPUT
      
      - name: Commit & Push Changes
        if: steps.verify_diff.outputs.changed == 'true'
        run: |
          git config --global user.name "Aymen Chaghoub"
          git config --global user.email "aymen.chaghoub@example.com"
          git add data/projects.json
          git commit -m "🔄 Auto-update projects.json [skip ci]"
          git push
```

---

## 🚀 Usage

### Manual Sync (Local)

```powershell
# Navigate to scripts directory
cd Portfolio_Aymen/scripts

# Install requests library
pip install requests

# Run sync
python sync_portfolio.py
```

**Expected Output**:
```
🔄 Syncing portfolio with GitHub...
   Username: AymenChaghoub
   Fetching top 5 repositories...
✅ Fetched 5 repositories
📂 Loaded 3 existing projects
✅ Saved 5 projects to ../data/projects.json

📊 Summary:
   Total Projects: 5
   Featured: 3
   Categories: {'Full-Stack', 'Backend', 'Data Science'}

✅ Sync complete!
```

### Automatic Sync (GitHub Actions)

**Runs automatically**:
- Every Monday at 9 AM UTC
- Can be triggered manually from GitHub Actions tab

**How to trigger manually**:
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Auto Sync Portfolio Projects"
4. Click "Run workflow"

---

## 🔐 Environment Variables

### For Local Development

Create `.env` in scripts directory (optional):
```env
GITHUB_TOKEN=your_github_personal_access_token
```

### For GitHub Actions

The workflow uses `${{ secrets.GITHUB_TOKEN }}` which is automatically provided.

For private repositories, you may need to create a Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Add as repository secret named `GH_PAT`
4. Update workflow to use `${{ secrets.GH_PAT }}`

---

## 📝 Customization

### Change Number of Repositories

Edit `sync_portfolio.py`:
```python
MAX_REPOS = 10  # Fetch top 10 instead of 5
```

### Add Custom Project Data

Manually edit `data/projects.json` to add:
- `highlights` array
- `docs` link
- Custom `description`
- `demo` URL

These will be preserved during auto-sync!

### Change Sync Schedule

Edit `.github/workflows/sync.yml`:
```yaml
schedule:
  - cron: "0 0 * * *"  # Daily at midnight
  # OR
  - cron: "0 */6 * * *"  # Every 6 hours
```

**Cron syntax**: `minute hour day month weekday`

---

## 🔄 Update Process

1. **GitHub Actions runs** (weekly or manual)
2. **Script fetches** latest repos from GitHub
3. **Data merges** with existing projects.json
4. **Preserves** manual additions (highlights, docs, etc.)
5. **Commits & pushes** updated projects.json
6. **Vercel auto-deploys** new portfolio version

---

## 🎯 Features

### Preserved Data
- ✅ Custom descriptions (if longer than GitHub's)
- ✅ Highlights array
- ✅ Documentation links
- ✅ Demo URLs (if added manually)
- ✅ Custom images

### Auto-Updated Data
- ✅ Repository name
- ✅ GitHub URL
- ✅ Stars count
- ✅ Forks count
- ✅ Last updated date
- ✅ Primary language
- ✅ Topics → Tech stack

### Smart Categorization
- Full-Stack
- Backend
- Frontend
- Mobile
- Data Science
- Other

---

## 🐛 Troubleshooting

### Rate Limit Error
```
❌ Error fetching repos: 403 Client Error
```

**Solution**: Add GitHub token to increase rate limit (60 → 5000)

### No Projects Fetched
- Check GitHub username is correct
- Ensure repositories are public
- Verify GitHub API is accessible

### Projects.json Not Updated
- Check file permissions
- Verify script ran successfully
- Check GitHub Actions logs

---

## 📊 Testing

```powershell
# Test sync script
cd Portfolio_Aymen/scripts
python sync_portfolio.py

# Verify output
cat ../data/projects.json
```

---

**Last Updated**: November 2025  
**Status**: 📋 Auto-Sync Guide Complete
